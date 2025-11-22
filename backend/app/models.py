from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Repository(Base):
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    owner = Column(String, index=True)
    url = Column(String)
    platform = Column(String, default="github") # github, gitlab, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    pull_requests = relationship("PullRequest", back_populates="repository")

class PullRequest(Base):
    __tablename__ = "pull_requests"

    id = Column(Integer, primary_key=True, index=True)
    repository_id = Column(Integer, ForeignKey("repositories.id"))
    pr_number = Column(Integer)
    title = Column(String)
    description = Column(Text)
    status = Column(String) # open, closed, merged
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    repository = relationship("Repository", back_populates="pull_requests")
    reviews = relationship("Review", back_populates="pull_request")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    pull_request_id = Column(Integer, ForeignKey("pull_requests.id"))
    status = Column(String) # pending, completed, failed
    summary = Column(Text)
    suggestions = Column(JSON) # List of suggestions
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    pull_request = relationship("PullRequest", back_populates="reviews")
