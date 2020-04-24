import tkinter as tk
from drag_window import DragWindow


root = DragWindow(alpha=1, bg="grey")

root.set_window_size(300, 350)
root.set_display_postion(100, 100)

tk.Button(root, text="Exit", command=root.quit, bg="white", bd=0).pack(side=tk.TOP)
tk.Canvas(root, height=30, bg="grey", bd=0, relief="groove").pack(side=tk.BOTTOM)
tk.Entry(root, width=300).pack(side=tk.BOTTOM)


root.mainloop()
