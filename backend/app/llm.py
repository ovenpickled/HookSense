import os
from typing import List, Dict, Any
import openai
import google.generativeai as genai

class LLMProvider:
    def generate_review(self, code_diff: str, context: str = "") -> Dict[str, Any]:
        raise NotImplementedError

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)

    def generate_review(self, code_diff: str, context: str = "") -> Dict[str, Any]:
        prompt = f"""
        You are an expert code reviewer. Review the following code diff and provide suggestions.
        Context: {context}
        
        Diff:
        {code_diff}
        
        Return a JSON response with a summary and a list of suggestions (file, line, comment).
        """
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "system", "content": "You are a helpful code reviewer."},
                      {"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content

class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_review(self, code_diff: str, context: str = "") -> Dict[str, Any]:
        prompt = f"""
        You are an expert code reviewer. Review the following code diff and provide suggestions.
        Context: {context}
        
        Diff:
        {code_diff}
        
        Return a JSON response with a summary and a list of suggestions (file, line, comment).
        """
        response = self.model.generate_content(prompt)
        return response.text

class LocalLLMProvider(LLMProvider):
    def __init__(self, model_path: str = "models/local_finetuned"):
        try:
            from peft import PeftModel, PeftConfig
            from transformers import AutoModelForCausalLM, AutoTokenizer
            import torch
            
            config = PeftConfig.from_pretrained(model_path)
            base_model = AutoModelForCausalLM.from_pretrained(
                config.base_model_name_or_path,
                return_dict=True,
                load_in_4bit=True,
                device_map='auto'
            )
            self.model = PeftModel.from_pretrained(base_model, model_path)
            self.tokenizer = AutoTokenizer.from_pretrained(config.base_model_name_or_path)
        except Exception as e:
            print(f"Failed to load local model: {e}")
            self.model = None

    def generate_review(self, code_diff: str, context: str = "") -> Dict[str, Any]:
        if not self.model:
            return {"error": "Local model not loaded"}
            
        prompt = f"Review this code:\n{code_diff}\nContext: {context}"
        inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")
        
        outputs = self.model.generate(**inputs, max_new_tokens=200)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

def get_llm_provider() -> LLMProvider:
    openai_key = os.getenv("OPENAI_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    use_local = os.getenv("USE_LOCAL_LLM", "false").lower() == "true"
    
    if use_local:
        return LocalLLMProvider()
    elif openai_key:
        return OpenAIProvider(openai_key)
    elif gemini_key:
        return GeminiProvider(gemini_key)
    else:
        raise ValueError("No LLM provider configured")
