# File monitoring logic
import time
import logging
import os
from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver
from watcher.event_handler import CodeChangeHandler

class FileMonitor:
    def __init__(self, path_to_watch: str, polling_fallback: bool = True):
        self.path = os.path.abspath(path_to_watch)
        self.polling_fallback = polling_fallback
        self.event_handler = CodeChangeHandler()
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('FileMonitor')

    def start(self):
        if not os.path.exists(self.path):
            raise ValueError(f"Path does not exist: {self.path}")

        # Try to use native observer first, fall back to polling if needed
        try:
            self.observer = Observer()
            self.observer.schedule(self.event_handler, path=self.path, recursive=True)
            self.observer.start()
            self.logger.info(f"[WATCHER] Monitoring started on: {self.path}")
        except Exception as e:
            if self.polling_fallback:
                self.logger.warning(f"Native observer failed, falling back to polling: {e}")
                self.observer = PollingObserver()
                self.observer.schedule(self.event_handler, path=self.path, recursive=True)
                self.observer.start()
            else:
                raise

    def stop(self):
        self.observer.stop()
        self.observer.join()
        self.logger.info("[WATCHER] Monitoring stopped.")

def start_monitoring(path_to_watch: str):
    monitor = FileMonitor(path_to_watch)
    try:
        monitor.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        monitor.stop()
    except Exception as e:
        logging.error(f"[ERROR] Monitoring failed: {e}")
        monitor.stop()
