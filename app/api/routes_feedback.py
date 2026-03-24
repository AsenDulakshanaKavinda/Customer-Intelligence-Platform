from fastapi import APIRouter, status, HTTPException, Depends
from pydantic import BaseModel
from app.agents import classification_agent
from app.database import get_session, Feedback
from sqlalchemy.orm import Session

from app.utils import cfg, get_logger

log = get_logger(__file__)

feedback_route = APIRouter()

@feedback_route.get(path="/health", status_code=status.HTTP_200_OK)
def check_feedback_router():
    log.info("Health checking feedback route")
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
    user_id: str
    sentiment: str
    topic: str
    content: str

    
@feedback_route.post(path="/submit", status_code=status.HTTP_201_CREATED)
async def submit_feedback(feedback_payload: FeedbackPayload):
    # todo receive the feedback and store it in the database, 
    # then invoke the classification agent to classify the feedback and store the classification result in the database
    try:
        response = await classification_agent.invoke(feedback_payload.content)
        log.info(f"Feedback submitted by user {feedback_payload.user_id}")

        new_feedback = Feedback(id="test_id_01", user_id=feedback_payload.user_id, sentiment=response["sentiment"], topic=response["topic"], content=feedback_payload.content)
        db: Session = Depends(get_session)
        db.add(new_feedback)
        db.commit()
        db.refresh(new_feedback)


        return {
            "message": "Feedback submitted successfully",
            "classification_result": response,
            "status_code": status.HTTP_201_CREATED
        }

    except Exception as e:
        log.error(f"Error submitting feedback: {str(e)}")
        raise HTTPException(
            detail=f"Error submitting feedback: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        