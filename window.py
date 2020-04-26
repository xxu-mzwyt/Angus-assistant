# -*- coding: utf-8 -*- #

# window.py

import tkinter as tk

class DragWindow(tk.Tk):
    root_x, root_y, abs_x, abs_y = 0, 0, 0, 0
    width, height = None, None

    def __init__(self, topmost=True, alpha=0.4, bg="white", width=None, height=None):
        super().__init__()
        self["bg"] = bg
        self.width, self.height = width, height
        self.overrideredirect(True)
        self.wm_attributes("-alpha", alpha)      # 透明度
        self.wm_attributes("-toolwindow", True)  # 置为工具窗口
        self.wm_attributes("-topmost", topmost)  # 永远处于顶层
        self.bind('<B1-Motion>', self._on_move)
        self.bind('<ButtonPress-1>', self._on_tap)

    def set_display_postion(self, offset_x, offset_y):
        self.geometry("+%s+%s" % (offset_x, offset_y))

    def set_window_size(self, w, h):
        self.width, self.height = w, h
        self.geometry("%sx%s" % (w, h))

    def _on_move(self, event):
        offset_x = event.x_root - self.root_x
        offset_y = event.y_root - self.root_y

        if self.width and self.height:
            geo_str = "%sx%s+%s+%s" % (self.width, self.height,
                                       self.abs_x + offset_x, self.abs_y + offset_y)
        else:
            geo_str = "+%s+%s" % (self.abs_x + offset_x, self.abs_y + offset_y)
        self.geometry(geo_str)

    def _on_tap(self, event):
        self.root_x, self.root_y = event.x_root, event.y_root
        self.abs_x, self.abs_y = self.winfo_x(), self.winfo_y()

def create_window():

    root = DragWindow(alpha=0.9, bg="grey")

    root.set_window_size(300, 350)
    root.set_display_postion(100, 100)

    tk.Button(root, text="Exit", command=root.quit, bg="white", bd=0).pack(side=tk.TOP)
    tk.Canvas(root, height=30, bg="grey", bd=0, relief="groove").pack(side=tk.BOTTOM)
    tk.Entry(root, width=300).pack(side=tk.BOTTOM)

    root.mainloop()


def create_note(note_text=""):

    root = DragWindow(alpha=0.7, bg="grey")

    root.set_window_size(200, 200)
    root.set_display_postion(100, 100)

    ExitBtn = tk.Button(root, text="Delete", command=root.quit, width=200, bg="grey", bd=0).pack(side=tk.BOTTOM)
    
    TextBox = tk.Text(root)
    TextBox.place(width=200, height=175)
    TextBox.insert('end', note_text)

    root.mainloop()

# create_window()
create_note("Test Note")