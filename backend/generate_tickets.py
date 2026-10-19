import random
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

from faker import Faker


# Generate fictional customer information.
fake = Faker()
Faker.seed(42)
random.seed(42)

# Store the database beside this Python script.
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "tickets.db"

TICKET_COUNT = 50


# Boutique-specific subjects and customer problems.
TICKET_TEMPLATES = [
    (
        "Order delivery delay",
        [
            "My order has not arrived yet. Could you please check its delivery status?",
            "The expected delivery date has passed, but I still have not received my parcel.",
            "My tracking information has not changed for several days. Please help.",
        ],
    ),
    (
        "Return request",
        [
            "I would like to return this dress because it does not suit me.",
            "Please explain how I can return my recent purchase.",
            "The item is different from what I expected. Can I return it?",
        ],
    ),
    (
        "Size exchange",
        [
            "The dress I received is too small. Can I exchange it for a larger size?",
            "I ordered a medium, but I need a large. Please guide me through an exchange.",
            "Could you tell me whether an exchange is possible for my order?",
        ],
    ),
    (
        "Incorrect item received",
        [
            "I received a different design from the one I ordered.",
            "The colour of the delivered outfit does not match my order.",
            "Could you help me resolve an incorrect item delivery?",
        ],
    ),
    (
        "Damaged product",
        [
            "My parcel arrived with a damaged dress. What should I do next?",
            "I noticed a tear in the outfit after opening the package.",
            "The product arrived damaged, and I would like assistance with a replacement.",
        ],
    ),
    (
        "Payment confirmation",
        [
            "My payment was successful, but I have not received an order confirmation.",
            "The amount was deducted from my account. Could you confirm my order?",
            "Please check whether my online payment has been received.",
        ],
    ),
    (
        "Order cancellation",
        [
            "I would like to cancel my order. Please let me know if it is still possible.",
            "I placed an order by mistake. Can you help me cancel it?",
            "Could you confirm whether my order can be cancelled before dispatch?",
        ],
    ),
    (
        "Product sizing information",
        [
            "Could you share the size chart for this outfit?",
            "I am unsure which size to choose. Can you provide measurements?",
            "Please help me select the correct size before I place my order.",
        ],
    ),
    (
        "Missing item",
        [
            "One item appears to be missing from my parcel.",
            "My package arrived, but it contains fewer items than I ordered.",
            "Could you check why one of the products is missing from my delivery?",
        ],
    ),
    (
        "Product availability",
        [
            "Will this design be available again in my preferred size?",
            "I would like to know when this outfit will be back in stock.",
            "Can you tell me whether this design is available in another colour?",
        ],
    ),
]


def create_database(connection):
    """Create the tickets table if it does not already exist."""
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            subject TEXT NOT NULL,
            body TEXT NOT NULL,
            date TEXT NOT NULL
        )
        """
    )

    connection.commit()


def generate_ticket():
    """Create one fictional customer support ticket."""
    subject, possible_messages = random.choice(TICKET_TEMPLATES)

    customer_name = fake.name()
    customer_email = fake.email()

    message = random.choice(possible_messages)

    # Add a fictional order reference to make the message more realistic.
    order_number = f"AB-{random.randint(10000, 99999)}"

    body = (
        f"Hello Support Team,\n\n"
        f"My name is {customer_name}. {message}\n\n"
        f"My order reference is {order_number}.\n"
        f"Thank you for your assistance."
    )

    # Generate a date within the previous 90 days.
    days_ago = random.randint(0, 90)
    seconds_ago = random.randint(0, 86399)

    created_at = datetime.now(timezone.utc) - timedelta(
        days=days_ago,
        seconds=seconds_ago,
    )

    return (
        customer_name,
        customer_email,
        subject,
        body,
        created_at.isoformat(timespec="seconds"),
    )


def generate_tickets():
    """Create the database and insert 50 sample tickets."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        create_database(connection)

        # Make repeated runs safe: replace the sample dataset.
        connection.execute("DELETE FROM tickets")
        connection.execute(
            "DELETE FROM sqlite_sequence WHERE name = 'tickets'"
        )

        tickets = [generate_ticket() for _ in range(TICKET_COUNT)]

        connection.executemany(
            """
            INSERT INTO tickets (
                customer_name,
                customer_email,
                subject,
                body,
                date
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            tickets,
        )

        connection.commit()

        total = connection.execute(
            "SELECT COUNT(*) FROM tickets"
        ).fetchone()[0]

    print(f"Successfully generated {total} support tickets.")
    print(f"Database location: {DATABASE_PATH}")


if __name__ == "__main__":
    generate_tickets()