import json
import os
from datetime import datetime
from typing import Dict, Any

class DataCollector:
    def __init__(self, data_dir: str = "data/fine_tuning"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        self.file_path = os.path.join(data_dir, "reviews.jsonl")

    def save_interaction(self, code_diff: str, review: Dict[str, Any], feedback: Dict[str, Any] = None):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "diff": code_diff,
            "review": review,
            "feedback": feedback
        }
        
        with open(self.file_path, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def get_dataset(self):
        dataset = []
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                for line in f:
                    dataset.append(json.loads(line))
        return dataset
