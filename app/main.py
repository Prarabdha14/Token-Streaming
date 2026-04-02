from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="AI Streaming Service",
    description="A service that streams tokens using yield and generators, and supports stopping the stream mid-way.",
    version="1.0.0"
)

# Register API router
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Token Streamer! Use /generate/{generation_id} to test."}
