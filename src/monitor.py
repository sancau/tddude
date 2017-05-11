# coding=utf-8

"""
Monitors given path, runs tester after modifications, writes log file, notifies GUI
"""

from datetime import datetime
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from tester import test


class EventHandler(FileSystemEventHandler):
    def __init__(self, root_dir, log=None, gui=None):
        super(EventHandler, self).__init__()
        self.root_dir = root_dir
        self.log = log
        self.history = {}
        self.gui = gui

    def on_modified(self, event):
        
        if any(['__pycache__' in event.src_path,
                '.cache' in event.src_path,
                self.log == event.src_path, 
                event.is_directory]):
            return

        if event.src_path in self.history:
            delta = datetime.now() - self.history[event.src_path]
            if delta.seconds < 1:
                return 
        
        self.history[event.src_path] = datetime.now()

        print('[MODIFIED] {}'.format(event.src_path))
        try:
            result = test(self.root_dir)
            if self.log:
                with open(self.log, 'w+') as f:
                    f.write(result.log)
            notify(result)
        except Exception as e:
            print('Could not run tests', e)
            print('No test were found or code has syntax errors')
        

    def notify(self, result):
        print('[GREEN]' if not result.failed else '[RED]', 
              '({}/{})'.format(result.passed, result.passed + result.failed),
              'Execution time: {} seconds'.format(result.time.seconds))

        if self.gui:
            self.gui.process_tests_result(result)


def monitor(source_root, log, gui):
    observer = Observer()
    event_handler = EventHandler(source_root, log, gui)
    observer.schedule(event_handler, source_root, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
        print('Stopped monitoring')
