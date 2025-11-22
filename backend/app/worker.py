
from celery import Celery
import os
import asyncio
from .llm import get_llm_provider
from .github_service import GitHubClient
from .analysis import CodeAnalyzer

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

celery = Celery(__name__, broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

@celery.task(name="process_review")
def process_review(owner: str, repo: str, pr_number: int, installation_id: int):
    # In a real app, we'd fetch the installation token using the installation_id
    # For now, we assume a global token or env var
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("No GITHUB_TOKEN found")
        return

    client = GitHubClient(token)
    llm = get_llm_provider()
    analyzer = CodeAnalyzer()

    # Run async code in sync Celery task
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        diff = loop.run_until_complete(client.get_pr_diff(owner, repo, pr_number))
        
        # Analyze code (simplified, just passing diff for now)
        # In reality, we'd fetch files and analyze them
        
        review_result = llm.generate_review(diff)
        
        # Post comment
        summary = f"## AI Code Review\n\n{review_result}"
        loop.run_until_complete(client.post_comment(owner, repo, pr_number, summary))
        
    except Exception as e:
        print(f"Error processing review: {e}")

