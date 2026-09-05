from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

class Evidence(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    timestamp:str
    speaker:str
    quote:str

class DiscussionPoint(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    topic: str
    details: list[str]
    evidence: list[Evidence]

class Takeaway(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    takeaway: str
    evidence: list[Evidence]

class Decision(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    decision: str
    evidence: list[Evidence]


class ActionItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    action: str
    
    owner: str | None = Field(
        default=None, 
        description="only include a owner when explicitly supported"
    )

    due_date: str | None = Field(
        default=None,
        description="only include due date when explicitly supported"
    )

    status: Literal[
        "committed",
        "supported",
        "proposed"
    ]

    evidence: list[Evidence]

class MeetingAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    summary: str = Field(
    description=(
        "Concise factual overview of the meeting, including the main "
        "topics discussed and key outcomes. Do not introduce information "
        "that is not supported by the transcript."
        )
    )

    discussion_pts: list[DiscussionPoint]
    take_aways: list[Takeaway]
    decisions: list[Decision]
    action_items: list[ActionItem]
    unresolved_items: list[str]