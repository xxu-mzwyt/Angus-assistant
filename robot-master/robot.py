# coding=utf-8

import baiduApi

if __name__ == "__main__":
    api_id = "18158180"
    api_key = "HXeOuF3fzhWVNwesAn5kD2Ep"
    api_secert = "P3GkrQTecuGN1dg7yLLjgZeqQF3McBem"
    bdr = baiduApi.BaiduRest(api_id, api_key, api_secert)
    # while True:
    # input("按下回车开始说话，自动停止")
    print('开始录音')
    bdr.recorder("output.wav")
    print("结束")
    ask = bdr.getText('output.wav')
    print('你：', ask)
    # robot = turing.Turing()
    # ans = robot.anser(ask)
    ans = "苟利国家生死以，岂因祸福避趋之"
    print('机器人：', ans)
    bdr.getVoice(ans, ".\\output.mp3")
    bdr.speak(".\\output.mp3")
