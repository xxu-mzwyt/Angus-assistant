# -*- coding: utf-8 -*- #

# reply.py


import random
import baidu_api


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

def get_answer(ask=""):
    
    bdr = baidu_api.BaiduRest()
    
    if ask == "":
        return "我没有听清你说了什么。"

    answered = False

    if "你好" in ask or "早上好" in ask or "中午好" in ask or "晚上好" in ask or "Hello" in ask or "嗨" in ask:
        return random.choice(Greeting_List)

    if "记录" in ask:


    if answered:
        return random.choice(NextAsk_List)
    else:
        return random.choice(NoAnswer_List)
