from pydantic import BaseModel
from typing import Literal, List, Optional

class Ticket(BaseModel):
    channel: Literal["email","chat","phone","portal"]
    severity: Literal["low","medium","high","critical"]
    summary: str
    details: Optional[str] = None

class ActionItem(BaseModel):
    id: str
    title: str
    description: str
    owner: Optional[str] = None

class DecisionResponse(BaseModel):
    decision: Literal["ai_code_patch","vibe_workflow"]
    reasoning: str
    checklist: List[ActionItem]
    metadata: Optional[dict] = None
