# -*- coding: utf-8 -*- #

# main.py

import tkinter as tk
import tkinter.messagebox as ms
import random
import time
import threading
import webbrowser
import smtplib
import playsound
import requests

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

intro_text = """

            你好，我是Angus。


-----------------------------------------
        
      点击左下角的图标来对我说话，或
      在右侧的输入框里输入并按下Enter
        

        你可以问我：

            “帮我记录‘八点钟回电话’”
            “搜索‘世界卫生组织’”
            “今天有什么新闻”
            “倒计时十分钟”
            “发送电子邮件”*

            * 需要合适的SMTP服务器

"""

ft = (('Verdana', 20))
ft_small = ('Verdana', 13)

first = True
Net_Error = False

try:
    bdr = baidu_api.BaiduRest()
except:
    Net_Error = True


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

def create_timer():

    TimerEnd = False

    def exit_timer():
        timer.quit()
        TimerEnd = True

    time_m = int(IptEntry.get())
    IptEntry.delete(0, 'end')
    IptEntry.bind("<Return>", start_rec)

    RecBtn['state'] = 'normal'

    time_s = 0

    timer = tk.Toplevel(root)
    timer.geometry('240x120')
    # timer.protocol("WM_DELETE_WINDOW", exit_timer)
    timer.iconbitmap(".\\assest\\timer.ico")
    timer.resizable(0,0)
    timer.title("计时器")

    tk.Label(timer, font=ft, text=" ").pack()
    TimeLast = tk.Label(timer, font=ft, text="00:00")
    TimeLast.pack()


    while time_m or time_s and not TimerEnd:
        if time_s == 0:
            time_s = 60
            time_m -= 1
        time_s -= 1
        TimeLast['text'] = str(time_m) + ":" + str(time_s)
        time.sleep(1)

    for i in range(2):
        if not TimerEnd:
            playsound.playsound(".\\assest\\ring.mp3")

def create_news():
    
    news = tk.Toplevel(root)
    news.geometry('450x360')

    news.iconbitmap(".\\assest\\news.ico")
    news.title(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + " 的新闻摘要")

    TextBox = tk.Text(news, font=ft_small)
    Scroll = tk.Scrollbar(news)
    
    Scroll.pack(side=tk.RIGHT,fill=tk.Y)   
    TextBox.pack(side=tk.LEFT,fill=tk.Y)

    Scroll.config(command=TextBox.yview)
    TextBox.config(yscrollcommand=Scroll.set)

    TextBox.insert('end', get_news())
    TextBox['state'] = 'disabled'

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
    IptEntry['state'] = 'disabled'

    bdr.recorder(".\\audio\\input.wav")

    IptEntry['state'] = 'normal'
    IptEntry.delete(0, 'end')
    IptEntry.insert('end', '完毕。')
    IptEntry['state'] = 'disabled'

    ask = bdr.getText('.\\audio\\input.wav')
    IptEntry['state'] = 'normal'
    IptEntry.delete(0, 'end')
    IptEntry.insert(0, ask)
    
    reply()


def reply():

    global first
    
    if first:
        OutText["state"] = 'normal'
        OutText.delete(1.0, 'end')
        OutText["state"] = 'disabled'
        first = False

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
    
    if "搜索" in ask:
        try:
            search(ask[ask.find("搜索")+2:])
            next_ask()
        except:
            answer("您的浏览器连接异常。")
        return

    if "百度" in ask:
        try:
            search(ask[ask.find("百度")+2:])
            next_ask()
        except:
            answer("您的浏览器连接异常。")
        return

    if "邮件" in ask:
        time.sleep(3)
        answer("邮件服务器连接异常。")
        return

    if "新闻" in ask:
        try:
            create_news()
            next_ask()
        except:
            answer("新闻服务器连接异常。")
        return

    if "记录" in ask:
        create_note(ask[ask.find("记录")+2:])
        next_ask()
        return

    if "时间" in ask:
        answer("现在时间为：\n" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        return

    if "计时" in ask:
        answer("请在输入框中确认您想要倒计时的时间（以分钟计）")
        type_time()
        return

    if "你好吗" in ask or "你怎么样" in ask:
        answer("我今天很好！")
        return

    if "你好" in ask or "您好" in ask or "早上好" in ask or "中午好" in ask or "晚上好" in ask or "Hello" in ask or "嗨" in ask:
        greet_me()
        return

    if "再见" in ask or "拜拜" in ask or "晚安" in ask:
        say_goodbye()
        root.quit()
        return        

    no_answer()

def answer(ans):
    
    IptEntry.delete(0, 'end')
    
    OutText["state"] = 'normal'
    OutText.insert('end', 'Angus: ' + ans + '\n')
    OutText.focus_force()
    OutText.see('end')
    OutText["state"] = 'disabled'

    bdr.getVoice(ans, ".\\audio\\output.mp3")
    bdr.speak(".\\audio\\output.mp3")

    RecBtn['state'] = 'normal'
    IptEntry.focus_force()

def type_time():

    RecBtn['state'] = 'disabled'
    IptEntry.bind("<Return>", start_time)

def start_time(u=""):

    thread = threading.Thread(target=create_timer)
    thread.start()

def search(term):
    
    url = "https://www.baidu.com/s?wd="
    webbrowser.open(url + term)

def get_news():

    rslt = ""

    news_url = "https://3g.163.com/touch/reconstruct/article/list/BA8D4A3Rwangning/0-10.html"

    res = requests.get(url=news_url).text
    res = res.replace("\\\"", "“").split("\"")

    for i in range(len(res)):

        if res[i] == "title":
            rslt += (res[i - 2].replace("\\", "").replace("#", "") + "\n")
            rslt += (res[i + 2].replace("\\", "") + "\n")

    return rslt
    

root = window.DragWindow(alpha=0.97, bg="grey")

root.set_window_size(400, 530)
root.set_display_postion(100, 100)

SepLine = tk.Label(root, bg="#515151", width=80, height=1)
SepLine.place(x=0, y=473)

Covline = tk.Label(root, bg="grey", width=80, height=1)
Covline.place(x=0, y=471)

IptEntry = tk.Entry(root, width=27, font=ft, bd=1)
IptEntry.place(x=50,y=494)
IptEntry.bind("<Return>", start_rec)
IptEntry.focus_force()

OutText = tk.Text(root, width=30, height=20, font=ft_small, bd=0, bg="grey", fg="white", state="disabled", cursor='arrow')
OutText.place(x=20, y=20)

ExitImage = tk.PhotoImage(file=".\\assest\\exit.png")
ExitBtn = tk.Button(root, image=ExitImage, command=root.quit, bg="grey", bd=0, width=30, height=30)
ExitBtn.place(x=360, y=10)

MicImage = tk.PhotoImage(file=".\\assest\\mic.png")
RecBtn = tk.Button(root, image=MicImage, command=start_rec, bg="grey", bd=0, width=50, height=33, font=ft)
RecBtn.place(x=0, y=495)



if Net_Error:
    OutText["state"] = 'normal'
    OutText.insert('end', "网络连接中断，请重启软件重试。")
    
    OutText["state"] = "disabled"
    IptEntry["state"] = "disabled"
    RecBtn["state"] = "disabled"
else:
    OutText["state"] = 'normal'
    OutText.insert('end', intro_text)
    OutText["state"] = 'disabled'

root.mainloop()

