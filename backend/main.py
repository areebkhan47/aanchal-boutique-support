import sqlite3
from contextlib import closing
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware


# Locate the SQLite database beside this file.
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "tickets.db"

app = FastAPI(title="Aanchal Boutique Support API")


# Allow the React development server to call the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_database_connection():
    """Open a connection to the SQLite database."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


@app.get("/")
def home():
    return {
        "message": "Aanchal Boutique Support API is running"
    }


@app.get("/tickets")
def get_tickets(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=50),
):
    """
    Return a page of support tickets from SQLite.

    page: page number, starting at 1
    size: number of tickets per page
    """

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


@app.get("/api/tickets")
def get_api_tickets(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=50),
):
    """Keep the original API path available for compatibility."""
    return get_tickets(page=page, size=size)