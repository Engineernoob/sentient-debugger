from typing import Dict
import datetime


class ConversationModel:
    def __init__(self):
        self.context = {
            'current_task': None,
            'project_context': {},
            'conversation_history': [],
            'user_preferences': {
                'frameworks': [],
                'coding_style': {},
                'tech_stack': []
            },
            'user_name': None,
            'session_start': datetime.datetime.now()
        }
        
    def start_conversation(self) -> Dict:
        """Initialize conversation with welcome message"""
        return {
            'response_type': 'welcome',
            'message': "Hello! I'm your AI programming assistant. I'm here to help you with coding, debugging, and any other development tasks. May I know your name?"
        }
    
    def set_user_name(self, name: str) -> Dict:
        """Handle user name response"""
        self.context['user_name'] = name
        return {
            'response_type': 'greeting',
            'message': (
                f"It's great to meet you, {name}! 😊\n\n"
                "I'm here to help you with your programming journey. I can:\n"
                "• Assist with coding and debugging\n"
                "• Suggest improvements and optimizations\n"
                "• Help with project planning and architecture\n"
                "• Answer programming questions\n"
                "• Monitor your code for potential issues\n\n"
                "What would you like to work on today?"
            )
        }
    
    def process_conversation(self, user_input: str) -> Dict:
        """Process conversational input and determine intent"""
        # Track conversation
        self.context['conversation_history'].append({
            'timestamp': datetime.datetime.now().isoformat(),
            'user': user_input,
            'user_name': self.context['user_name']
        })
        
        # Analyze intent
        intent = self._analyze_intent(user_input)
        
        if intent['type'] == 'task_switch':
            return self._handle_task_switch(intent)
        elif intent['type'] == 'technical_request':
            return self._prepare_technical_response(intent)
        elif intent['type'] == 'greeting':
            return self._handle_greeting()
        elif intent['type'] == 'farewell':
            return self._handle_farewell()
        
        return self._generate_conversation_response(intent)

    def _analyze_intent(self, text: str) -> Dict:
        """Enhanced intent analysis"""
        text_lower = text.lower()
        
        # Greeting patterns
        if any(word in text_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return {'type': 'greeting'}
            
        # Farewell patterns
        if any(word in text_lower for word in ['bye', 'goodbye', 'exit', 'quit']):
            return {'type': 'farewell'}
            
        # Technical patterns
        if any(word in text_lower for word in ['code', 'bug', 'error', 'fix', 'debug']):
            return {'type': 'technical_request', 'category': 'debugging'}
            
        # Task switching
        if any(word in text_lower for word in ['frontend', 'backend', 'database']):
            return {'type': 'task_switch', 'area': text_lower}
            
        return {'type': 'conversation', 'context': 'general'}

    def _handle_greeting(self) -> Dict:
        """Handle user greetings"""
        name = self.context['user_name'] or "there"
        return {
            'response_type': 'conversation',
            'message': f"Hello again, {name}! How can I help you today?"
        }

    def _handle_farewell(self) -> Dict:
        """Handle user farewells"""
        name = self.context['user_name'] or "there"
        return {
            'response_type': 'farewell',
            'message': f"Goodbye, {name}! It was great helping you. Feel free to come back anytime you need assistance!"
        }
    
    def _handle_task_switch(self, intent: Dict) -> Dict:
        """Handle switching between different development tasks"""
        self.context['current_task'] = intent['area']
        
        # Generate appropriate follow-up questions
        if intent['area'] == 'frontend':
            return {
                'response_type': 'task_switch',
                'message': 'Would you like to use a specific frontend framework? I can suggest one based on your project requirements.',
                'suggestions': ['React', 'Vue', 'Angular', 'Svelte'],
                'context': 'frontend_setup'
            }
        elif intent['area'] == 'backend':
            return {
                'response_type': 'task_switch',
                'message': 'For the backend, what are your main requirements? (Performance, scalability, ease of development?)',
                'context': 'backend_setup'
            }
        
        return {
            'response_type': 'clarification',
            'message': 'Could you tell me more about what you\'d like to work on?'
        }
    
    def _prepare_technical_response(self, intent: Dict) -> Dict:
        """Prepare context for technical requests"""
        return {
            'response_type': 'technical',
            'requires_code_model': True,
            'context': self.context,
            'intent': intent
        }
    
    def _generate_conversation_response(self, intent: Dict) -> Dict:
        """Generate conversational responses"""
        return {
            'response_type': 'conversation',
            'message': self._get_contextual_response(intent),
            'context': self.context['current_task']
        }
    
    def _get_contextual_response(self, intent: Dict) -> str:
        """Get context-aware response"""
        name = self.context['user_name'] or "there"
        
        if intent.get('type') == 'help_request':
            return f"Of course, {name}! I can help you with coding, debugging, or any other development tasks. What specific area would you like help with?"
            
        if not self.context['current_task']:
            return f"What would you like to work on, {name}? I can help with frontend, backend, or any other aspect of your project."
        
        return f"I'm here to help with your {self.context['current_task']} development, {name}. What specific aspect would you like to discuss?"