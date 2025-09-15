import subprocess
import sys
import os
from datetime import datetime

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    print(log_entry.strip())
    with open("startup.log", "a", encoding="utf-8") as f:
        f.write(log_entry)

def main():
    log_message("Starting Nephrology Backend Service...")
    log_message(f"Python version: {sys.version}")
    log_message(f"Current directory: {os.getcwd()}")
    
    # Check if required files exist
    required_files = ["nephro_api.py", ".env", "requirements.txt"]
    for file in required_files:
        if os.path.exists(file):
            log_message(f"✓ Found {file}")
        else:
            log_message(f"✗ Missing {file}")
    
    # Install dependencies
    log_message("Installing dependencies...")
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                              capture_output=True, text=True, timeout=300)
        log_message(f"Pip install exit code: {result.returncode}")
        if result.stdout:
            log_message(f"Pip stdout: {result.stdout[:500]}...")
        if result.stderr:
            log_message(f"Pip stderr: {result.stderr[:500]}...")
    except Exception as e:
        log_message(f"Error installing dependencies: {e}")
    
    # Start the server
    log_message("Starting the API server...")
    try:
        # Import and run the server
        import uvicorn
        log_message("Uvicorn imported successfully")
        log_message("Server will be available at: http://localhost:8002")
        log_message("API Documentation: http://localhost:8002/docs")
        
        # Import the app
        sys.path.insert(0, os.getcwd())
        from nephro_api import app
        log_message("App imported successfully")
        
        uvicorn.run(app, host="0.0.0.0", port=8002, log_level="info")
        
    except Exception as e:
        log_message(f"Error starting server: {e}")
        import traceback
        log_message(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    main()