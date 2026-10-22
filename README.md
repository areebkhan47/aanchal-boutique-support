# Aanchal Boutique Support

A simple customer support ticket management dashboard built with **React, FastAPI, SQLite, and AI-powered semantic search**.

The application displays customer support tickets and allows users to find similar tickets by searching with natural language. Instead of matching only exact words, the AI search understands the meaning of a query and finds tickets with similar content.

## Features

* **Support Ticket Dashboard:** Displays customer support tickets, including customer name, subject, message, and date.
* **Sample Ticket Data:** Generates 50 realistic sample tickets using Faker.
* **Pagination:** Displays tickets in pages so users can navigate through the dataset.
* **AI-Powered Search:** Finds up to three tickets that are semantically similar to a user's search.
* **FastAPI Backend:** Provides REST API endpoints for retrieving and searching tickets.
* **React Frontend:** Provides a simple interface for viewing tickets and searching for similar ones.
* **SQLite Database:** Stores ticket information locally.
* **FAISS Search Index:** Enables efficient similarity searches over ticket embeddings.

## Technologies Used

| Technology            | Purpose                                        |
| --------------------- | ---------------------------------------------- |
| React                 | Builds the frontend user interface             |
| JavaScript            | Handles frontend logic and API requests        |
| Python                | Implements the backend and AI search           |
| FastAPI               | Provides REST API endpoints                    |
| SQLite                | Stores support ticket data                     |
| Faker                 | Generates realistic sample tickets             |
| Sentence Transformers | Converts ticket text into numerical embeddings |
| all-MiniLM-L6-v2      | Generates text embeddings for semantic search  |
| FAISS                 | Searches for similar ticket embeddings         |
| NumPy                 | Stores and manages numerical data              |

## Project Structure

```text
aanchal-boutique-support/
│
├── backend/
│   ├── main.py
│   ├── generate_tickets.py
│   ├── build_index.py
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.js
│   │   ├── App.css
│   │   └── ...
│   ├── package.json
│   └── ...
│
├── .gitignore
├── LICENSE
└── README.md
```

**Note:** `tickets.db`, `tickets.index`, and `ticket_ids.npy` are generated files. They are excluded from Git and can be recreated locally using the scripts provided in the backend.

## How It Works

### 1. Generating Sample Tickets

The `generate_tickets.py` script creates 50 realistic sample support tickets using Faker and saves them in an SQLite database named `tickets.db`.

Each ticket contains information such as:

* Ticket ID
* Customer name
* Customer email
* Subject
* Message body
* Date

### 2. Building the AI Search Index

The `build_index.py` script prepares the ticket data for semantic search.

It performs the following steps:

1. Reads ticket information from the SQLite database.
2. Loads the `sentence-transformers/all-MiniLM-L6-v2` model.
3. Converts each ticket's message into a numerical embedding.
4. Normalizes the embeddings for cosine-similarity-style comparison.
5. Creates a FAISS index using inner-product similarity.
6. Saves the index to `tickets.index`.
7. Saves the corresponding ticket IDs to `ticket_ids.npy`.

These generated files allow the backend to search for similar tickets without rebuilding the index for every request.

### 3. Searching for Similar Tickets

When a user enters a search query in the React interface:

1. React sends the query to the FastAPI backend.
2. The AI model converts the query into an embedding.
3. FAISS searches the index for the most similar ticket embeddings.
4. The backend retrieves the matching ticket details from SQLite.
5. The API returns up to three matching tickets, along with similarity scores.
6. React displays the results to the user.

For example, searching for:

`I need to exchange my dress for a different size.`

can return tickets about size exchanges or related return requests, even when their wording differs.

**Important:** Similarity scores measure how closely the text embeddings match. They are not probabilities that a ticket is the correct answer.

## Requirements

Install the following software before running the project:

* Python
* Node.js and npm
* Git
* Visual Studio Code or another code editor

An internet connection is needed the first time you install dependencies and download the AI model. After the required packages and model are available locally, the application can run on your computer.

## Installation and Setup

### Step 1: Clone the Repository

Open a terminal and run:

```bash
git clone https://github.com/areebkhan47/aanchal-boutique-support.git
cd aanchal-boutique-support
```

### Step 2: Set Up the Backend

Open a terminal in the project directory.

Move into the backend folder:

```bash
cd backend
```

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the backend dependencies:

```bash
python -m pip install -r requirements.txt
```

### Step 3: Generate the Ticket Database

Run the following command from the `backend` directory:

```bash
python generate_tickets.py
```

This creates the SQLite database and populates it with sample tickets.

Run this step when setting up a fresh copy of the project or when you need to regenerate the sample dataset.

### Step 4: Build the AI Search Index

After generating the database, run:

```bash
python build_index.py
```

This script generates the ticket embeddings and creates the following files:

* `tickets.index` — the FAISS similarity-search index.
* `ticket_ids.npy` — the mapping between index positions and ticket IDs.

**Rebuild the index whenever the ticket dataset changes** so that the search results remain consistent with the database.

### Step 5: Start the Backend Server

From the `backend` directory, run:

```bash
uvicorn main:app --reload
```

The backend API will be available at:

`http://127.0.0.1:8000`

The interactive API documentation is available at:

`http://127.0.0.1:8000/docs`

Keep this terminal running while using the application.

### Step 6: Set Up the Frontend

Open a second terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install the frontend dependencies:

```bash
npm install
```

Start the React development server:

```bash
npm start
```

The frontend will normally open at:

`http://localhost:3000`

Keep both the backend and frontend servers running while testing the application.

## API Endpoints

### 1. Home

**Endpoint:** `GET /`

Returns a basic response from the backend.

Example:

```text
http://127.0.0.1:8000/
```

### 2. Get Paginated Tickets

**Endpoint:** `GET /tickets`

Returns support tickets with pagination.

**Query parameters:**

* `page` — the page number, starting from 1.
* `size` — the number of tickets per page, from 1 to 50.

Example:

```text
http://127.0.0.1:8000/tickets?page=1&size=10
```

The response includes the tickets and pagination information, such as the current page, page size, total ticket count, and total number of pages.

### 3. Find Similar Tickets

**Endpoint:** `GET /similar`

Finds tickets with content similar to the supplied text.

**Query parameter:**

* `text` — the text to search for.

Example:

```text
http://127.0.0.1:8000/similar?text=I%20need%20a%20dress%20size%20exchange
```

The response contains up to three matching tickets, including their details and similarity scores.

### 4. Legacy Ticket Endpoint

**Endpoint:** `GET /api/tickets`

The original ticket API endpoint is retained for compatibility with the initial version of the project.

## Rebuilding the AI Index

The generated database and index files are excluded from the Git repository. To recreate them on a new computer, follow these steps:

1. Clone the repository.
2. Install the backend dependencies.
3. Activate the Python virtual environment.
4. Run `python generate_tickets.py` from the `backend` directory.
5. Run `python build_index.py` from the same directory.
6. Start the backend with `uvicorn main:app --reload`.
7. Start the frontend with `npm start` from the `frontend` directory.

The index-building process downloads or loads the required Sentence Transformers model. The first run may take longer because the model needs to be downloaded.

## Troubleshooting

### Backend is not starting

Check that the Python virtual environment is activated and that the dependencies are installed.

### The frontend cannot load tickets

Make sure the backend is running at `http://127.0.0.1:8000`.

### Similarity search is unavailable

Make sure you have generated the database, built the FAISS index, and started the backend with all required files present.

If you change the ticket dataset, rebuild the index using:

```bash
python build_index.py
```

### Frontend dependencies are missing

Run the following command from the `frontend` directory:

```bash
npm install
```

## License

This project is distributed under the license included in the repository. See the `LICENSE` file for details.
