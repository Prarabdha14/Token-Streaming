import asyncio
import os
from dotenv import load_dotenv
import google.generativeai as genai
from app.core.state import get_generation_status, remove_generation

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

async def generate_tokens(generation_id: str, prompt: str):
    """"
    A generator function that streams tokens from Google Gemini API.
    It checks the generation status to see if it should stop.
    """
    try:
        response = await model.generate_content_async(prompt, stream=True)
        
        async for chunk in response:
            if chunk.text:
                words = chunk.text.split(" ")
                for word in words:
                    is_active = get_generation_status(generation_id)
                    if not is_active:
                        yield "\n\n[Generation stopped by user via stop button.]"
                        return 
                        
                    yield word + " "
                    await asyncio.sleep(0.05)
                
    except asyncio.CancelledError:
        pass
    except Exception as e:
        yield f"\n\n[Error occurred during generation: {str(e)}]"
    finally:
        remove_generation(generation_id)
