from fastapi import APIRouter, status, HTTPException, Depends
from pydantic import BaseModel
from app.agents import classification_agent
from app.database import get_session, Feedback
from sqlalchemy.orm import Session
from uuid import uuid4
from app.utils import cfg, get_logger

log = get_logger(__file__)

feedback_route = APIRouter()

@feedback_route.get(path="/health", status_code=status.HTTP_200_OK)
def check_feedback_router():
    """Health check endpoint for the feedback route."""
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
    content: str

    
@feedback_route.post(path="/submit", status_code=status.HTTP_201_CREATED)
def submit_feedback(feedback_payload: FeedbackPayload, db: Session = Depends(get_session)):
    """
    Endpoint to submit user feedback. The feedback is classified using the classification agent and stored in the database.

    args:
    - feedback_payload: A Pydantic model containing the user_id and content of the feedback.
    - db: A database session provided by FastAPI's dependency injection system.
    returns:
    - A JSON response indicating the success of the feedback submission and the classification result.
    exceptions:
    - Raises HTTPException with status code 500 if there is an error during feedback submission or classification.
    """

    feedback_id = str(uuid4())
    user_id = feedback_payload.user_id
    content = feedback_payload.content

    try:
        response = classification_agent.invoke(user_query=feedback_payload.content, thread_id=None) # keep thread_id as None for now, to remove memory
        sentiment = response["structured_response"].sentiment
        topic = response["structured_response"].topic

        log.info(f"Feedback submitted by user {user_id}")

        new_feedback = Feedback(id=feedback_id, user_id=user_id, sentiment=sentiment, topic=topic, content=content)
        db.add(new_feedback)
        db.commit()
        db.refresh(new_feedback)


        return {
            "message": "Feedback submitted successfully",
            "classification_result": "response",
            "status_code": status.HTTP_201_CREATED
        }

    except Exception as e:
        log.error(f"Error submitting feedback: {str(e)}")
        raise HTTPException(
            detail=f"Error submitting feedback: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        