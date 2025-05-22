# Handles code change events

from watchdog.events import FileSystemEventHandler
from static_analysis.call_static_parser import analyze_file
import logging
from datetime import datetime

class CodeChangeHandler(FileSystemEventHandler):
    def __init__(self, ai_runner=None):
        self.supported_extensions = ('.py', '.ts', '.rs', '.tsx', '.jsx', '.js')
        self.last_modified = {}
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('CodeChangeHandler')
        self.ai_runner = ai_runner

    def on_modified(self, event):
        if event.is_directory:
            return

        file_path = event.src_path
        current_time = datetime.now()

        # Debounce file changes (prevent multiple rapid triggers)
        if file_path in self.last_modified:
            time_diff = (current_time - self.last_modified[file_path]).total_seconds()
            if time_diff < 1:  # Ignore changes within 1 second
                return

        if not file_path.endswith(self.supported_extensions):
            return

        self.last_modified[file_path] = current_time
        self.logger.info(f"[EVENT] File modified: {file_path}")
        
        try:
            # First run static analysis
            analysis_result = analyze_file(file_path)
            
            # If AI runner is available, get AI suggestions
            if self.ai_runner:
                with open(file_path, 'r') as f:
                    code_content = f.read()
                
                # Ask user for permission to analyze
                print(f"\n[AI] Would you like me to analyze the changes in {os.path.basename(file_path)}? (y/n)")
                response = input().lower().strip()
                
                if response == 'y':
                    suggestions = self.ai_runner.ask(
                        f"Please analyze this code and provide suggestions for improvements:\n{code_content}",
                        code_context={'filename': file_path, 'code': code_content}
                    )
                    print("\n[AI] Analysis and Suggestions:")
                    print(suggestions)
                    print("\nType 'feedback yes/no [comments]' to provide feedback on these suggestions.")
                
        except Exception as e:
            self.logger.error(f"[ERROR] Failed to analyze {file_path}: {e}")

    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith(self.supported_extensions):
            return
        self.logger.info(f"[EVENT] New file created: {event.src_path}")
        analyze_file(event.src_path)

    def on_deleted(self, event):
        if event.is_directory or not event.src_path.endswith(self.supported_extensions):
            return
        self.logger.info(f"[EVENT] File deleted: {event.src_path}")
