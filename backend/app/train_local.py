import os
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer
from datasets import load_dataset

def train_local_model(
    base_model_id: str = "codellama/CodeLlama-7b-hf",
    data_path: str = "data/fine_tuning/training_data.jsonl",
    output_dir: str = "models/local_finetuned"
):
    print(f"Starting local fine-tuning of {base_model_id}...")
    
    # 1. Load Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(base_model_id)
    tokenizer.pad_token = tokenizer.eos_token
    
    # 2. Load Base Model with QLoRA config
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
    )
    
    model = AutoModelForCausalLM.from_pretrained(
        base_model_id,
        quantization_config=bnb_config,
        device_map="auto"
    )
    
    model = prepare_model_for_kbit_training(model)
    
    # 3. LoRA Config
    peft_config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "v_proj"] # Adjust based on model architecture
    )
    
    model = get_peft_model(model, peft_config)
    
    # 4. Load Data
    dataset = load_dataset("json", data_files=data_path, split="train")
    
    # 5. Training Arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        logging_steps=10,
        max_steps=100, # Short run for demo
        optim="paged_adamw_8bit",
        fp16=True,
    )
    
    # 6. Trainer
    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        dataset_text_field="messages", # Needs formatting adapter for chat format
        max_seq_length=512,
        tokenizer=tokenizer,
        args=training_args,
    )
    
    trainer.train()
    
    # 7. Save Model
    trainer.model.save_pretrained(output_dir)
    print(f"Model saved to {output_dir}")

if __name__ == "__main__":
    # Ensure data exists
    if not os.path.exists("data/fine_tuning/training_data.jsonl"):
        print("No training data found. Run collector first.")
    else:
        train_local_model()
