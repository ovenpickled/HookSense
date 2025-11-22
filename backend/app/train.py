import json
from .collector import DataCollector
import openai
import os

def prepare_training_data():
    collector = DataCollector()
    raw_data = collector.get_dataset()
    
    training_data = []
    for entry in raw_data:
        if entry.get("feedback") and entry["feedback"].get("rating", 0) >= 4:
            # Only use high-quality reviews
            training_data.append({
                "messages": [
                    {"role": "system", "content": "You are an expert code reviewer."},
                    {"role": "user", "content": f"Review this diff:\n{entry['diff']}"},
                    {"role": "assistant", "content": json.dumps(entry['review'])}
                ]
            })
            
    with open("data/fine_tuning/training_data.jsonl", "w") as f:
        for item in training_data:
            f.write(json.dumps(item) + "\n")
            
    return "data/fine_tuning/training_data.jsonl"

def start_finetuning_job(file_path: str):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Upload file
    file = client.files.create(
        file=open(file_path, "rb"),
        purpose="fine-tune"
    )
    
    # Create job
    job = client.fine_tuning.jobs.create(
        training_file=file.id,
        model="gpt-3.5-turbo"
    )
    
    print(f"Fine-tuning job started: {job.id}")

if __name__ == "__main__":
    print("Preparing data...")
    file_path = prepare_training_data()
    print(f"Data saved to {file_path}")
    
    # Uncomment to actually run
    # start_finetuning_job(file_path)
