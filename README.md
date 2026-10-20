# Aanchal Boutique Support Tickets

A customer support ticket dashboard for Aanchal Boutique, built with React and FastAPI. The application generates 50 realistic sample support tickets using Faker, stores them in a SQLite database, and provides a paginated API for retrieving tickets. The React frontend displays customer queries in a table with Previous and Next pagination controls.

## Technologies Used

- React
- JavaScript
- Python
- FastAPI
- Uvicorn
- SQLite
- Faker
- Git and GitHub

## Project Structure

```text
aanchal-boutique-support/
├── backend/
│   ├── main.py
│   ├── generate_tickets.py
│   ├── requirements.txt
│   ├── tickets.db          # Generated locally
│   └── venv/               # Local Python virtual environment
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── package-lock.json
├── .gitignore
├── LICENSE
└── README.md
```

The SQLite database and Python virtual environment are generated or maintained locally and should not be committed to Git.

## Requirements

Install the following before running the application:

- Python 3
- Node.js and npm
- Git

## Local Installation and Setup

### 1. Clone the Repository

Open a terminal and run:

```bash
git clone https://github.com/areebkhan47/aanchal-boutique-support.git
cd aanchal-boutique-support
```

### 2. Set Up the FastAPI Backend

Navigate to the backend directory:

```powershell
cd backend
```

Create a Python virtual environment:

```powershell
py -m venv venv
```

Activate it in Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use Command Prompt instead:

```cmd
venv\Scripts\activate.bat
```

Install the backend dependencies:

```powershell
python -m pip install -r requirements.txt
```

### 3. Generate Sample Support Tickets

From the `backend` directory, run:

```powershell
python generate_tickets.py
```

The script generates 50 realistic sample support tickets and stores them in `backend/tickets.db`.

Each ticket includes:

- Ticket ID
- Customer name
- Customer email
- Subject
- Message body
- Creation date

Running the script again replaces the existing sample dataset with a newly generated set of 50 tickets.

### 4. Start the FastAPI Server

While still in the `backend` directory, run:

```powershell
python -m uvicorn main:app --reload
```

The backend will be available at:

- **API home:** http://127.0.0.1:8000/
- **Paginated tickets:** http://127.0.0.1:8000/tickets?page=1&size=10
- **Alternative API endpoint:** http://127.0.0.1:8000/api/tickets?page=1&size=10
- **Interactive API documentation:** http://127.0.0.1:8000/docs

Keep the backend terminal running while using the application.

### 5. Understand API Pagination

The `/tickets` endpoint supports two query parameters:

| Parameter | Description | Default | Allowed values |
|---|---|---|---|
| `page` | Page number | 1 | 1 or greater |
| `size` | Number of tickets per page | 10 | 1–50 |

Example requests:

```text
/tickets?page=1&size=10
/tickets?page=2&size=10
/tickets?page=1&size=5
```

The API response includes:

- `tickets`: The requested ticket records.
- `page`: The current page number.
- `size`: The requested page size.
- `total`: The total number of tickets in the database.
- `total_pages`: The total number of available pages.

For example, with 50 tickets and a page size of 10, the API returns five pages.

### 6. Start the React Frontend

Open a second terminal in the project root directory:

```powershell
cd frontend
```

Install the frontend dependencies:

```powershell
npm install
```

Start the React development server:

```powershell
npm start
```

The frontend will be available at:

http://localhost:3000

Keep both the backend and frontend terminals running.

### 7. Use the Application

Open http://localhost:3000 in your browser.

The dashboard retrieves ticket records from the FastAPI backend and displays them in a table.

Use the Previous and Next buttons to navigate between pages of tickets.

## Task 2: Sample Ticket Generation and Pagination

This task introduces realistic sample data generation, SQLite storage, and paginated API access.

The generator creates 50 support tickets covering common boutique customer service issues, including:

- Order delivery delays
- Return requests
- Size exchanges
- Incorrect or damaged products
- Payment confirmations
- Order cancellations
- Product sizing questions
- Missing items
- Product availability

SQLite stores the generated records locally. FastAPI retrieves them using pagination, while React displays the results and allows users to navigate between pages.

## Notes

- The SQLite database is generated locally and excluded from Git.
- Run `python generate_tickets.py` before starting the backend if the database does not exist.
- The frontend expects the backend to be available at `http://127.0.0.1:8000`.
- This project uses sample data for development and demonstration purposes.