import tkinter as tk

class BaseWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def on_close(self):
        self.root.quit()
        self.root.destroy()

    def run(self):
        self.root.mainloop()