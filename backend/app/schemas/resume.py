from pydantic import BaseModel


class ResumeCreate(BaseModel):
    content: str
