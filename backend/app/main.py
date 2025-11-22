from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .worker import process_review
import os

app = FastAPI(title="AI Code Reviewer API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Code Reviewer API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/webhook")
async def webhook(request: Request):
    payload = await request.json()
    event = request.headers.get("X-GitHub-Event")

    if event == "pull_request":
        action = payload.get("action")
        if action in ["opened", "synchronize"]:
            pr = payload.get("pull_request")
            repo = payload.get("repository")
            installation = payload.get("installation")
            
            if pr and repo:
                process_review.delay(
                    owner=repo["owner"]["login"],
                    repo=repo["name"],
                    pr_number=pr["number"],
                    installation_id=installation["id"] if installation else 0
                )
                return {"message": "Review processing started"}
    
from .collector import DataCollector
from pydantic import BaseModel

# ... existing imports

class Feedback(BaseModel):
    review_id: str
    rating: int # 1-5
    comment: str

collector = DataCollector()

@app.post("/feedback")
def submit_feedback(feedback: Feedback):
    # In a real app, we'd link this to the specific review in DB
    # For now, we just log it
    collector.save_interaction(code_diff="<lookup_diff>", review={"id": feedback.review_id}, feedback=feedback.dict())
    return {"message": "Feedback received"}


from sqlalchemy.orm import Session
from fastapi import Depends
from .database import get_db
from .models import Review, PullRequest as PRModel

@app.get("/metrics")
def get_metrics(db: Session = Depends(get_db)):
    total_reviews = db.query(Review).count()
    # Simplified issues count (assuming JSON suggestions list)
    # In real app, we'd query inside the JSON or have a separate counter
    issues_found = 0 
    reviews = db.query(Review).all()
    for r in reviews:
        if r.suggestions:
            issues_found += len(r.suggestions)
            
    return {
        "total_reviews": total_reviews,
        "issues_found": issues_found,
        "avg_review_time": "1.2s" # Placeholder for now
    }

@app.get("/reviews")
def get_recent_reviews(limit: int = 5, db: Session = Depends(get_db)):
    reviews = db.query(Review).order_by(Review.created_at.desc()).limit(limit).all()
    result = []
    for r in reviews:
        result.append({
            "repository": r.pull_request.repository.name if r.pull_request and r.pull_request.repository else "unknown",
            "pr_number": r.pull_request.pr_number if r.pull_request else 0,
            "status": r.status,
            "date": r.created_at.strftime("%Y-%m-%d")
        })
    return result
