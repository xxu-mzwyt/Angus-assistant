# -*- coding: utf-8 -*- #

# record.py

import baidu_api
from reply import get_answer

def talk():

    bdr = baidu_api.BaiduRest()

    print('正在倾听...')
    bdr.recorder(".\\recordings\\input.wav")
    print('完毕。')

    ask = bdr.getText('.\\recordings\\input.wav')
    print('>>', ask)

    ans = get_answer(ask)
    print('Angus:', ans)
    bdr.getVoice(ans, ".\\recordings\\output.mp3")
    bdr.speak(".\\recordings\\output.mp3")

    return ans

talk()