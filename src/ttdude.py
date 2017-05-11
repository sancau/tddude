# coding=utf=8

from tkinter import *
import tempfile

from monitor import monitor


ICON = (b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00h\x05\x00\x00'
        b'\x16\x00\x00\x00(\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x00\x01\x00'
        b'\x08\x00\x00\x00\x00\x00@\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x01\x00\x00\x00\x01') + b'\x00'*1282 + b'\xff'*64


_, ICON_PATH = tempfile.mkstemp()
with open(ICON_PATH, 'wb') as icon_file:
    icon_file.write(ICON)


class App:

	def __init__(self, source_root='.', log='.'):
		self.init_ui()
		self.source_root = source_root
		self.log = log

	def move_window(self, event): 
		self.w.geometry('+{}+{}'.format(event.x_root, event.y_root))

	def init_ui(self):
		self.w = Tk()
		self.w.iconbitmap(default=ICON_PATH)
		self.w.title('')
		self.w.maxsize(100, 70)
		self.w.resizable(False, False)
		self.w.overrideredirect(1)
		self.w.bind('<B1-Motion>', self.move_window)

		self.log = StringVar()
		self.log.set('NO LOG')

		self.text = StringVar()
		self.text.set('READY')

		self.label = Label(self.w, textvariable=self.text, relief=RAISED)
		self.label.configure(background='green', font=("Courier", 24))
		self.label.bind("<Button-1>", self.toggle_details)
		self.label.pack()

	def run(self):
		self.w.lift()
		self.w.call('wm', 'attributes', '.', '-topmost', True)
		self.w.mainloop()

	def toggle_details(self, event=None):
		# TODO
		print(self.log)

	def update_gui(self, text, color):
		self.text.set(text)
		self.label.configure(background=color)


def main(source_root, log=None):
    print('[TDDUDE] Monitoring path {}'.format(source_root))
    print()
    monitor(source_root, log)


if __name__ == '__main__':
    fire.Fire(main)