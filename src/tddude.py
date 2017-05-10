# coding=utf-8
from datetime import datetime, timedelta
import time
import os

import fire

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from tester import test


def get_last_modified_offset(filename):
    try:
        mtime = os.path.getmtime(filename)
    except OSError:
        mtime = 0
    mod = datetime.fromtimestamp(mtime)
    delta = datetime.now() - mod
    return delta.seconds, delta.microseconds


class EventHandler(FileSystemEventHandler):
    def __init__(self, root_dir, log=None):
        super(EventHandler, self).__init__()
        self.root_dir = root_dir
        self.log = log
        self.history = {}

    def on_modified(self, event):
        
        if any(['__pycache__' in event.src_path,
                '.cache' in event.src_path,
                self.log == event.src_path, 
                event.is_directory]):
            return

        if event.src_path in self.history:
            delta = datetime.now() - self.history[event.src_path]
            if delta.seconds < 1 and delta.microseconds < 500000:
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
        

def notify(result):
    print('[GREEN]' if not result.failed else '[RED]', 
          '({}/{})'.format(result.passed, result.passed + result.failed),
          'Execution time: {} seconds'.format(result.time.seconds))


def monitor(source_root, log):
    observer = Observer()
    event_handler = EventHandler(source_root, log)
    observer.schedule(event_handler, source_root, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
        print('Stopped monitoring')


def main(source_root, log=None):
    print('[TDDUDE] Monitoring path {}'.format(source_root))
    print()
    monitor(source_root, log)


if __name__ == '__main__':
    fire.Fire(main)
