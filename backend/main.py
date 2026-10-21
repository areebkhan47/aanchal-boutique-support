import sqlite3
from contextlib import closing
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware


# --------------------------------------------------
# 1. File paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATABASE_PATH = BASE_DIR / "tickets.db"
INDEX_PATH = BASE_DIR / "tickets.index"
METADATA_PATH = BASE_DIR / "ticket_ids.npy"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


# --------------------------------------------------
# 2. Create FastAPI application
# --------------------------------------------------

app = FastAPI(title="Aanchal Boutique Support API")


# Allow React to communicate with FastAPI.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# 3. AI search resources
# --------------------------------------------------

embedding_model = None
faiss_index = None
ticket_ids = None


@app.on_event("startup")
def load_search_resources():
    """Load the embedding model and FAISS index when the API starts."""

    global embedding_model, faiss_index, ticket_ids

    # Check that the index-building script has been run.
    if not INDEX_PATH.exists() or not METADATA_PATH.exists():
        print(
            "Similarity search is unavailable. "
            "Run build_index.py to create the index files."
        )
        return

    try:
        print("Loading embedding model...")

        embedding_model = SentenceTransformer(MODEL_NAME)

        print("Loading FAISS index...")

        faiss_index = faiss.read_index(str(INDEX_PATH))

        ticket_ids = np.load(METADATA_PATH)

        # Verify that every indexed vector has a corresponding ticket ID.
        if faiss_index.ntotal != len(ticket_ids):
            raise ValueError(
                "FAISS index size does not match the ticket-ID mapping."
            )

        print(f"AI search ready. Indexed tickets: {faiss_index.ntotal}")

    except Exception as error:
        embedding_model = None
        faiss_index = None
        ticket_ids = None

        print(f"Could not initialize AI search: {error}")


# --------------------------------------------------
# 4. Database connection
# --------------------------------------------------

def get_database_connection():
    """Open a connection to the SQLite database."""

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection


# --------------------------------------------------
# 5. Home endpoint
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Aanchal Boutique Support API is running"
    }


# --------------------------------------------------
# 6. Paginated tickets endpoint
# --------------------------------------------------

@app.get("/tickets")
def get_tickets(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=50),
):
    """Return a page of support tickets from SQLite."""

    offset = (page - 1) * size

    with closing(get_database_connection()) as connection:

        total = connection.execute(
            "SELECT COUNT(*) FROM tickets"
        ).fetchone()[0]

        rows = connection.execute(
            """
            SELECT id, customer_name, customer_email, subject, body, date
            FROM tickets
            ORDER BY id ASC
            LIMIT ? OFFSET ?
            """,
            (size, offset),
        ).fetchall()

    tickets = [dict(row) for row in rows]

    return {
        "tickets": tickets,
        "page": page,
        "size": size,
        "total": total,
        "total_pages": (total + size - 1) // size,
    }


# --------------------------------------------------
# 7. Original API endpoint
# --------------------------------------------------

@app.get("/api/tickets")
def get_api_tickets(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=50),
):
    """Keep the original API path available for compatibility."""

    return get_tickets(page=page, size=size)


# --------------------------------------------------
# 8. AI similarity-search endpoint
# --------------------------------------------------

@app.get("/similar")
def find_similar_tickets(
    text: str = Query(min_length=1, max_length=1000),
):
    """Find the three most similar historical support tickets."""

    # Make sure the model and index are available.
    if (
        embedding_model is None
        or faiss_index is None
        or ticket_ids is None
    ):
        raise HTTPException(
            status_code=503,
            detail=(
                "AI search is not ready. "
                "Check the backend logs and rebuild the index if necessary."
            ),
        )

    # Remove unnecessary spaces.
    search_text = text.strip()

    if not search_text:
        raise HTTPException(
            status_code=422,
            detail="Search text cannot be empty.",
        )

    # Convert the search query into a normalized embedding.
    query_embedding = embedding_model.encode(
        [search_text],
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    query_embedding = np.asarray(
        query_embedding,
        dtype=np.float32,
    )

    # Search for up to three similar ticket vectors.
    number_of_results = min(3, faiss_index.ntotal)

    if number_of_results == 0:
        return {
            "query": search_text,
            "results": [],
        }

    scores, positions = faiss_index.search(
        query_embedding,
        number_of_results,
    )

    # Convert FAISS positions into original SQLite ticket IDs.
    matched_ids = [
        int(ticket_ids[position])
        for position in positions[0]
        if position >= 0
    ]

    if not matched_ids:
        return {
            "query": search_text,
            "results": [],
        }

    # Retrieve ticket details from SQLite.
    placeholders = ",".join("?" for _ in matched_ids)

    with closing(get_database_connection()) as connection:
        rows = connection.execute(
            f"""
            SELECT id, customer_name, customer_email, subject, body, date
            FROM tickets
            WHERE id IN ({placeholders})
            """,
            matched_ids,
        ).fetchall()

    # Build a lookup so we can preserve FAISS ranking order.
    tickets_by_id = {
        row["id"]: dict(row)
        for row in rows
    }

    results = []

    for position, score in zip(
        positions[0],
        scores[0],
    ):
        if position < 0:
            continue

        ticket_id = int(ticket_ids[position])

        ticket = tickets_by_id.get(ticket_id)

        if ticket is None:
            continue

        ticket["similarity_score"] = round(float(score), 4)

        results.append(ticket)

    return {
        "query": search_text,
        "results": results,
    }