from pydantic import BaseModel
from typing import List, Optional

class Message(BaseModel):
    text: str
    session: str

class ChatHistory(BaseModel):
    messages: List[Message]

class ChatRequest(BaseModel):
    input: str
    history: Optional[ChatHistory]

class ChatResponse(BaseModel):
    output: str
    intermediate_steps: list[str]


class Document(BaseModel):
    content: str
    metadata: Optional[dict]