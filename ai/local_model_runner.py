# ai/local_model_runner.py

from pathlib import Path
from llama_cpp import Llama
import threading

class LocalModelRunner:
    def __init__(self, model_name="codellama-7b-instruct.Q2_K.gguf", max_tokens=512):
        base_path = Path(__file__).resolve().parent
        self.model_path = base_path / "models" / model_name

        if not self.model_path.exists():
            raise FileNotFoundError(f"Model not found at: {self.model_path}")

        print(f"[LLM] Loading model from {self.model_path}")
        self.llm = Llama.from_pretrained(
            repo_id="TheBloke/CodeLlama-7B-Instruct-GGUF",
            filename=model_name,
            n_ctx=4096,
            n_threads=8,
            n_gpu_layers=33,
            verbose=False
        )
        self.lock = threading.Lock()

    def ask(self, prompt, system_prompt="You are an expert programming assistant. You help with code generation, explanation, and debugging."):
        with self.lock:
            try:
                result = self.llm(
                    f"{system_prompt}\n\n{prompt}",
                    max_tokens=512,
                    temperature=0.7,
                    echo=True  # This will include the prompt in the response
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
