from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.services.ai_service import generate_tokens
from app.core.state import set_generation_status, get_generation_status

router = APIRouter()

@router.get("/generate/{generation_id}")
async def generate(generation_id: str, prompt: str = "Hello AI"):
    """
    Streaming endpoint that uses generator and yield to stream tokens.
    Can be tested in Postman using the provided generation_id.
    """
    set_generation_status(generation_id, True)

    # Return the generator directly as a StreamingResponse
    return StreamingResponse(
        generate_tokens(generation_id, prompt), 
        media_type="text/event-stream"
    )

@router.post("/stop/{generation_id}")
async def stop_generation(generation_id: str):
    """
    Stop endpoint acts as the "Stop Button" logic.
    Changes the internal state, causing the generator to halt early.
    """
    if get_generation_status(generation_id) is False:
        raise HTTPException(status_code=404, detail="Generation ID not found or already stopped.")
    
    set_generation_status(generation_id, False)
    
    return {"status": "success", "message": f"Generation {generation_id} stopped."}
