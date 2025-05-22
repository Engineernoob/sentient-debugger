# Entry point for the Sentient Debugger

import argparse
import os
import logging
from watcher.file_monitor import start_monitoring
from ai.local_model_runner import LocalModelRunner

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger('SentientDebugger')

def main():
    logger = setup_logging()
    
    parser = argparse.ArgumentParser(description="Sentient Debugger - An AI-powered coding assistant")
    parser.add_argument("--watch", required=True, help="Path to the code directory")
    parser.add_argument("--model", default="codellama-7b-instruct.Q2_K.gguf", 
                       help="Name of the model to use")
    parser.add_argument("--no-gpu", action="store_true", 
                       help="Disable GPU acceleration")
    
    args = parser.parse_args()

    # Validate watch path
    watch_path = os.path.abspath(args.watch)
    if not os.path.exists(watch_path):
        logger.error(f"Watch path does not exist: {watch_path}")
        return

    # Initialize AI model
    try:
        logger.info("Initializing AI assistant...")
        ai_runner = LocalModelRunner(
            model_name=args.model,
            n_gpu_layers=0 if args.no_gpu else 33
        )
        logger.info("AI assistant initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize AI assistant: {e}")
        return

    # Start file monitoring
    logger.info(f"Starting file monitoring on: {watch_path}")
    try:
        start_monitoring(watch_path)
    except KeyboardInterrupt:
        logger.info("Shutting down Sentient Debugger...")
    except Exception as e:
        logger.error(f"Error during monitoring: {e}")

if __name__ == "__main__":
    main()
