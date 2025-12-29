# AceIt - Interview Practice Platform

## Project Structure
- **Backend**: FastAPI (Python) located in `aceit-backend`
- **Frontend**: React (Vite) located in `aceit-frontend`

## Prerequisites
- Python 3.8+
- Node.js & npm
- PostgreSQL (for database)

## Setup

### 1. Backend Setup
```powershell
cd aceit-backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```
*Note: Make sure your database configuration (PostgreSQL) is correct in `database_postgres.py` or `.env`.*

### 2. Frontend Setup
```powershell
cd aceit-frontend
npm install
```

## Running the Project

The easiest way to run the project on Windows is to use the provided batch script:

```powershell
.\start_servers.bat
```

This will automatically:
1. Start the backend server on `http://localhost:8001`
2. Start the frontend server on `http://localhost:5173`

### Manual Run
If you prefer to run them separately:

**Backend:**
```powershell
cd aceit-backend
.\venv\Scripts\activate
uvicorn main:app --reload --port 8001
```

**Frontend:**
```powershell
cd aceit-frontend
npm run dev
```
