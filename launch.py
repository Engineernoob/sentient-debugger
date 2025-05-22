# Entry point for the Sentient Debugger

import argparse
import os
import logging
import threading
from watcher.file_monitor import start_monitoring
from ai.local_model_runner import LocalModelRunner

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger('SentientDebugger')

def start_interactive_mode(ai_runner):
    print("\nSentient Debugger Interactive Mode")
    print("Type 'help' for available commands")
    print("Type 'exit' to quit\n")

    while True:
        try:
            user_input = input(">>> ").strip()
            
            if user_input.lower().startswith('feedback'):
                _, feedback = user_input.split(' ', 1)
                helpful, *comments = feedback.split(' ', 1)
                ai_runner.provide_feedback(
                    suggestion_id=len(ai_runner.conversation_history),
                    was_helpful=helpful.lower() == 'yes',
                    comments=comments[0] if comments else None
                )
                print("Thank you for your feedback!")
                continue
            elif user_input.lower() == 'exit':
                break
            elif user_input.lower() == 'help':
                print("\nAvailable commands:")
                print("  help          - Show this help message")
                print("  clear         - Clear conversation history")
                print("  feedback      - Provide feedback on last suggestion")
                print("  stats        - Show learning statistics and feedback metrics")
                print("  adapt        - Show how the AI has adapted to your style")
                print("  suggest       - Get code suggestions for current file")
                print("  explain       - Explain the current code")
                print("  test          - Generate test cases")
                print("  exit          - Exit interactive mode")
                print("  CODE:         - Share code context (format: CODE:filename.py\\ncode)")
                print("  metrics       - Show code quality metrics")
                print("  optimize      - Get optimization suggestions")
                print("  refactor      - Get refactoring suggestions")
                print("  patterns      - Show detected code patterns")
                print("  complexity    - Show code complexity metrics")
                print("  readability   - Show code readability metrics")
                print("  maintainability - Show code maintainability metrics")
                print("  security      - Show code security metrics")
                print("  performance   - Show code performance metrics")
                print("  bugs          - Show code bug metrics")
                print()
                continue
            
            response = ai_runner.ask(user_input)
            print("\nAI:", response.strip(), "\n")
            
        except KeyboardInterrupt:
            print("\nExiting interactive mode...")
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    logger = setup_logging()
    
    parser = argparse.ArgumentParser(description="Sentient Debugger - An AI-powered coding assistant")
    parser.add_argument("--watch", required=False, help="Path to the code directory to monitor")
    parser.add_argument("--model", default="codellama-7b-instruct.Q2_K.gguf", 
                       help="Name of the model to use")
    parser.add_argument("--no-gpu", action="store_true", 
                       help="Disable GPU acceleration")
    parser.add_argument("--watch-only", action="store_true",
                       help="Run in file monitoring mode only (no interactive mode)")
    
    args = parser.parse_args()

    # Initialize AI model
    try:
        logger.info("Initializing AI assistant...")
        ai_runner = LocalModelRunner(
            model_name=args.model
        )
        logger.info("AI assistant initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize AI assistant: {e}")
        return

    # Start monitoring if watch path is provided
    monitor_thread = None
    if args.watch:
        watch_path = os.path.abspath(args.watch)
        if not os.path.exists(watch_path):
            logger.error(f"Watch path does not exist: {watch_path}")
            return
            
        monitor_thread = threading.Thread(
            target=start_monitoring,
            args=(watch_path,),
            daemon=True
        )
        monitor_thread.start()
        logger.info(f"File monitoring started on: {watch_path}")

    # Run in watch-only mode if specified
    if args.watch_only and monitor_thread:
        try:
            monitor_thread.join()
        except KeyboardInterrupt:
            logger.info("Shutting down Sentient Debugger...")
        return

    # Start interactive mode by default
    try:
        start_interactive_mode(ai_runner)
    except Exception as e:
        logger.error(f"Interactive mode error: {e}")

if __name__ == "__main__":
    main()
