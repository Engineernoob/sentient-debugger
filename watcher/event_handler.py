# Handles code change events

from watchdog.events import FileSystemEventHandler
from static_analysis.call_static_parser import analyze_file  # Will create this soon

class CodeChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory or not event.src_path.endswith(('.py', '.ts', '.rs')):
            return
        print(f"[EVENT] File modified: {event.src_path}")
        analyze_file(event.src_path)
