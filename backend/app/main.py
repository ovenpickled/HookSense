from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
from .worker import process_review
import os

app = FastAPI(title="AI Code Reviewer API")

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


