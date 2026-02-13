
import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'aceit_backend'))

from fastapi import FastAPI
# from routes import coding
import uvicorn

# We need to import coding after setting up path
from routes import coding

app = FastAPI()
app.include_router(coding.router, prefix="/coding")

print("Starting minimal test server on port 8003...")

if __name__ == "__main__":
    uvicorn.run(app, port=8003)
