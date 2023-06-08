import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def on_any_event(self, event):
        self.callback(event.src_path)

def watch(folders=[''], callback=None):
    if not callback:
        raise ValueError("Callback function must be provided.")

    event_handler = MyHandler(callback)
    observer = Observer()

    for folder in folders:
        observer.schedule(event_handler, folder, recursive=True)

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()