from fastapi import APIRouter, status, HTTPException
from app.agents import classification_agent

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

@chat_route.post("/question")
def user_question():
    # todo invoke classification agent here and send the classification result with the payload
    pass