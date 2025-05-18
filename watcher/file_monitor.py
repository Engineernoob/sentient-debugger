# File monitoring logic
import time
from watchdog.observers import Observer
from watcher.event_handler import CodeChangeHandler

def start_monitoring(path_to_watch: str):
    event_handler = CodeChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=True)
    observer.start()
    print(f"[WATCHER] Monitoring started on: {path_to_watch}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("[WATCHER] Stopped monitoring.")
    observer.join()
