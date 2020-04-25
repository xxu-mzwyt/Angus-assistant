# -*- coding: utf-8 -*- #

# baidu_api.py

from sys import byteorder
from array import array
from struct import pack
import time

import pyaudio
import wave
import subprocess
import urllib.request
import urllib
import json
import base64


class BaiduRest:
    def __init__(self, cu_id="18158180", api_key="HXeOuF3fzhWVNwesAn5kD2Ep", api_secert="P3GkrQTecuGN1dg7yLLjgZeqQF3McBem"):
        self.token_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"
        self.getvoice_url = "http://tsn.baidu.com/text2audio?tex=%s&lan=zh&cuid=%s&ctp=1&tok=%s"
        self.upvoice_url = 'http://vop.baidu.com/server_api'
        self.cu_id = cu_id
        self.getToken(api_key, api_secert)
        self.THRESHOLD = 500
        self.CHUNK_SIZE = 1024
        self.FORMAT = pyaudio.paInt16
        self.RATE = 8000

        return

    def getToken(self, api_key, api_secert):
        token_url = self.token_url % (api_key, api_secert)

        r_str = urllib.request.urlopen(token_url).read()
        token_data = json.loads(r_str)
        self.token_str = token_data['access_token']
        pass

    def getVoice(self, text, filename):
        get_url = self.getvoice_url % (
            urllib.parse.quote(text), self.cu_id, self.token_str)

        voice_data = urllib.request.urlopen(get_url).read()
        voice_fp = open(filename, 'wb+')
        voice_fp.write(voice_data)
        voice_fp.close()
        pass

    def getText(self, filename):
        data = {}
        data['format'] = 'wav'
        data['rate'] = 8000
        data['channel'] = 1
        data['cuid'] = self.cu_id
        data['token'] = self.token_str
        wav_fp = open(filename, 'rb')
        voice_data = wav_fp.read()
        data['len'] = len(voice_data)
        data['speech'] = base64.b64encode(voice_data).decode('utf-8')
        post_data = json.dumps(data)
        r_data = urllib.request.urlopen(
            self.upvoice_url, data=bytes(
                post_data, encoding="utf-8")).read()
        # 3.处理返回数据

        return json.loads(r_data)['result'][0]

    def speakMac(self, audio_file):
        return_code = subprocess.call(["afplay", audio_file])
        return return_code

    def speak(self, audio_file):
        import playsound 
        playsound.playsound(audio_file)

    def is_silent(self, snd_data):
        # Returns 'True' if below the 'silent' threshold
        return max(snd_data) < self.THRESHOLD

    def normalize(self, snd_data):
        # Average the volume out
        MAXIMUM = 16384
        times = float(MAXIMUM) / max(abs(i) for i in snd_data)

        r = array('h')
        for i in snd_data:
            r.append(int(i * times))
        return r

    def trim(self, snd_data):
        "Trim the blank spots at the start and end"

        def _trim(snd_data):
            snd_started = False
            r = array('h')

            for i in snd_data:
                if not snd_started and abs(i) > self.THRESHOLD:
                    snd_started = True
                    r.append(i)

                elif snd_started:
                    r.append(i)
            return r

        # Trim to the left
        snd_data = _trim(snd_data)

        # Trim to the right
        snd_data.reverse()
        snd_data = _trim(snd_data)
        snd_data.reverse()
        return snd_data

    def add_silence(self, snd_data, seconds):
        "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
        r = array('h', [0 for i in range(int(seconds * self.RATE))])
        r.extend(snd_data)
        r.extend([0 for i in range(int(seconds * self.RATE))])
        return r

    def record(self):
        """
        Record a word or words from the microphone and
        return the data as an array of signed shorts.

        Normalizes the audio, trims silence from the
        start and end, and pads with 0.5 seconds of
        blank sound to make sure VLC et al can play
        it without getting chopped off.
        """
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT, channels=1, rate=self.RATE,
                        input=True, output=True,
                        frames_per_buffer=self.CHUNK_SIZE)

        num_silent = 0
        snd_started = False

        r = array('h')

        while True:
            # little endian, signed short
            snd_data = array('h', stream.read(self.CHUNK_SIZE))
            if byteorder == 'big':
                snd_data.byteswap()
            r.extend(snd_data)

            silent = self.is_silent(snd_data)

            if silent and snd_started:
                num_silent += 1
            elif not silent and not snd_started:
                snd_started = True

            if snd_started and num_silent > 10:
                break

        sample_width = p.get_sample_size(self.FORMAT)
        stream.stop_stream()
        stream.close()
        p.terminate()

        r = self.normalize(r)
        r = self.trim(r)
        r = self.add_silence(r, 0.5)
        return sample_width, r

    def record_to_file(self, path):
        "Records from the microphone and outputs the resulting data to 'path'"
        sample_width, data = self.record()
        data = pack('<' + ('h' * len(data)), *data)

        wf = wave.open(path, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(sample_width)
        wf.setframerate(self.RATE)
        wf.writeframes(data)
        wf.close()

    def recorder(self, filename):
        self.record_to_file(filename)

