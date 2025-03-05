from fastapi import APIRouter, HTTPException
from leak_lock_ai.services.chat_service import get_chatgpt_response
from pydantic import BaseModel

router = APIRouter()

# Request model
class ChatRequest(BaseModel):
    prompt: str  # User's query

@router.post("/chat-query")
def chat_with_context(request: ChatRequest):
    try:
        response = get_chatgpt_response(request.prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
