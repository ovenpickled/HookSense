import httpx
import os
from typing import Dict, Any, List

class GitHubClient:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json"
        }

    async def get_pr_diff(self, owner: str, repo: str, pr_number: int) -> str:
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}"
        headers = self.headers.copy()
        headers["Accept"] = "application/vnd.github.v3.diff"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.text

    async def post_comment(self, owner: str, repo: str, pr_number: int, body: str):
        url = f"{self.base_url}/repos/{owner}/{repo}/issues/{pr_number}/comments"
        data = {"body": body}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()

    async def post_review_comment(self, owner: str, repo: str, pr_number: int, body: str, commit_id: str, path: str, line: int):
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}/comments"
        data = {
            "body": body,
            "commit_id": commit_id,
            "path": path,
            "line": line,
            "side": "RIGHT"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
