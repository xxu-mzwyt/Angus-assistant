# -*- coding: utf-8 -*- #

# reply.py


import random
import baidu_api
import window
import threading




def get_answer(ask=""):
    
    bdr = baidu_api.BaiduRest()
    
    if ask == "":
        return "我没有听清你说了什么。"

    answered = False


    if "记录" in ask:

        t = threading.Thread(target = window.create_note(ask[ask.rfind("记录"):], root)
        t.start()
        
        answered = True

    if answered:
        return random.choice(NextAsk_List)
    else:
        if "你好" in ask or "早上好" in ask or "中午好" in ask or "晚上好" in ask or "Hello" in ask or "嗨" in ask:
            return random.choice(Greeting_List)
        else:
            return random.choice(NoAnswer_List)
