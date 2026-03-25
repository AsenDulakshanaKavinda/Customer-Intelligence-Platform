from pydantic import BaseModel

# routes auth
class UserCreate(BaseModel):
    username: str
    password: str

# routes chat
class QuestionPayload(BaseModel):
    question: str
    user_id: str