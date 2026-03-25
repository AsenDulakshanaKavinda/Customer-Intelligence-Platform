from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from .schemas import QuestionPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

chat_route = APIRouter(dependencies=[Depends(oauth2_scheme)])


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
def user_question(question_payload: QuestionPayload):
    # todo invoke classification agent here and send the classification result with the payload
    pass