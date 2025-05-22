# ai/local_model_runner.py

from pathlib import Path
from llama_cpp import Llama
import threading

class LocalModelRunner:
    def __init__(self, model_name="codellama-7b-instruct.Q2_K.gguf", max_tokens=512):
        print(f"[LLM] Loading model {model_name} from TheBloke/CodeLlama-7B-Instruct-GGUF")
        try:
            self.llm = Llama.from_pretrained(
                repo_id="TheBloke/CodeLlama-7B-Instruct-GGUF",
                filename=model_name,
                n_ctx=4096,
                n_threads=8,
                n_gpu_layers=33,
                verbose=True  # Set to True temporarily to see download progress
            )
            self.lock = threading.Lock()
        except Exception as e:
            print(f"[ERROR] Failed to load model: {e}")
            raise

    def ask(self, prompt, system_prompt="You are an expert programming assistant. You help with code generation, explanation, and debugging."):
        with self.lock:
            try:
                result = self.llm(
                    f"{system_prompt}\n\n{prompt}",
                    max_tokens=512,
                    temperature=0.7,
                    echo=True
                )
                return result["choices"][0]["text"].strip()
            except Exception as e:
                return f"[ERROR] Failed to run inference: {e}"

# Example usage
if __name__ == "__main__":
    runner = LocalModelRunner()
    prompt = "Write a Python function that implements a binary search tree insertion."
    response = runner.ask(prompt)
    print("\nAI Response:\n", response)
