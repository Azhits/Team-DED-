import tkinter as tk

from PIL import Image, ImageTk


class Interface(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('auto_genshin_v0.0.1')
        self.resizable(False, False)
        self.button_click = False
        width = 250
        height = 100
        x = self.winfo_screenwidth() - width
        y = (self.winfo_screenheight()) // 2
        self.geometry(f'{width}x{height}+{x}+{y}')
        self.create_objects()

    def create_objects(self):
        frame = tk.Frame(self)
        frame.pack(expand=True, fill='both')
        self.button = tk.Label(self, text='заглушка', width=30)
        self.button.pack(pady=5)
        self.button.bind("<Button-1>", self.on_button_click)

    def on_button_click(self, event):
        self.button_click = True
    
def use_attrs():
    root.attributes('-alpha', 0.3)
    root.attributes('-topmost', True)

if __name__ == '__main__':
    root = Interface()
    root.after(100, use_attrs)
    print(root.button_click)
    root.mainloop()