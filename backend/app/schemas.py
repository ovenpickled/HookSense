from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime

class ReviewBase(BaseModel):
    status: str
    summary: Optional[str] = None
    suggestions: Optional[List[Any]] = None

class ReviewCreate(ReviewBase):
    pull_request_id: int

class Review(ReviewBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class PullRequestBase(BaseModel):
    pr_number: int
    title: str
    description: Optional[str] = None
    status: str

class PullRequestCreate(PullRequestBase):
    repository_id: int

class PullRequest(PullRequestBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    reviews: List[Review] = []

    class Config:
        orm_mode = True

class RepositoryBase(BaseModel):
    name: str
    owner: str
    url: str
    platform: str = "github"

class RepositoryCreate(RepositoryBase):
    pass

class Repository(RepositoryBase):
    id: int
    created_at: datetime
    pull_requests: List[PullRequest] = []

    class Config:
        orm_mode = True
