# ai/local_model_runner.py

from pathlib import Path
from llama_cpp import Llama
import threading

class LocalModelRunner:
    def __init__(self, model_name="llama-2-7b-chat.gguf", max_tokens=512):
        base_path = Path(__file__).resolve().parent
        self.model_path = base_path / "models" / model_name

        if not self.model_path.exists():
            raise FileNotFoundError(f"Model not found at: {self.model_path}")

        print(f"[LLM] Loading model from {self.model_path}")
        self.llm = Llama(
            model_path=str(self.model_path),
            n_ctx=2048,
            n_threads=8,  # Adjust based on your CPU
            n_gpu_layers=33,  # Set > 0 if using GPU via llama-cpp built with CUDA
            verbose=False
        )
        self.lock = threading.Lock()

    def ask(self, prompt, system_prompt="You are a helpful assistant."):
        with self.lock:
            try:
                result = self.llm(
                    f"{system_prompt}\n\n{prompt}",
                    max_tokens=512,
                    stop=["</s>"]
                )
                return result["choices"][0]["text"].strip()
            except Exception as e:
                return f"[ERROR] Failed to run inference: {e}"

# Example usage
if __name__ == "__main__":
    runner = LocalModelRunner()
    prompt = "Explain what a binary search tree is."
    response = runner.ask(prompt)
    print("\nAI Response:\n", response)
