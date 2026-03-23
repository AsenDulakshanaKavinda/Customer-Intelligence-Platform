from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel

from app.agents import classification_agent

feedback_route = APIRouter()

@feedback_route.get("/health")
def check_feedback_router():
    try:
        return {
            "message": f"Feedback route running...",
            "status_code": status.HTTP_200_OK
        }
    except Exception as e:
        raise HTTPException(
            detail=f"Error in feedback route: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

class FeedbackPayload(BaseModel):
    consent: str
    user_id: str

@feedback_route.post("/submit")
async def submit_feedback(feedback_payload: FeedbackPayload):
    # todo receive the feedback and store it in the database, then invoke the classification agent to classify the feedback and store the classification result in the database
    try:
        response = await classification_agent.invoke(feedback_payload.consent)

    except Exception as e:
        raise RuntimeError(f"Error in submit feedback: {str(e)}")