from pydantic import BaseModel, Field
from typing import List, Optional, TypedDict

class AgentState(TypedDict):
    # Input Data
    user_id: str
    query: str
    question: str
    
    # Classification Metadata
    sentiment: Optional[str] 
    topics: List[str] 
    
    # RAG Data
    retrieved_docs: List[str] 
    
    # Output Data
    generated_response: Optional[str] 
    confidence_score: float 
    
    # Control Flags
    is_escalated: bool
    # next_step: str = "triage"  Used by the Router to track progress