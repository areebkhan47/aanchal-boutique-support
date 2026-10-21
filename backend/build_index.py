import sqlite3
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Paths relative to this script
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "tickets.db"
INDEX_PATH = BASE_DIR / "tickets.index"
METADATA_PATH = BASE_DIR / "ticket_ids.npy"

# Pretrained sentence embedding model
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def build_index():
    # Check that the database exists
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DATABASE_PATH}. "
            "Run generate_tickets.py first."
        )

    # Read ticket records from SQLite
    with sqlite3.connect(DATABASE_PATH) as connection:
        rows = connection.execute(
            """
            SELECT id, subject, body
            FROM tickets
            ORDER BY id
            """
        ).fetchall()

    if not rows:
        raise ValueError(
            "No tickets found. Generate sample tickets first."
        )

    ticket_ids = [row[0] for row in rows]
    subjects = [row[1] for row in rows]
    bodies = [row[2] for row in rows]

    print(f"Loaded {len(rows)} tickets from SQLite.")
    print(f"Loading embedding model: {MODEL_NAME}")

    # Load the pretrained model
    model = SentenceTransformer(MODEL_NAME)

    # Convert ticket bodies into normalized vectors
    embeddings = model.encode(
        bodies,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    embeddings = np.asarray(embeddings, dtype=np.float32)

    # Build a FAISS index using inner product.
    # Because the vectors are normalized, this gives cosine similarity.
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    # Save the index and its corresponding ticket metadata
    faiss.write_index(index, str(INDEX_PATH))

    np.save(
        METADATA_PATH,
        np.asarray(ticket_ids, dtype=np.int64),
    )

    print("\nIndex built successfully!")
    print(f"Tickets indexed: {index.ntotal}")
    print(f"Vector dimensions: {dimension}")
    print(f"FAISS index: {INDEX_PATH}")
    print(f"Ticket ID mapping: {METADATA_PATH}")

    # Show the first few records to verify the mapping
    print("\nFirst three indexed tickets:")
    for ticket_id, subject in zip(ticket_ids[:3], subjects[:3]):
        print(f"ID {ticket_id}: {subject}")


if __name__ == "__main__":
    build_index()