import sys
print(f"Python version: {sys.version}")
print("Python is working correctly!")

try:
    import fastapi
    print("FastAPI is installed")
except ImportError:
    print("FastAPI is NOT installed - need to install dependencies")

try:
    import uvicorn
    print("Uvicorn is installed")
except ImportError:
    print("Uvicorn is NOT installed - need to install dependencies")

print("Test completed.")
input("Press Enter to continue...")