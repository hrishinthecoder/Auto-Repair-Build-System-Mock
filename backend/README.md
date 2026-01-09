# Backend - Auto-Repair System

This is the backend server that handles file uploads and runs the auto-repair loop.

## Files

- `main.py` - FastAPI server with all endpoints
- `requirements.txt` - Python packages needed
- `fixed.py` - Template file with correct code 

## Setup

1. Install packages:
```bash
pip install -r requirements.txt
```

2. Create fixed.py:
```python
print("Hello World")
```

3. Run server:
```bash
uvicorn main:app --reload
```

Server starts at http://localhost:8000

## API Endpoints

- `POST /upload` - Upload broken file
- `POST /run` - Start auto-repair process
- `GET /status` - Check current status (for polling)
- `GET /download/{filename}` - Download fixed file

## How it works

1. Receives broken.py from frontend
2. Tries to run it with subprocess
3. If it fails, reads fixed.py
4. Overwrites broken.py with fixed.py content
5. Tries again (max 3 times)
6. Returns result to frontend

## Important

- Make sure fixed.py exists before running
- Backend doesn't call any real AI API
- It's a mock system for learning
