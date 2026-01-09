from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import subprocess  # REQUIRED: To run the Python scripts
import tempfile    # REQUIRED: To create safe temporary files
import os          # REQUIRED: To access the hard drive

app = FastAPI()

# --- 1. CONFIGURATION ---
# This allows your HTML frontend to talk to this Python backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. GLOBAL STORAGE ---
# 'current_status': Updates the frontend timeline/progress bar.
# 'stored_files': Holds uploaded file content in RAM.
current_status = {"status": "IDLE", "retries": 0, "message": "", "timeline": []}
stored_files = {} 

# --- 3. AI SIMULATION LOGIC ---
def fake_ai(error_message: str):
    """
    Analyzes the error. 
    If it's a parenthesis error, it reads 'fixed.py' from your HARD DRIVE.
    If it's a colon error, it returns None.
    """
    # Check if the error is about missing brackets.
    # We check two phrases to support different Python versions.
    is_parenthesis_error = "unexpected EOF" in error_message or "was never closed" in error_message

    if is_parenthesis_error:
        # --- CRITICAL SECTION: READING LOCAL FILE ---
        # We check if 'fixed.py' exists in the same folder as main.py.
        if os.path.exists("fixed.py"):
            print("LOG: Found fixed.py on disk. Reading content...")
            
            # 'open' reads the file from your local computer's disk.
            with open("fixed.py", "r") as f:
                return f.read()
        else:
            print("⚠️ ERROR: 'fixed.py' is missing from the backend folder!")
    
    # If the error is not about parentheses, return None.
    return None

# --- 4. MAIN RETRY LOOP ---
def run_with_retry(filename, file_content):
    global current_status
    retries = 0
    max_retries = 3
    current_status["timeline"] = []
    
    # Keep the original code safe in case we fail and need to revert.
    original_code = file_content 
    current_code = file_content 

    # Loop infinitely until we hit 'break' or 'return'
    while True:
        attempt_number = retries + 1
        current_status["status"] = "BUILDING"
        current_status["timeline"].append(f"🚀 Attempt {attempt_number}: Running Build...")

        # Create a temporary file to safely run the code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(current_code)
            temp_filename = temp_file.name
        
        try:
            # --- CRITICAL SECTION: EXECUTION ---
            # subprocess.run executes the temporary python file.
            # capture_output=True: Grabs what would be printed to the screen.
            # text=True: Ensures the output is text, not bytes.
            result = subprocess.run(
                ['python', temp_filename], 
                capture_output=True, 
                text=True
            )
            
            # --- SUCCESS PATH ---
            if result.returncode == 0:
                current_status["status"] = "SUCCESS"
                current_status["retries"] = retries
                current_status["timeline"].append(f"✅ Success on attempt {attempt_number}!")
                
                # Update memory with the working code
                stored_files[filename] = current_code 
                
                return {
                    "status": "SUCCESS", 
                    "retries": retries, 
                    "output": result.stdout, 
                    "code": current_code, 
                    "timeline": current_status["timeline"]
                }
            
            # --- FAILURE PATH ---
            else:
                current_status["timeline"].append(f"❌ Attempt {attempt_number} Failed: Syntax Error")
                
                # 1. Check if we ran out of retries
                if retries >= max_retries:
                    break # Exit the loop immediately

                # 2. Ask "AI" for help
                current_status["status"] = "FIXING"
                current_status["timeline"].append(f"🧠 AI Analyzing Error (Retry {retries + 1})...")
                
                # We pass the stderr (Error Message) to the AI function
                suggested_fix = fake_ai(result.stderr)
                
                if suggested_fix:
                    current_code = suggested_fix
                    current_status["timeline"].append("✨ AI: Found 'fixed.py' on disk. Applying fix...")
                else:
                    # Provide helpful logs for why it failed
                    if not os.path.exists("fixed.py"):
                        current_status["timeline"].append("⚠️ AI Error: 'fixed.py' is missing from the folder!")
                    elif "unexpected EOF" not in result.stderr and "was never closed" not in result.stderr:
                        current_status["timeline"].append("⚠️ AI: Error type doesn't match 'fixed.py' template.")
                    else:
                        current_status["timeline"].append("⚠️ AI: No solution found.")
                
                retries += 1 

        finally:
            # Clean up: Always delete the temp file so we don't clog the disk
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)

    # --- FINAL ERROR BLOCK (After 3 Retries) ---
    current_status["status"] = "ERROR"
    current_status["retries"] = retries
    current_status["message"] = "Maximum retries reached. Cannot fix automatically."
    current_status["timeline"].append("🚫 Final: Maximum retries reached. Reverting to original.")
    
    # IMPORTANT: Revert to original code so the user doesn't download a bad fix
    stored_files[filename] = original_code
    
    return {
        "status": "ERROR", 
        "retries": retries, 
        "code": original_code, 
        "message": current_status["message"], 
        "timeline": current_status["timeline"]
    }

# --- 5. API ENDPOINTS ---

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Read the uploaded file into memory
    content = await file.read()
    stored_files[file.filename] = content.decode('utf-8')
    return {"message": "Uploaded", "filename": file.filename}

@app.post("/run")
async def run_repair(filename: str):
    # Check if we have the file in memory
    if filename not in stored_files:
        return {"status": "ERROR", "message": "File not found"}
    # Start the retry loop
    return run_with_retry(filename, stored_files[filename])

@app.get("/status")
async def get_status():
    # Frontend polls this to update the UI
    return current_status

@app.get("/download/{filename}")
async def download_file(filename: str):
    # Allows the user to download the final result
    if filename not in stored_files:
        return {"status": "ERROR", "message": "File not found"}
    
    return Response(
        content=stored_files[filename],
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

# Test endpoint to check if API is running
@app.get("/")
async def root():
    return {"message": "Auto-Repair System API is running"}