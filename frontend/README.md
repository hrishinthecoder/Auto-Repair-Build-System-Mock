# Frontend - Auto-Repair System

This is the web interface where you upload files and see the repair process.

## Files

- `index.html` - Main interface 

## How to use

1. Make sure backend is running first
2. Open index.html in your browser
3. Click "Choose File" and select a broken .py file
4. Click "Run" button
5. Watch the timeline update in real-time
6. See the final result

## Features

- File upload interface
- Live timeline showing repair progress
- Color-coded status (Blue → Red → Yellow → Green)
- Retry counter with progress bars
- Code preview section
- Download button for fixed file

## What you see

- 🚀 Blue = Building/Starting
- ❌ Red = Error detected
- 🧠 Yellow = AI fixing
- ✅ Green = Success

## Testing

Create a broken.py file:
```python
print("Hello World
```
(missing closing quote)

Upload it and watch it get fixed!

## Notes

- Frontend polls backend every 2 seconds
- Shows maximum 3 retry attempts
- Only accepts .py files 
- Needs backend running on localhost:8000
