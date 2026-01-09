# Auto-Repair Build System

This is a system that automatically fixes broken Python code. It detects errors and tries to fix them up to 3 times.

## What it does

- Upload a broken Python file
- System runs it and detects errors
- Reads a template file (fixed.py) and applies the fix
- Retries up to 3 times
- Shows you the results

## How it works

It uses a "mock AI" approach. Instead of calling expensive APIs, it just reads a pre-made fixed.py file and replaces the broken code with it.

## Project Structure

```
backend/     - Python FastAPI server
frontend/    - HTML interface
upload/    - stores the broken.py and extra_error.py file
```

## Quick Start

1. Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Create fixed.py in backend folder:
```python
print("Hello World")
```

3. Run the backend:
```bash
uvicorn main:app --reload
```

4. Open frontend/index.html in your browser

5. Upload broken.py and click Run

## Requirements

- Python 3.7+
- Modern web browser

## Notes

- Backend runs on http://localhost:8000
- Maximum 3 retry attempts
- Only works with Python files (.py)

Made as a learning project for understanding self-healing systems.
