from pydantic import BaseModel


class JobOut(BaseModel):
    id: int
    keyword_set_id: int
    job_data: str

    class Config:
        from_attributes = True
