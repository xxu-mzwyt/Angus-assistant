# -*- coding: utf-8 -*- #

# main.py

import tkinter as tk
import tkinter.font as tf
import random
import time
import baidu_api
import window


Greeting_List = ["你好呀！",
                 "嗨！",
                 "很高兴见到你。",
                 "你好你好！",
                 "哈喽。",
                 "你好！找我有什么事？"]

Leaving_List  = ["再见！",
                 "期待再见到你！",
                 "很高兴帮到你，再见！"]

NoAnswer_List = ["嗯，我好像还不太知道呢……",
                 "我不太清楚你的意思。",
                 "不好意思，能解释一下吗？",
                 "能换一种说法试试看吗？"]

NextAsk_List  = ["好的，还有其他事情吗？",
                 "已完成！",
                 "没问题。",
                 "OK！"]

bdr = baidu_api.BaiduRest()

def create_note(note_text=""):

    note = tk.Toplevel(root)
    note.geometry('320x280')
    note.wm_attributes("-alpha", 0.7)
    note.wm_attributes('-topmost', 1)
    note.iconbitmap(".\\assest\\note.ico")
    note.title("便签 " + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

    TextBox = tk.Text(note, font='Verdana')
    Scroll = tk.Scrollbar(note)
    
    Scroll.pack(side=tk.RIGHT,fill=tk.Y)   
    TextBox.pack(side=tk.LEFT,fill=tk.Y)

    Scroll.config(command=TextBox.yview)
    TextBox.config(yscrollcommand=Scroll.set)

    TextBox.insert('end', note_text)

def record():

    print('正在倾听...')
    bdr.recorder(".\\audio\\input.wav")
    print('完毕。')

    ask = bdr.getText('.\\audio\\input.wav')
    print('>>', ask)

    ans = reply(ask)
    print('Angus:', ans)
    bdr.getVoice(ans, ".\\audio\\output.mp3")
    bdr.speak(".\\audio\\output.mp3")

def reply(ask):
    
    def next_ask():
        return random.choice(Greeting_List)
    def no_answer():
        return random.choice(NoAnswer_List)

    pass


root = window.DragWindow(alpha=0.9, bg="grey")

root.set_window_size(300, 350)
root.set_display_postion(100, 100)

ExitImage = tk.PhotoImage(file=".\\assest\\exit.png")
tk.Button(root, image=ExitImage, command=root.quit, bg="white", bd=0, font='Verdana', width=30, height=30).pack()

tk.Button(root, text="talk", command=create_note, bg="white", bd=0, font='Verdana').pack(side=tk.BOTTOM)

tk.Entry(root, width=300, font='Verdana').pack(side=tk.BOTTOM)

root.mainloop()

