# Entry point for the Sentient Debugger

import argparse
from watcher.file_monitor import start_monitoring

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start the Sentient Debugger")
    parser.add_argument("--watch", required=True, help="Path to the code directory")
    args = parser.parse_args()

    start_monitoring(args.watch)
