from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel

chat_route = APIRouter()

@chat_route.get("/health")
def check_chat_router():
    try:
        return {
            "message": f"Chat route running...",
            "status_code": status.HTTP_200_OK
        }
    except Exception as e:
        raise HTTPException(
            detail=f"Error in chat route: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

class QuestionPayload(BaseModel):
    question: str
    user_id: str

@chat_route.post("/question")
def user_question(question_payload: QuestionPayload):
    # todo invoke classification agent here and send the classification result with the payload
    pass