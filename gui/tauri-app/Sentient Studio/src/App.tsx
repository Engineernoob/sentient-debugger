import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [output, setOutput] = useState<string>('');
  const [input, setInput] = useState<string>('');
  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  const [userName, setUserName] = useState<string>('');
  const [isInitialized, setIsInitialized] = useState<boolean>(false);

  useEffect(() => {
    if (!isInitialized) {
      setOutput("Welcome to Sentient Studio! May I know your name?");
      setIsInitialized(true);
    }
  }, [isInitialized]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsProcessing(true);
    
    try {
      if (!userName) {
        setUserName(input);
        setOutput(prev => `${prev}\n\nGreat to meet you, ${input}! 😊\nI'm here to help you with your programming tasks. What would you like to work on today?`);
      } else {
        setOutput(prev => `${prev}\n\n${userName}: ${input}\nAI: Processing...`);
      }
      setInput('');
    } catch (error) {
      console.error('Error:', error);
      setOutput(prev => `${prev}\n\nError: Failed to process request. Please try again.`);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="container">
      <header>
        <h1>Sentient Studio</h1>
        {userName && <p>Welcome, {userName}!</p>}
      </header>
      
      <main>
        <div className="output-area">
          <pre>{output}</pre>
        </div>
        
        <form onSubmit={handleSubmit} className="input-area">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={userName ? "Type your message..." : "Enter your name..."}
            disabled={isProcessing}
          />
          <button type="submit" disabled={isProcessing}>
            Send
          </button>
        </form>
      </main>
    </div>
  );
}

export default App;
