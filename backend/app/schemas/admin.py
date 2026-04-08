from pydantic import BaseModel


class MetricsOut(BaseModel):
    users_count: int
    jobs_count: int
    resumes_count: int
