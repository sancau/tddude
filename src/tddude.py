# coding=utf-8

"""
TDDude is a dev. tool for easy and enjoyable 
test driven development workflow with Python
"""

from datetime import datetime
from queue import Queue
import sys

import fire
from tkinter import *
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from tester import test 


class EventHandler(FileSystemEventHandler):
    def __init__(self, app):
        super(FileSystemEventHandler, self).__init__()
        self.app = app

    def on_modified(self, event): 
        self.app.notify(event)


class Application:
    def __init__(self, path='.', log=None):
        self.observer = Observer()
        self.observer.schedule(EventHandler(self), path, recursive=True)
        self.queue = Queue()
        self.observer.start()
        self.log = log
        self.path = path
        self.history = {}
        self.log_window = None
        self.init_ui()

        self.root.event_generate("<<WatchdogEvent>>", when="tail")  # initial tests invokation

    def move_window(self, event): 
        self.root.geometry('+{}+{}'.format(event.x_root, event.y_root))

    def init_ui(self):
        self.root = Tk()
        self.root.title('TDD')  # we don't want any window title
        self.root.resizable(False, False)

        # dragable window behavior
        self.root.bind('<B1-Motion>', self.move_window) 
        self.root.overrideredirect(True)  # borderless main window

        self.root.bind("<Destroy>", self.shutdown)
        self.root.bind("<<WatchdogEvent>>", self.handle_watchdog_event)
        
        self.root.call('wm', 'attributes', '.', '-topmost', True)  # stay on top
        
        self.last_pytest_output = StringVar()
        self.last_pytest_output.set('')
        
        self.label_text = StringVar()
        self.label_text.set('READY')        
        self.label = Label(self.root, width=7, height=1, textvariable=self.label_text, relief=RAISED)
        self.label.configure(background='#94b8b8', font=('Courier bold', 24))
        
        # show / hide pytest output window
        self.label.bind("<Button-1>", self.show_pytest_log)
        self.label.pack()

    def handle_watchdog_event(self, event):
        """Called when watchdog posts an event"""
        event = self.queue.get()

        if any(['__pycache__' in event.src_path,
                '.cache' in event.src_path,
                self.log == event.src_path, 
                event.is_directory]):
            return

        if event.src_path in self.history:
            delta = datetime.now() - self.history[event.src_path]
            if delta.seconds < 1:  # prevents watchdog duplicated event issue :( 
                return 
        
        self.history[event.src_path] = datetime.now()

        print('[MODIFIED] {}'.format(event.src_path))
        try:
            result = test(self.path)
            if self.log:
                with open(self.log, 'w+') as f:
                    f.write(result.log)
            self.update_ui(result)
        except Exception as e:
            print('Could not run tests', e)
            print('No test were found or code has syntax errors')
            self.label_text.set('ERROR')
            self.label.configure(background='orange')

    def update_ui(self, result):
        all_passed = not result.failed
        self.last_pytest_output.set(result.log)
        self.label_text.set('{}/{}'.format(result.passed, result.passed + result.failed))
        self.label.configure(background='#39ac73' if all_passed else '#ff6666')    
        self.update_pytest_log_window()

    def shutdown(self, event):
        self.observer.stop()
        self.observer.join()

    def mainloop(self):
        self.root.mainloop()

    def notify(self, event):
        self.queue.put(event)
        self.root.event_generate("<<WatchdogEvent>>", when="tail")

    def show_pytest_log(self, event):
        if not self.log_window:
            self.log_window = Toplevel()
            self.log_window.title('Lastest PyTest Output')
            self.log_window.minsize(800, 600)
            self.log_window.protocol('WM_DELETE_WINDOW', self.on_pytest_log_x)
            self.log_window.log = Text(self.log_window)
            self.log_window.log.pack(expand=True, fill='both')
            self.update_pytest_log_window()
        else:
            self.log_window.lift()

    def on_pytest_log_x(self):
        self.log_window.withdraw()
        self.log_window = None

    def update_pytest_log_window(self):
        if self.log_window:
            self.log_window.log.delete('1.0', END)
            self.log_window.log.insert(END, self.last_pytest_output.get() + '\n')


def main(path='.', log=None):
    app = Application(path=path, log=log)
    app.mainloop()


if __name__ == '__main__':
    fire.Fire(main)
