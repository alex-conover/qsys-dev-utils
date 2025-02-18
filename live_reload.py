import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from lib.log import logger


class ReloadHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback

    def on_modified(self, event):
        if isinstance(event.src_path, str) and event.src_path.endswith(".lua"):
            logger.info(f"File modified: {event.src_path}")
            self.callback(event.src_path)


def start_watching(path: str, callback):
    event_handler = ReloadHandler(callback)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    logger.debug(f"Started watching directory: {path}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
