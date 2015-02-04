'''
ryGoogleTTS.py

2015/01/29

'''
import io
import tokenize as tn

def main():

    '''
    x= gTTS(text= aPyText, lang= 'zh-tw')        
    playIt()
    '''
    
    fp= io.StringIO(tc_yinyang)

    tokenL= [ x for x in tn.generate_tokens(fp.readline) ]

    ttsIt(tokenL, langAnother= 'zh-tw')
    
    playIt()
    
            
def ttsIt00(tokenL, savefile= '_gtts.mp3', langAnother= 'zh-tw'):
    """ Do the Web request and save to `savefile` """

    GOOGLE_TTS_URL= 'http://translate.google.com/translate_tts'
    #MAX_CHARS= 100 # Max characters the Google TTS API takes at a time
    
    textL= [t.string for t in tokenL if t.type == tn.NAME]

    textlangL= []
    for text in textL:
        lang= 'en' if all([ord(x)<=0x7f for x in text]) else langAnother #'ja' #'zh-tw'
        textlangL += [(text, lang)]
    
    f= open(savefile, 'wb')

    for idx, textlang in enumerate(textlangL):

        print(idx, textlang)
        
        text, lang= textlang
        
        payload = { 'ie': 'utf-8',
                    'tl': lang,
                    'q':  text,
                    'total': len(textlangL),
                    'idx':   idx,
                    'textlen': len(text) }
        try:
            r= requests.get(GOOGLE_TTS_URL, params= payload)
            
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)

        except Exception as e:
            raise
    f.close()
    print('ttsIt--> %s'%savefile)


def ttsIt(tokenL, savefile= '_gtts.mp3', langAnother= 'zh-tw'):
    """ Do the Web request and save to `savefile` """

    GOOGLE_TTS_URL= 'http://translate.google.com/translate_tts'
    #MAX_CHARS= 100 # Max characters the Google TTS API takes at a time
    
    textL= [t.string for t in tokenL if t.type == tn.NAME]

    textlangL= []
    for text in textL:
        lang= 'en' if all([ord(x)<=0x7f for x in text]) else langAnother #'ja' #'zh-tw'
        textlangL += [(text, lang)]
    
    f= open(savefile, 'wb')

    for idx, textlang in enumerate(textlangL):

        print(idx, textlang, end= ', ')
        
        text, lang= textlang
        
        payload = { 'ie': 'utf-8',
                    'tl': lang,
                    'q':  text,
                    'total': len(textlangL),
                    'idx':   idx,
                    'textlen': len(text) }
        try:
            r= requests.get(GOOGLE_TTS_URL, params= payload)
            #
            byteNum= len(r.content)
            print('byteNum= ', byteNum)
            # 代表 byte 數，不知能否與時間長度成正比？
            # 若可，音文同步就做出來了！
            #
            f.write(r.content) # 可能就可以，
            #
            # 但要預防 它 太大， 故用 iter_content(), 
            # 設定 1024 bytes 為 1個 chunk
            #
            # 也可分成小檔儲存，但數量太多，檔案管理不易。
            # 為了 debug 倒是小檔較方便。
            #
            '''
            fn= '%s%04d.mp3'%(savefile.replace('.mp3',''),idx)
            fp= open(fn,'wb')
            
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)
                fp.write(chunk)
            
            fp.close()
            '''

        except Exception as e:
            raise
    f.close()
    print('ttsIt--> %s'%savefile)


    
tc_yinyang_timedText= '''
>>> 
0 ('from', 'en'), byteNum=  3312
1 ('turtle_tc', 'en'), byteNum=  8640
2 ('import', 'en'), byteNum=  3168
3 ('def', 'en'), byteNum=  3024
4 ('陰', 'zh-tw'), byteNum=  2880
5 ('半徑', 'zh-tw'), byteNum=  3456
6 ('顏色1', 'zh-tw'), byteNum=  5040
7 ('顏色2', 'zh-tw'), byteNum=  3888
8 ('筆寬', 'zh-tw'), byteNum=  3888
9 ('顏色', 'zh-tw'), byteNum=  4176
10 ('黑', 'zh-tw'), byteNum=  2736
11 ('顏色1', 'zh-tw'), byteNum=  5040
12 ('開始填', 'zh-tw'), byteNum=  4752
13 ('畫圓', 'zh-tw'), byteNum=  4032
14 ('半徑', 'zh-tw'), byteNum=  3456
15 ('畫圓', 'zh-tw'), byteNum=  4032
16 ('半徑', 'zh-tw'), byteNum=  3456
17 ('左轉', 'zh-tw'), byteNum=  3744
18 ('畫圓', 'zh-tw'), byteNum=  4032
19 ('半徑', 'zh-tw'), byteNum=  3456
20 ('結束填', 'zh-tw'), byteNum=  4896
21 ('左轉', 'zh-tw'), byteNum=  3744
22 ('提筆', 'zh-tw'), byteNum=  3456
23 ('前進', 'zh-tw'), byteNum=  4320
24 ('半徑', 'zh-tw'), byteNum=  3456
25 ('右轉', 'zh-tw'), byteNum=  4032
26 ('下筆', 'zh-tw'), byteNum=  3888
27 ('顏色', 'zh-tw'), byteNum=  4176
28 ('顏色1', 'zh-tw'), byteNum=  5040
29 ('顏色2', 'zh-tw'), byteNum=  3888
30 ('開始填', 'zh-tw'), byteNum=  4752
31 ('畫圓', 'zh-tw'), byteNum=  4032
32 ('半徑', 'zh-tw'), byteNum=  3456
33 ('結束填', 'zh-tw'), byteNum=  4896
34 ('左轉', 'zh-tw'), byteNum=  3744
35 ('提筆', 'zh-tw'), byteNum=  3456
36 ('後退', 'zh-tw'), byteNum=  3744
37 ('半徑', 'zh-tw'), byteNum=  3456
38 ('下筆', 'zh-tw'), byteNum=  3888
39 ('左轉', 'zh-tw'), byteNum=  3744
40 ('def', 'en'), byteNum=  3024
41 ('主函數', 'zh-tw'), byteNum=  4752
42 ('重設', 'zh-tw'), byteNum=  3888
43 ('陰', 'zh-tw'), byteNum=  2880
44 ('黑', 'zh-tw'), byteNum=  2736
45 ('白', 'zh-tw'), byteNum=  2880
46 ('陰', 'zh-tw'), byteNum=  2880
47 ('白', 'zh-tw'), byteNum=  2880
48 ('黑', 'zh-tw'), byteNum=  2736
49 ('藏龜', 'zh-tw'), byteNum=  4320
50 ('return', 'en'), byteNum=  3456
51 ('if', 'en'), byteNum=  1728
52 ('__name__', 'en'), byteNum=  13536
53 ('主函數', 'zh-tw'), byteNum=  4752
54 ('主迴圈', 'zh-tw'), byteNum=  4752
ttsIt--> _gtts.mp3
playIt: _gtts.mp3
>>> 
'''

tc_yinyang= '''
from turtle_tc import *

def 陰(半徑, 顏色1, 顏色2):
    筆寬(3)
    顏色(黑, 顏色1)
    開始填()
    畫圓(半徑/2., 180)
    畫圓(半徑, 180)
    左轉(180)
    畫圓(-半徑/2., 180)
    結束填()
    左轉(90)
    提筆()
    前進(半徑*0.35)
    右轉(90)
    下筆()
    顏色(顏色1, 顏色2)
    開始填()
    畫圓(半徑*0.15)
    結束填()
    左轉(90)
    提筆()
    後退(半徑*0.35)
    下筆()
    左轉(90)

def 主函數():
    重設()
    陰(200, 黑, 白)
    陰(200, 白, 黑)
    藏龜()
    return "Done!"

if __name__ == '__main__':
    主函數()
    主迴圈()
'''

en_yinyang= '''
from turtle import *

def yin(radius, color1, color2):
    width(3)
    color("black", color1)
    begin_fill()
    circle(radius/2., 180)
    circle(radius, 180)
    left(180)
    circle(-radius/2., 180)
    end_fill()
    left(90)
    up()
    forward(radius*0.35)
    right(90)
    down()
    color(color1, color2)
    begin_fill()
    circle(radius*0.15)
    end_fill()
    left(90)
    up()
    backward(radius*0.35)
    down()
    left(90)

def main():
    reset()
    yin(200, "black", "white")
    yin(200, "white", "black")
    ht()
    return "Done!"

if __name__ == '__main__':
    main()
    mainloop()
'''

jp_yinyang= '''
from turtle_jp import *

def 陰(半径, カラー1, カラー2):
    幅(3)
    色(黒, カラー1)
    塗りつぶしを開始()
    サークル(半径/2., 180)
    サークル(半径, 180)
    左(180)
    サークル(-半径/2., 180)
    エンド·フィル()
    左(90)
    アップ()
    フォワード(半径*0.35)
    右(90)
    ダウン()
    色(カラー1, カラー2)
    塗りつぶしを開始()
    サークル(半径*0.15)
    エンド·フィル()
    左(90)
    アップ()
    後方(半径*0.35)
    ダウン()
    左(90)

def メイン():
    リセット()
    陰(200, 黒, 白)
    陰(200, 白, 黒)
    ハイチ()
    return "やった！"

if __name__ == '__main__':
    メイン()
    メインループ()
'''

def main00():

    text1= '''
        Beautiful is better than ugly.
        Explicit is better than implicit.
        Simple is better than complex.
        Complex is better than complicated.
        Flat is better than nested.
        Sparse is better than dense.
        Readability counts.
        '''
    text2= '''
        漂亮的比醜陋的好。
        明確優於隱式。
        簡單比複雜好。
        複雜比複雜好。
        扁平比嵌套要好。
        稀疏比密集要好。
        可讀性計數。
        '''
    text3= '''
        美しいは醜いよりも優れています。
        明示的、暗黙的よりも優れています。
        シンプルは複雑よりも優れています。
        複合体は、複雑よりも優れています。
        フラットは、ネストされたよりも優れています。
        スパースが密集よりも優れています。
        可読性カウント。
        '''
    texts= [(text1,'en'), (text2, 'zh-tw'), (text3,'ja')]
    
    for text, lang in texts:

        print('text= %s\nlang= %s\n'%(text,lang))
        
        x= gTTS(text, lang)
        
        playIt()



import pygame, os                

def playIt00(audio_file= "_gtts.mp3"):
    
    print('playIt: %s'%audio_file)

    import sys    
    if sys.platform == 'darwin': # mac 上的 pygame 無法撥放 mp3，額外處理一下。
        import subprocess
        #subprocess.call(["afplay", audio_file]) # 這行會鎖住
        subprocess.Popen(["afplay", audio_file], 
            stdin= subprocess.PIPE,
            stdout= subprocess.PIPE)
  
    else:# elif sys.platform == 'win32':

        #pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffersize=4096)
        pygame.mixer.pre_init(frequency=16000, size=-16, channels=1)
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

import sys 
import subprocess

def playIt(audio_file= "_gtts.mp3"):
           
    if sys.platform == 'darwin': # mac 上的 pygame 無法撥放 mp3，額外處理一下。
   
        oggFile= audio_file.replace('.mp3','.ogg')
        if os.path.exists(oggFile):
            subprocess.call(['rm',oggFile])

        subprocess.call(["/usr/local/bin/ffmpeg", "-i", audio_file, "-f", "ogg", oggFile])
        
        audio_file= oggFile

    print('playIt: %s'%audio_file)  
    
    #pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffersize=4096)
    pygame.mixer.pre_init(frequency=16000, size=-16, channels=1)
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

def stopIt():
    pygame.mixer.music.stop()
def pauseIt():
    pygame.mixer.music.pause()
def unpauseIt():
    pygame.mixer.music.unpause()
def rewindIt():
    pygame.mixer.music.rewind()    

def quitIt():
    pygame.mixer.music.stop()
    pygame.mixer.quit() 
    # 上行必須執行，否則開啟的 mp3 檔沒有關閉，隨後就不能再寫進去。
    # 但是...在哪裡呼叫它呢？再想想！


    
#-----------------------------------------------
# thanks to https://github.com/pndurette/gTTS
#-----------------------------------------------
#
# also need "requests"
#
# http://docs.python-requests.org
#

import requests

import re


class gTTS:
    """ gTTS (Google Text to Speech): an interface to Google's Text to Speech API """

    GOOGLE_TTS_URL = 'http://translate.google.com/translate_tts'
    MAX_CHARS = 100 # Max characters the Google TTS API takes at a time
    LANGUAGES = {
        'af' : 'Afrikaans',
        'sq' : 'Albanian',
        'ar' : 'Arabic',
        'hy' : 'Armenian',
        'ca' : 'Catalan',
        'zh-cn' : 'Mandarin (simplified)',
        'zh-tw' : 'Mandarin (traditional)',
        'hr' : 'Croatian',
        'cs' : 'Czech',
        'da' : 'Danish',
        'nl' : 'Dutch',
        'en' : 'English',
        'en-us' : 'English (United States)',
        'en-au' : 'English (Australia)',
        'eo' : 'Esperanto',
        'fi' : 'Finnish',
        'fr' : 'French',
        'de' : 'German',
        'el' : 'Greek',
        'ht' : 'Haitian Creole',
        'hi' : 'Hindi',
        'hu' : 'Hungarian',
        'is' : 'Icelandic',
        'id' : 'Indonesian',
        'it' : 'Italian',
        'ja' : 'Japanese',
        'ko' : 'Korean',
        'la' : 'Latin',
        'lv' : 'Latvian',
        'mk' : 'Macedonian',
        'no' : 'Norwegian',
        'pl' : 'Polish',
        'pt' : 'Portuguese',
        'ro' : 'Romanian',
        'ru' : 'Russian',
        'sr' : 'Serbian',
        'sk' : 'Slovak',
        'es' : 'Spanish',
        'sw' : 'Swahili',
        'sv' : 'Swedish',
        'ta' : 'Tamil',
        'th' : 'Thai',
        'tr' : 'Turkish',
        'vi' : 'Vietnamese',
        'cy' : 'Welsh'
    }

    def __init__(self, text= 'Hello, world.', lang= 'en', debug = False):
        self.debug = debug
        if lang not in self.LANGUAGES:
            raise Exception('Language not supported: %s' % lang)
        else:
            self.lang = lang

        if not text:
            raise Exception('No text to speak')
        else:
            self.text = text

        # Split text in parts
        if len(text) <= self.MAX_CHARS: 
            text_parts = [text]
        else:
            text_parts = self._tokenize(text, self.MAX_CHARS)           

        # Clean
        def strip(x): return x.replace('\n', '').strip()
        text_parts = [strip(x) for x in text_parts]
        text_parts = [x for x in text_parts if len(x) > 0]
        self.text_parts = text_parts

        self.save() # ry added

    def save(self, savefile= '_gtts.mp3'):
        """ Do the Web request and save to `savefile` """
        with open(savefile, 'wb') as f:
            for idx, part in enumerate(self.text_parts):
                payload = { 'ie' : 'UTF-8',
                            'tl' : self.lang,
                            'q' : part,
                            'total' : len(self.text_parts),
                            'idx' : idx,
                            'textlen' : len(part) }
                if self.debug: print(payload)
                try:
                    r = requests.get(self.GOOGLE_TTS_URL, params=payload)
                    for chunk in r.iter_content(chunk_size=1024):
                        f.write(chunk)
                except Exception as e:
                    raise

    def _tokenize(self, text, max_size):
        """ Tokenizer on basic roman punctuation """ 
        
        punc = "¡!()[]¿?.,;:—«»\n"
        punc_list = [re.escape(c) for c in punc]
        pattern = '|'.join(punc_list)
        parts = re.split(pattern, text)

        min_parts = []
        for p in parts:
            min_parts += self._minimize(p, " ", max_size)
        return min_parts

    def _minimize(self, thestring, delim, max_size):
        """ Recursive function that splits `thestring` in chunks
        of maximum `max_size` chars delimited by `delim`. Returns list. """ 
        
        if len(thestring) > max_size:
            idx = thestring.rfind(delim, 0, max_size)
            return [thestring[:idx]] + self._minimize(thestring[idx:], delim, max_size)
        else:
            return [thestring]

if __name__ == "__main__":  main() # this is the last line
