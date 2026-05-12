from fastapi import APIRouter, HTTPException
from app.models.chat import ChatRequest, ChatResponse
from app.services.chat_service import process_chat_message
from app.services.intent_service import classify_intent

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        answer = process_chat_message(request.question)
        intent = classify_intent(request.question)
        return ChatResponse(answer=answer, intent=intent)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
