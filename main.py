# -*- coding: utf-8 -*- #

# main.py

import tkinter as tk
import tkinter.messagebox as ms
import random
import time
import threading
import webbrowser

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

ft = ('Verdana', 20)
ft_small = ('Verdana', 13)

bdr = baidu_api.BaiduRest()

def create_note(note_text=""):

    note = tk.Toplevel(root)
    note.geometry('320x280')
    note.wm_attributes("-alpha", 0.7)
    note.wm_attributes('-topmost', 1)
    note.iconbitmap(".\\assest\\note.ico")
    note.title("便签 " + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

    TextBox = tk.Text(note, font=ft)
    Scroll = tk.Scrollbar(note)
    
    Scroll.pack(side=tk.RIGHT,fill=tk.Y)   
    TextBox.pack(side=tk.LEFT,fill=tk.Y)

    Scroll.config(command=TextBox.yview)
    TextBox.config(yscrollcommand=Scroll.set)

    TextBox.insert('end', note_text)

def start_rec(text=''):

    RecBtn['state'] = 'disabled'

    if text:
        thread = threading.Thread(target=reply)
        thread.start()

    else:
        thread = threading.Thread(target=record)
        thread.start()

def record():

    IptEntry.delete(0, 'end')
    IptEntry.insert('end',"正在倾听...")

    bdr.recorder(".\\audio\\input.wav")

    IptEntry.delete(0, 'end')
    IptEntry.insert('end', '完毕。')

    ask = bdr.getText('.\\audio\\input.wav')
    IptEntry.delete(0, 'end')
    IptEntry.insert(0, ask)
    
    reply()


def reply():
    
    def next_ask():
        answer(random.choice(NextAsk_List))
    def no_answer():
        answer(random.choice(NoAnswer_List))
    def greet_me():
        answer(random.choice(Greeting_List))
    def say_goodbye():
        answer(random.choice(Leaving_List))

    ask = IptEntry.get()

    OutText["state"] = 'normal'
    OutText.insert('end', '>>' + ask + '\n')
    OutText.focus_force()
    OutText.see('end')
    OutText["state"] = 'disabled'

    if not ask:
        no_answer()
        return

    if "你好" in ask or "您好" in ask or "早上好" in ask or "中午好" in ask or "晚上好" in ask or "Hello" in ask or "嗨" in ask:
        greet_me()
        return

    if "再见" in ask or "拜拜" in ask:
        say_goodbye()
        exit()
        return

    if "搜索" in ask:
        search(ask[ask.find("搜索")+2:])
        next_ask()
        return

    if "记录" in ask:
        create_note(ask[ask.find("记录")+2:])
        next_ask()
        return


    no_answer()

def answer(ans):
    
    IptEntry.delete(0, 'end')
    
    OutText["state"] = 'normal'
    OutText.insert('end', 'Angus:' + ans + '\n')
    OutText.focus_force()
    OutText.see('end')
    OutText["state"] = 'disabled'

    bdr.getVoice(ans, ".\\audio\\output.mp3")
    bdr.speak(".\\audio\\output.mp3")

    RecBtn['state'] = 'normal'
    IptEntry.focus_force()

def search(term):
    
    url = "https://www.baidu.com/s?wd="
    webbrowser.open(url + term)


def exit():
    if ms.askokcancel('Angus', '您确认要退出吗？\n正在进行的计时与笔记会关闭。'):
        root.quit()

root = window.DragWindow(alpha=0.97, bg="grey")

root.set_window_size(400, 530)
root.set_display_postion(100, 100)

IptEntry = tk.Entry(root, width=27, font=ft, bd=1)
IptEntry.place(x=50,y=494)
IptEntry.bind("<Return>", start_rec)

OutText = tk.Text(root, width=30, height=20, font=ft_small, bd=0, bg="grey", fg="white", state="disabled", cursor='arrow')
OutText.place(x=20, y=20)

ExitImage = tk.PhotoImage(file=".\\assest\\exit.png")
ExitBtn = tk.Button(root, image=ExitImage, command=exit, bg="grey", bd=0, width=30, height=30)
ExitBtn.place(x=360, y=10)

MicImage = tk.PhotoImage(file=".\\assest\\mic.png")
RecBtn = tk.Button(root, image=MicImage, command=start_rec, bg="grey", bd=0, width=50, height=33, font=ft)
RecBtn.place(x=0, y=495)

SepLine = tk.Label(root, bg="#515151", width=80, height=1)
SepLine.place(x=0, y=473)

Covline = tk.Label(root, bg="grey", width=80, height=1)
Covline.place(x=0, y=471)

root.mainloop()

