# Aanchal Boutique Support Tickets

A simple customer support ticket dashboard for Aanchal Boutique, built with React and FastAPI. The application retrieves sample customer support tickets from a FastAPI backend and displays them in a responsive table.

## Technologies Used

- React
- JavaScript
- Python
- FastAPI
- Uvicorn

## Project Structure

```text
aanchal-boutique-support/
├── frontend/
├── backend/
│   └── main.py
├── .gitignore
├── LICENSE
└── README.md

## Requirements

Before running the application, install the following:

- Python 3
- Node.js and npm
- Git

## Local Installation and Setup

Follow these steps to run the project on your local computer.

### 1. Clone the Repository

Open a terminal and run:

```bash
git clone https://github.com/areebkhan47/aanchal-boutique-support.git
cd aanchal-boutique-support
```

### 2. Start the FastAPI Backend

Open a terminal in the project root directory.

Navigate to the backend folder:

```bash
cd backend
```

Create a Python virtual environment:

```bash
py -m venv venv
```

Activate the virtual environment in Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use the following alternative in Command Prompt:

```cmd
venv\Scripts\activate.bat
```

Install the backend dependencies:

```bash
python -m pip install fastapi "uvicorn[standard]"
```

Start the FastAPI server:

```bash
python -m uvicorn main:app --reload
```

The backend will run at:

http://127.0.0.1:8000

The available API endpoints are:

- Main endpoint: http://127.0.0.1:8000/
- Tickets endpoint: http://127.0.0.1:8000/api/tickets
- Interactive API documentation: http://127.0.0.1:8000/docs

Keep this terminal running while using the application.

### 3. Start the React Frontend

Open a second terminal in your project root directory.

Navigate to the frontend folder:

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

The frontend will be available at:

http://localhost:3000

Keep the frontend terminal running as well.

### 4. Use the Application

Open your browser and visit:

http://localhost:3000

The dashboard will request ticket data from the FastAPI backend and display the tickets in a table.
