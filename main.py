from tkinter import *
from parse import before_run
from login import *

before_run()

class myTk(Tk):
    def __init__(self):
        super().__init__()

root = myTk()
root.title('京东数据库系统')

LoginPage(root)
root.mainloop()
