import tkinter as tk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from queue import Queue
import sys

class CustomHandler(FileSystemEventHandler):
    def __init__(self, app):
        FileSystemEventHandler.__init__(self)
        self.app = app
    def on_created(self, event): app.notify(event)
    def on_deleted(self, event): app.notify(event)
    def on_modified(self, event): app.notify(event)
    def on_moved(self, event): app.notify(event)

class App(object):
    def __init__(self):
        path = '.'
        handler = CustomHandler(self)
        self.observer = Observer()
        self.observer.schedule(handler, path, recursive=True)

        self.queue = Queue()
        self.root = tk.Tk()

        self.text = tk.Text(self.root)
        self.text.pack(fill="both", expand=True)

        self.text.insert("end", "Watching %s...\n" % path)

        self.root.bind("<Destroy>", self.shutdown)
        self.root.bind("<<WatchdogEvent>>", self.handle_watchdog_event)

        self.observer.start()

    def handle_watchdog_event(self, event):
        """Called when watchdog posts an event"""
        watchdog_event = self.queue.get()
        print("event type:", type(watchdog_event))
        self.text.insert("end", str(watchdog_event) + "\n")

    def shutdown(self, event):
        """Perform safe shutdown when GUI has been destroyed"""
        self.observer.stop()
        self.observer.join()

    def mainloop(self):
        """Start the GUI loop"""
        self.root.mainloop()

    def notify(self, event):
        """Forward events from watchdog to GUI"""
        self.queue.put(event)
        self.root.event_generate("<<WatchdogEvent>>", when="tail")

app = App()
app.mainloop()