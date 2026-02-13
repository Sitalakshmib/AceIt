
from fastapi import FastAPI
from routes import coding
import uvicorn

app = FastAPI()
app.include_router(coding.router, prefix="/coding")

print("Starting main_test.py on port 8000...")

if __name__ == "__main__":
    uvicorn.run(app, port=8003)
