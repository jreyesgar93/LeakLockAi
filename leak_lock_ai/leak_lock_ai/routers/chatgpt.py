from fastapi import APIRouter, HTTPException
from leak_lock_ai.services.chatgpt_service import get_chatgpt_response
from pydantic import BaseModel

router = APIRouter()

# Request model
class ChatGPTRequest(BaseModel):
    feature: str  # User's query

@router.post("/chatpgt-features")
def chat_with_context(request: ChatGPTRequest):
    try:
        response = get_chatgpt_response(request.feature)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
