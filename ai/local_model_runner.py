# ai/local_model_runner.py

from llama_cpp import Llama
import threading
import ast
import json
import datetime
# Import moved to __init__ where it's actually used

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
                verbose=True
            )
            self.lock = threading.Lock()
            self.conversation_history = []
            self.code_context = {}
            self.user_patterns = {
                'coding_style': {},
                'common_patterns': {},
                'preferred_libraries': set(),
                'feedback_history': [],  # Track user feedback
                'interaction_metrics': {
                    'suggestions_accepted': 0,
                    'suggestions_rejected': 0,
                    'common_issues': {}
                }
            }
            self.learning_history = []
            # Initialize conversation model
            from .conversation_model import ConversationModel
            self.conversation_model = ConversationModel()
        except Exception as e:
            print(f"[ERROR] Failed to load model: {e}")
            raise

    def parse_code_context(self, code_str):
        """Parse Python code and extract relevant AST information and coding patterns"""
        try:
            tree = ast.parse(code_str)
            context = {
                'functions': [],
                'classes': [],
                'imports': [],
                'patterns': {
                    'naming_style': {},
                    'indentation': None,
                    'docstring_style': None
                }
            }
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    context['functions'].append({
                        'name': node.name,
                        'lineno': node.lineno,
                        'args': [arg.arg for arg in node.args.args],
                        'docstring': ast.get_docstring(node)
                    })
                    # Learn naming patterns
                    self._learn_naming_pattern(node.name, 'function')
                elif isinstance(node, ast.ClassDef):
                    context['classes'].append({
                        'name': node.name,
                        'lineno': node.lineno,
                        'methods': [m.name for m in node.body if isinstance(m, ast.FunctionDef)]
                    })
                    self._learn_naming_pattern(node.name, 'class')
                elif isinstance(node, ast.Import):
                    for name in node.names:
                        context['imports'].append(name.name)
                        self.user_patterns['preferred_libraries'].add(name.name)
                elif isinstance(node, ast.ImportFrom):
                    module_import = f"{node.module}.{node.names[0].name}"
                    context['imports'].append(module_import)
                    self.user_patterns['preferred_libraries'].add(node.module)
            
            return context
        except Exception as e:
            return {'error': str(e)}

    def _learn_naming_pattern(self, name, type_):
        """Learn user's naming conventions"""
        if name.islower():
            style = 'snake_case'
        elif name[0].isupper():
            style = 'PascalCase'
        else:
            style = 'camelCase'
        
        if type_ not in self.user_patterns['coding_style']:
            self.user_patterns['coding_style'][type_] = {}
        
        if style not in self.user_patterns['coding_style'][type_]:
            self.user_patterns['coding_style'][type_][style] = 0
        self.user_patterns['coding_style'][type_][style] += 1

    def add_code_context(self, filename, code):
        """Add or update code context for a file"""
        self.code_context[filename] = self.parse_code_context(code)
        self._update_learning_history('code_analysis', filename)

    def format_conversation_context(self):
        """Format conversation and code context for the model"""
        context = "Previous conversation:\n"
        for qa in self.conversation_history[-3:]:
            context += f"User: {qa['question']}\nAssistant: {qa['answer']}\n\n"
        
        if self.code_context:
            context += "\nCode context:\n"
            for filename, ctx in self.code_context.items():
                context += f"\nFile: {filename}\n"
                context += json.dumps(ctx, indent=2) + "\n"
        
        # Add learned patterns
        context += "\nLearned user preferences:\n"
        context += json.dumps(self.user_patterns, indent=2) + "\n"
        
        return context

    def _update_learning_history(self, action_type, details):
        """Track learning events"""
        self.learning_history.append({
            'timestamp': datetime.datetime.now().isoformat(),
            'type': action_type,
            'details': details
        })

    def ask(self, prompt, system_prompt="You are an expert programming assistant that learns and adapts to the user's coding style.", code_context=None):
        if code_context:
            self.add_code_context(code_context['filename'], code_context['code'])

        with self.lock:
            try:
                context = self.format_conversation_context()
                # Add feedback-aware context
                context += "\nFeedback metrics:\n"
                context += f"Acceptance rate: {self._calculate_acceptance_rate()}%\n"
                context += "Recent feedback: " + json.dumps(self.user_patterns['feedback_history'][-3:]) + "\n"
                
                full_prompt = f"{context}\nCurrent question: {prompt}"
                
                result = self.llm(
                    f"{system_prompt}\n\n{full_prompt}",
                    max_tokens=512,
                    temperature=0.7,
                    echo=True
                )
                
                response = result["choices"][0]["text"].strip()
                
                self.conversation_history.append({
                    'question': prompt,
                    'answer': response,
                    'timestamp': datetime.datetime.now().isoformat()
                })
                
                return response
            except Exception as e:
                return f"[ERROR] Failed to run inference: {e}"

    def clear_history(self):
        """Clear conversation history but retain learned patterns"""
        self.conversation_history = []
        self.code_context = {}

    def provide_feedback(self, suggestion_id, was_helpful, comments=None):
        """Track user feedback on suggestions"""
        feedback = {
            'timestamp': datetime.datetime.now().isoformat(),
            'suggestion_id': suggestion_id,
            'was_helpful': was_helpful,
            'comments': comments
        }
        self.user_patterns['feedback_history'].append(feedback)
        
        if was_helpful:
            self.user_patterns['interaction_metrics']['suggestions_accepted'] += 1
        else:
            self.user_patterns['interaction_metrics']['suggestions_rejected'] += 1
            
        self._update_learning_history('feedback_received', feedback)

    def ask(self, prompt, system_prompt="You are an expert programming assistant that learns and adapts to the user's coding style.", code_context=None):
        if code_context:
            self.add_code_context(code_context['filename'], code_context['code'])

        # First, process through conversation model
        conv_response = self.conversation_model.process_conversation(prompt)
        
        if conv_response['response_type'] == 'conversation':
            # Handle pure conversation
            return conv_response['message']
        elif conv_response['response_type'] == 'task_switch':
            # Handle task switching with suggestions
            response = conv_response['message']
            if 'suggestions' in conv_response:
                response += "\nSuggested options:\n- " + "\n- ".join(conv_response['suggestions'])
            return response
        
        # For technical requests, use the main model
        with self.lock:
            try:
                context = self.format_conversation_context()
                # Add conversation context
                context += "\nCurrent task: " + str(self.conversation_model.context['current_task'])
                full_prompt = f"{context}\nCurrent question: {prompt}"
                
                result = self.llm(
                    f"{system_prompt}\n\n{full_prompt}",
                    max_tokens=512,
                    temperature=0.7,
                    echo=True
                )
                
                response = result["choices"][0]["text"].strip()
                
                self.conversation_history.append({
                    'question': prompt,
                    'answer': response,
                    'timestamp': datetime.datetime.now().isoformat(),
                    'task_context': self.conversation_model.context['current_task']
                })
                
                return response
            except Exception as e:
                return f"[ERROR] Failed to run inference: {e}"

    def clear_history(self):
        """Clear conversation history but retain learned patterns"""
        self.conversation_history = []
        self.code_context = {}

    def _calculate_acceptance_rate(self):
        """Calculate the acceptance rate of suggestions"""
        total = (self.user_patterns['interaction_metrics']['suggestions_accepted'] + 
                self.user_patterns['interaction_metrics']['suggestions_rejected'])
        if total == 0:
            return 100
        return round((self.user_patterns['interaction_metrics']['suggestions_accepted'] / total) * 100, 2)

# Interactive CLI
if __name__ == "__main__":
    runner = LocalModelRunner()
    print("Sentient Debugger AI Assistant")
    print("This AI learns from your coding style and adapts to your preferences.")
    print("\nCommands:")
    print("  exit    - Exit the program")
    print("  clear   - Clear conversation history")
    print("  stats   - Show learned patterns and statistics")
    print("  CODE:   - Set code context (format: CODE:filename.py\\ncode)")
    print("\nWhat can I help you with?\n")
    
    while True:
        try:
            user_input = input("> ").strip()
            
            if user_input.lower() == 'exit':
                break
            elif user_input.lower() == 'clear':
                runner.clear_history()
                print("Conversation history cleared. (Learned patterns retained)")
                continue
            elif user_input.lower() == 'stats':
                print("\nLearned Patterns:")
                print(json.dumps(runner.user_patterns, indent=2))
                print("\nLearning History:")
                print(json.dumps(runner.learning_history[-5:], indent=2))  # Show last 5 events
                continue
            
            if user_input.startswith("CODE:"):
                try:
                    _, rest = user_input.split("CODE:", 1)
                    filename, code = rest.split("\n", 1)
                    filename = filename.strip()
                    
                    code_context = {
                        'filename': filename,
                        'code': code
                    }
                    runner.add_code_context(filename, code)
                    print(f"\nCode context set for file: {filename}")
                    print("Learned new patterns from your code.")
                    continue
                except Exception as e:
                    print(f"Error parsing code context: {e}")
                    print("Please use the format: CODE:filename.py\\nYour code here")
                    continue
            
            response = runner.ask(user_input)
            print("\nAI Response:\n", response, "\n")
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")
