# ai/local_model_runner.py

from llama_cpp import Llama
import threading
import ast
import json

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
            self.conversation_history = []
            self.code_context = {}
        except Exception as e:
            print(f"[ERROR] Failed to load model: {e}")
            raise

    def parse_code_context(self, code_str):
        """Parse Python code and extract relevant AST information"""
        try:
            tree = ast.parse(code_str)
            context = {
                'functions': [],
                'classes': [],
                'imports': []
            }
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    context['functions'].append({
                        'name': node.name,
                        'lineno': node.lineno
                    })
                elif isinstance(node, ast.ClassDef):
                    context['classes'].append({
                        'name': node.name,
                        'lineno': node.lineno
                    })
                elif isinstance(node, ast.Import):
                    for name in node.names:
                        context['imports'].append(name.name)
                elif isinstance(node, ast.ImportFrom):
                    context['imports'].append(f"{node.module}.{node.names[0].name}")
            
            return context
        except Exception as e:
            return {'error': str(e)}

    def add_code_context(self, filename, code):
        """Add or update code context for a file"""
        self.code_context[filename] = self.parse_code_context(code)

    def format_conversation_context(self):
        """Format conversation and code context for the model"""
        context = "Previous conversation:\n"
        for qa in self.conversation_history[-3:]:  # Keep last 3 exchanges for context
            context += f"User: {qa['question']}\nAssistant: {qa['answer']}\n\n"
        
        if self.code_context:
            context += "\nCode context:\n"
            for filename, ctx in self.code_context.items():
                context += f"\nFile: {filename}\n"
                context += json.dumps(ctx, indent=2) + "\n"
        
        return context

    def ask(self, prompt, system_prompt="You are an expert programming assistant. You help with code generation, explanation, and debugging.", code_context=None):
        if code_context:
            self.add_code_context(code_context['filename'], code_context['code'])

        with self.lock:
            try:
                # Combine conversation history, code context, and current prompt
                context = self.format_conversation_context()
                full_prompt = f"{context}\nCurrent question: {prompt}"
                
                result = self.llm(
                    f"{system_prompt}\n\n{full_prompt}",
                    max_tokens=512,
                    temperature=0.7,
                    echo=True
                )
                
                response = result["choices"][0]["text"].strip()
                
                # Store the Q&A pair in conversation history
                self.conversation_history.append({
                    'question': prompt,
                    'answer': response
                })
                
                return response
            except Exception as e:
                return f"[ERROR] Failed to run inference: {e}"

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        self.code_context = {}

# Example usage
if __name__ == "__main__":
    runner = LocalModelRunner()
    
    # Example with code context
    code_context = {
        'filename': 'example.py',
        'code': '''
def calculate_sum(a, b):
    return a + b
        '''
    }
    
    # First question
    response = runner.ask("How can I modify this function to handle multiple numbers?", 
                         code_context=code_context)
    print("\nAI Response 1:\n", response)
    
    # Follow-up question (will include previous context)
    response = runner.ask("Can you add input validation to the function?")
    print("\nAI Response 2:\n", response)
