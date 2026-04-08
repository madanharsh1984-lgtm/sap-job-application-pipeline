from pydantic import BaseModel


class JobOut(BaseModel):
    id: int
    keyword_group: str
    job_data: str

    class Config:
        from_attributes = True
