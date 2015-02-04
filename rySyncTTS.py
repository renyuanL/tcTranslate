'''
rySyncTTS.py

基於雲端語音合成的 音文同步 
做出來了。
renyuan, 2015/02/02

'''
from tkinter import Text, Button
import pygame
import time
import sys
#
# 為了語法高亮，學ryViewer 引入下列 2 工具。
#
from idlelib.Percolator import Percolator
from idlelib.ColorDelegator import ColorDelegator

def main():

    x= RySyncTTS()
    x.rySync()
    x.ryQuit()

class RySyncTTS:
    def __init__(我, tx= None):

        file_mp3= '_gtts_tc_yinyang.mp3'
        if sys.platform=='darwin':
            file_mp3= '_gtts_tc_yinyang.ogg' # mac 上 pygame 不吃 .mp3，只吃.ogg
        
        L= 55560 # time length of mp3, in ms
        sumT= sum([x[2] for x in timeText])
        
        if tx==None:
            tx= Text()
            tx.pack()
            Percolator(tx).insertfilter(ColorDelegator())
        
        tx.tag_configure('highlight', background='yellow')#, relief='raised')
                
        accT= 0
        Z=[]
        for x in timeText:
            z= [x[0], x[2], accT, accT+x[2], '1.0', '1.0'] 
            # 最後2個: z[4], z[5] ， 預留給文字在螢幕上的位置 idx1, idx2
            accT += x[2]
            Z += [z]
        
        pygame.mixer.pre_init(frequency= 16000, channels=1, size=-16)
        pygame.mixer.init()
        pygame.mixer.music.load(file_mp3) #'_gtts_tc_yinyang.mp3')
        
        我.Z= Z
        我.L= L
        我.sumT= sumT
        我.tx= tx
        
    def rySync(我): # 目前來自 rySync03

        tx= 我.tx
        Z= 我.Z
        L= 我.L
        sumT= 我.sumT
                
        if len(tx.get('1.0','end'))<=1:
            tcPy= tc_yinyang_py
            tx.insert('insert',tcPy)
        
        #Y= []
        idx2= '1.0'
        for n,z in enumerate(Z):
            
            #
            # 如何 根據 text= z[0] 在 tcPy 中 「循序」找到 idx1, idx2 
            #
            text= z[0]
            idx1= tx.search(text, idx2) # idx2= '1.0' for init
            idx2= idx1 + ' + %d chars'%len(text)
            idx2= tx.index(idx2)
            
            
            #y= (idx1, idx2)

            #Z[n] += (idx1, idx2) # 這組 index 資訊就存入 Z[n][4], Z[n][5]
            Z[n][4], Z[n][5]= idx1, idx2
            
            #Y += [y]
        
        #print(Z)
        '''
        Z= [
            ('from', 3312, 0, 3312, '1.0', '1.5'), 
            ('turtle_tc', 8640, 3312, 11952, '1.5', '1.15'), 
            ('import', 3168, 11952, 15120, '1.15', '1.22'), 
            ('def', 3024, 15120, 18144, '1.22', '2.0'), 
            ('陰', 2880, 18144, 21024, '2.0', '2.2'), 
            ('半徑', 3456, 21024, 24480, '2.2', '2.5'), 
            ('顏色1', 5040, 24480, 29520, '2.5', '2.9'), 
            ('顏色2', 3888, 29520, 33408, '2.9', '3.0'),
            ...
            ]
        '''
        
        pygame.mixer.music.play()
        
        n=0
        tmpBool= True

        pos=  pygame.mixer.music.get_pos()
        while pos!=-1:

            pos=  pygame.mixer.music.get_pos() # in msec
            
            #print('pos= ',pos/L*sumT)

            # 重要音文同步計算公式
            iPos= int(pos/L*sumT) # 這就是我說的「正比關係」！！
            
            if n<len(Z):
                if iPos>=Z[n][2] and iPos<=Z[n][3] and tmpBool==True:

                    if n>=1:
                        tx.tag_remove('highlight',Z[n-1][4],Z[n-1][5])
                    tx.tag_add('highlight',Z[n][4],Z[n][5])
                    
                    tx.see(Z[n][5]) # 加這行，才能自動捲軸。
                    tx.update()     # 加這行，才能即時顯示效果。
                    
                    tmpBool= False
                    
                elif iPos >= Z[n][3]:
                    n+=1
                    tmpBool= True
        
    def ryQuit(我):
        pygame.mixer.music.stop()
        pygame.mixer.quit()

def main00():

    Z=[] 
    # 這個 Z 存放音文同步資訊(進一步處理)，
    # 將在 ryShowText 中設定，rySync01 中使用。
    
    file_mp3= '_gtts_tc_yinyang.mp3'
    L= 55560 # time length of mp3, in ms
    #
    # 這個 L 是 file_mp3 的 時間長度，還不知道如何自動找出來，
    # 目前是用 ryPlay() 先 播放一次，找到 lastPos 記錄下來得知。
    # 可能有點不準，自動方法要再研究。
    #
    
    sumT= sum([x[2] for x in timeText])
    #
    # 這個 timeText 來自 ryGoogleTTS.py，
    # 從那邊跑出結果，再貼進來這裡，
    # 半手動半自動做些字串處理
    #
    # sumT=  221472
    # print('sumT= ', sumT)
    #
    # 這個 sumT 是 從ryGoogleTTS.py 弄回來的 mp3 之檔案長度 (in bytes)
    #
    # 我覺得 L 與 sumT 應該有正比關係，經過1天的實驗，果然如此。
    #

    #
    # 學會 tkinter.Text 的 高亮 (highlight) 技巧，
    # 再配合 pygame.mixer.music 的播放聲音(mp3)
    # 於是音文同步就做出來了。
    #
    tx= Text()
    tx.pack()
    tx.tag_configure('highlight', background='yellow')#, relief='raised')
    #
    # 把 文字的第5列，從頭(0)到尾(end)加標籤，此處標籤意指高亮(底色變黃)
    # 方法如下2行
    #
    # tx.tag_add('highlight','5.0','5.end')
    # tx.tag_remove('highlight','5.0','5.end')
    #
    # 上述方法 參考這裡很多，http://www.tkdocs.com/tutorial/text.html
    #
    
    # 讓 程式內文 有 語法 顏色，超酷的！
    Percolator(tx).insertfilter(ColorDelegator())

    def ryMain():
    
        ryShowText()
        ryInit()
        #rySync01()
        #rySync02()
        rySync03()
        
        setButtons()
        
    def ryShowText():
        nonlocal Z

        tx.delete('1.0','end')
        
        accT= 0
        Z=[]
        for x in timeText:
            z= [x[0], x[2], accT, accT+x[2], '1.0', '1.0'] 
            # 最後2個: z[4], z[5] ， 預留給文字在螢幕上的位置 idx1, idx2
            accT += x[2]
            Z += [z]
        
        ''' Z=[
            ('from', 3312, 0, 3312),
            ('turtle_tc', 8640, 3312, 11952),
            ('import', 3168, 11952, 15120),
            ('def', 3024, 15120, 18144),
            ('陰', 2880, 18144, 21024),
            ('半徑', 3456, 21024, 24480),
            ('顏色1', 5040, 24480, 29520),
            ('顏色2', 3888, 29520, 33408),
            ...
            ]
        '''
        
        '''
        for n,z in enumerate(Z):
        
            #text= '%s:%04d:%s:%d\n'%(idx,n,z[0],len(z[0]))#'%s'%(z[0])
            text= '%s\n'%(str(z))
            tx.insert('end','%s'%(text))
        '''
        
        text= tc_yinyang_py
        tx.insert('end',text)
            
    def ryHighLight():
        nonlocal Z
        tx.delete('1.0','end')
        
        Y= []

        for n,z in enumerate(Z):
        
            #text= '%s:%04d:%s:%d\n'%(idx,n,z[0],len(z[0]))#'%s'%(z[0])
            xxxx= '\n' if n%4==0 else '\t'
            text= '%s%s'%(z[0],xxxx)
            
            idx1= tx.index('insert')
            tx.insert('insert',text)            
            idx2= tx.index('insert')
            
            y= (text, idx1, idx2)
            
            Y += [y]
        
        #print(Y)
            
        for i,y in enumerate(Y):

            idx1= y[1]
            idx2= y[2]
            
            tx.tag_add('highlight',idx1,idx2)
            tx.see(idx1)
            tx.update()
            
            time.sleep(0.5)
            
            tx.tag_remove('highlight',idx1,idx2)
            tx.update()
            
    def ryInit():
        nonlocal file_mp3
        
        pygame.mixer.pre_init(frequency= 16000, channels=1, size=-16)
        pygame.mixer.init()
        pygame.mixer.music.load(file_mp3) #'_gtts_tc_yinyang.mp3')
    
    def ryPlay():
        pygame.mixer.music.play()
        pos=  pygame.mixer.music.get_pos()
        lastPos= pos
        while pos != -1:
            pos=  pygame.mixer.music.get_pos()
            if pos != -1: lastPos= pos
            if pos%1000==0:
                ryPos(pos)

        tx.delete('1.0','1.end')
        tx.insert('1.0','lastPos= %d'%int(lastPos))
        tx.update()

    def ryPos(pos=0):
        if pos!=0: pos=  pygame.mixer.music.get_pos()
        tx.delete('1.0','1.end')
        tx.insert('1.0','%d'%int(pos))
        tx.update()

    def rySync01(): # 這裡還有很多其他改的空間，故名稱加上 01
        nonlocal Z

        for n,z in enumerate(Z):
            idx='%d.0'%(n+1)
            
            #text= '%s:%04d:%s:%d\n'%(idx,n,z[0],len(z[0]))#'%s'%(z[0])
            text= '%s\n'%(z[0])
            
            tx.insert(idx,'%s'%(text))
            
        pygame.mixer.music.play()
        
        n=0
        tmpBool= True
        #busy= pygame.mixer.music.get_busy()
        pos=  pygame.mixer.music.get_pos()
        while pos!=-1:#busy: # pos 正常情形會傳回聲音的時間位置(ms)，聲音結束時，pos==-1
            #busy= pygame.mixer.music.get_busy()
            pos=  pygame.mixer.music.get_pos() # in msec
            
            #print('pos= ',pos/L*sumT)

            iPos= int(pos/L*sumT) # 這就是我說的「正比關係」！！
            
            if n<len(Z):
                if iPos>=Z[n][2] and iPos<=Z[n][3] and tmpBool==True:

                    #print(Z[n][0], iPos)
                    
                    #tx.delete('1.0','1.end')
                    #tx.insert('1.0','%s'%(Z[n][0]))
                    
                    #
                    # 目前先採用「整行高亮」的方式，
                    # 隨後再改成依照文字排版的方式來高亮
                    #

                    if n>=1:
                        tx.tag_remove('highlight','%d.0'%(n),'%d.end'%(n))
                    tx.tag_add('highlight','%d.0'%(n+1),'%d.end'%(n+1))
                    tx.see('%d.0'%(n+1)) # 加這行，才能自動捲軸。
                    tx.update()
                    
                    tmpBool= False
                    
                elif iPos >= Z[n][3]:
                    n+=1
                    tmpBool= True

    def rySync02(): # 這裡還有很多其他改的空間，故名稱加上 02
        nonlocal Z

        tx.delete('1.0','end')
        
        #
        # 把文字依 「某種格式」 擺在 螢幕上，其位置存入 Z[4], Z[5]
        #
        # 參考:  Text widget indices
        # http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/text-index.html
        #
        # idx= 'line.column'
        #
        # tk.INSERT
        #   The position of the insertion cursor in the text widget. 
        #   This constant is equal to the string 'insert'.
        #
        
        #Y= []
        for n,z in enumerate(Z):
        
            #
            # 暫時假設文字格式為 每列 (line) 4 個 text
            #
            xxxx= '\n' if (n+1)%4==0 else '\t'
            text= '%s%s'%(z[0],xxxx)
            
            #
            # 一邊把文字插入 tx, 一邊記錄其在螢幕上的位置 idx1, idx2
            #
            idx1= tx.index('insert')
            tx.insert('insert',text)            
            idx2= tx.index('insert')
            
            #y= (idx1, idx2)
            #Z[n] += (idx1, idx2) # 這組 index 資訊就存入 Z[n][4], Z[n][5]
            Z[n][4], Z[n][5]= idx1, idx2
            
            #Y += [y]
        
        #print(Z)
        '''
        Z= [
            ('from', 3312, 0, 3312, '1.0', '1.5'), 
            ('turtle_tc', 8640, 3312, 11952, '1.5', '1.15'), 
            ('import', 3168, 11952, 15120, '1.15', '1.22'), 
            ('def', 3024, 15120, 18144, '1.22', '2.0'), 
            ('陰', 2880, 18144, 21024, '2.0', '2.2'), 
            ('半徑', 3456, 21024, 24480, '2.2', '2.5'), 
            ('顏色1', 5040, 24480, 29520, '2.5', '2.9'), 
            ('顏色2', 3888, 29520, 33408, '2.9', '3.0'),
            ...
            ]
        '''
        
        pygame.mixer.music.play()
        
        n=0
        tmpBool= True

        pos=  pygame.mixer.music.get_pos()
        while pos!=-1:

            pos=  pygame.mixer.music.get_pos() # in msec
            
            #print('pos= ',pos/L*sumT)

            # 重要音文同步計算公式
            iPos= int(pos/L*sumT) # 這就是我說的「正比關係」！！
            
            if n<len(Z):
                if iPos>=Z[n][2] and iPos<=Z[n][3] and tmpBool==True:

                    if n>=1:
                        tx.tag_remove('highlight',Z[n-1][4],Z[n-1][5])
                    tx.tag_add('highlight',Z[n][4],Z[n][5])
                    
                    tx.see(Z[n][5]) # 加這行，才能自動捲軸。
                    tx.update()     # 加這行，才能即時顯示效果。
                    
                    tmpBool= False
                    
                elif iPos >= Z[n][3]:
                    n+=1
                    tmpBool= True
 

    def rySync03(): # 這裡還有很多其他改的空間，故名稱加上 03
        nonlocal Z

        tx.delete('1.0','end')
        
        #
        # 把文字依 「某種格式」 擺在 螢幕上，其位置存入 Z[4], Z[5]
        #
        # 參考:  Text widget indices
        # http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/text-index.html
        #
        # idx= 'line.column'
        #
        # tk.INSERT
        #   The position of the insertion cursor in the text widget. 
        #   This constant is equal to the string 'insert'.
        #
        
        tcPy= tc_yinyang_py
        tx.insert('insert',tcPy)
        
        #Y= []
        idx2= '1.0'
        for n,z in enumerate(Z):
            '''
            #
            # 暫時假設文字格式為 每列 (line) 4 個 text
            #
            xxxx= '\n' if (n+1)%10==0 else '\t'
            text= '%s%s'%(z[0],xxxx)
            
            #
            # 一邊把文字插入 tx, 一邊記錄其在螢幕上的位置 idx1, idx2
            #
            idx1= tx.index('insert')
            tx.insert('insert',text)            
            idx2= tx.index('insert')
            '''
            
            #
            # 如何 根據 text= z[0] 在 tcPy 中 「循序」找到 idx1, idx2 
            #
            text= z[0]
            idx1= tx.search(text, idx2) # idx2= '1.0' for init
            idx2= idx1 + ' + %d chars'%len(text)
            idx2= tx.index(idx2)
            
            
            #y= (idx1, idx2)

            #Z[n] += (idx1, idx2) # 這組 index 資訊就存入 Z[n][4], Z[n][5]
            Z[n][4], Z[n][5]= idx1, idx2
            
            #Y += [y]
        
        #print(Z)
        '''
        Z= [
            ('from', 3312, 0, 3312, '1.0', '1.5'), 
            ('turtle_tc', 8640, 3312, 11952, '1.5', '1.15'), 
            ('import', 3168, 11952, 15120, '1.15', '1.22'), 
            ('def', 3024, 15120, 18144, '1.22', '2.0'), 
            ('陰', 2880, 18144, 21024, '2.0', '2.2'), 
            ('半徑', 3456, 21024, 24480, '2.2', '2.5'), 
            ('顏色1', 5040, 24480, 29520, '2.5', '2.9'), 
            ('顏色2', 3888, 29520, 33408, '2.9', '3.0'),
            ...
            ]
        '''
        
        pygame.mixer.music.play()
        
        n=0
        tmpBool= True

        pos=  pygame.mixer.music.get_pos()
        while pos!=-1:

            pos=  pygame.mixer.music.get_pos() # in msec
            
            #print('pos= ',pos/L*sumT)

            # 重要音文同步計算公式
            iPos= int(pos/L*sumT) # 這就是我說的「正比關係」！！
            
            if n<len(Z):
                if iPos>=Z[n][2] and iPos<=Z[n][3] and tmpBool==True:

                    if n>=1:
                        tx.tag_remove('highlight',Z[n-1][4],Z[n-1][5])
                    tx.tag_add('highlight',Z[n][4],Z[n][5])
                    
                    tx.see(Z[n][5]) # 加這行，才能自動捲軸。
                    tx.update()     # 加這行，才能即時顯示效果。
                    
                    tmpBool= False
                    
                elif iPos >= Z[n][3]:
                    n+=1
                    tmpBool= True
  
    def ryQuit():
        pygame.mixer.music.stop()
        pygame.mixer.quit()

    def setButtons():
        
        bnShowText=  Button(text= 'ryShowText',  command= ryShowText)
        bnHighLight= Button(text= 'ryHighLight', command= ryHighLight)
        bnInit=      Button(text= 'ryInit',      command= ryInit)
        bnQuit=      Button(text= 'ryQuit',      command= ryQuit)
        bnPlay=      Button(text= 'ryPlay',      command= ryPlay)
        bnSync01=    Button(text= 'rySync01',    command= rySync01)
        bnSync02=    Button(text= 'rySync02',    command= rySync02)
        bnSync03=    Button(text= 'rySync03',    command= rySync03)


        bnShowText.pack( side='left')
        bnHighLight.pack(side='left')
        bnInit.pack(     side='left')
        bnQuit.pack(     side='left')
        bnPlay.pack(     side='left')
        bnSync01.pack(   side='left')
        bnSync02.pack(   side='left')
        bnSync03.pack(   side='left')


    #########################
    ryMain() # 真正執行在此。
    #########################


#----------------------------------------------------------------

#
# 這是從 ryGoogleTTS.py 剪貼過來的。
#
tc_yinyang_timedText= '''
('from', 'en'), byteNum=  3312
('turtle_tc', 'en'), byteNum=  8640
('import', 'en'), byteNum=  3168
('def', 'en'), byteNum=  3024
('陰', 'zh-tw'), byteNum=  2880
('半徑', 'zh-tw'), byteNum=  3456
('顏色1', 'zh-tw'), byteNum=  5040
('顏色2', 'zh-tw'), byteNum=  3888
('筆寬', 'zh-tw'), byteNum=  3888
('顏色', 'zh-tw'), byteNum=  4176
('黑', 'zh-tw'), byteNum=  2736
('顏色1', 'zh-tw'), byteNum=  5040
('開始填', 'zh-tw'), byteNum=  4752
('畫圓', 'zh-tw'), byteNum=  4032
('半徑', 'zh-tw'), byteNum=  3456
('畫圓', 'zh-tw'), byteNum=  4032
('半徑', 'zh-tw'), byteNum=  3456
('左轉', 'zh-tw'), byteNum=  3744
('畫圓', 'zh-tw'), byteNum=  4032
('半徑', 'zh-tw'), byteNum=  3456
('結束填', 'zh-tw'), byteNum=  4896
('左轉', 'zh-tw'), byteNum=  3744
('提筆', 'zh-tw'), byteNum=  3456
('前進', 'zh-tw'), byteNum=  4320
('半徑', 'zh-tw'), byteNum=  3456
('右轉', 'zh-tw'), byteNum=  4032
('下筆', 'zh-tw'), byteNum=  3888
('顏色', 'zh-tw'), byteNum=  4176
('顏色1', 'zh-tw'), byteNum=  5040
('顏色2', 'zh-tw'), byteNum=  3888
('開始填', 'zh-tw'), byteNum=  4752
('畫圓', 'zh-tw'), byteNum=  4032
('半徑', 'zh-tw'), byteNum=  3456
('結束填', 'zh-tw'), byteNum=  4896
('左轉', 'zh-tw'), byteNum=  3744
('提筆', 'zh-tw'), byteNum=  3456
('後退', 'zh-tw'), byteNum=  3744
('半徑', 'zh-tw'), byteNum=  3456
('下筆', 'zh-tw'), byteNum=  3888
('左轉', 'zh-tw'), byteNum=  3744
('def', 'en'), byteNum=  3024
('主函數', 'zh-tw'), byteNum=  4752
('重設', 'zh-tw'), byteNum=  3888
('陰', 'zh-tw'), byteNum=  2880
('黑', 'zh-tw'), byteNum=  2736
('白', 'zh-tw'), byteNum=  2880
('陰', 'zh-tw'), byteNum=  2880
('白', 'zh-tw'), byteNum=  2880
('黑', 'zh-tw'), byteNum=  2736
('藏龜', 'zh-tw'), byteNum=  4320
('return', 'en'), byteNum=  3456
('if', 'en'), byteNum=  1728
('__name__', 'en'), byteNum=  13536
('主函數', 'zh-tw'), byteNum=  4752
('主迴圈', 'zh-tw'), byteNum=  4752
'''

#
# 手動加自動整理成如下，就當作本程式的基底資料。
#

'''
x= tc_yinyang_timedText.replace('byteNum=','')
x= x.replace(')','')
x= x.replace('\n','),\n')
xL= x.split('\n')
for y in xL:
    print(y)
'''

timeText= [
    ('from', 'en',   3312),
    ('turtle_tc', 'en',   8640),
    ('import', 'en',   3168),
    ('def', 'en',   3024),
    ('陰', 'zh-tw',   2880),
    ('半徑', 'zh-tw',   3456),
    ('顏色1', 'zh-tw',   5040),
    ('顏色2', 'zh-tw',   3888),
    ('筆寬', 'zh-tw',   3888),
    ('顏色', 'zh-tw',   4176),
    ('黑', 'zh-tw',   2736),
    ('顏色1', 'zh-tw',   5040),
    ('開始填', 'zh-tw',   4752),
    ('畫圓', 'zh-tw',   4032),
    ('半徑', 'zh-tw',   3456),
    ('畫圓', 'zh-tw',   4032),
    ('半徑', 'zh-tw',   3456),
    ('左轉', 'zh-tw',   3744),
    ('畫圓', 'zh-tw',   4032),
    ('半徑', 'zh-tw',   3456),
    ('結束填', 'zh-tw',   4896),
    ('左轉', 'zh-tw',   3744),
    ('提筆', 'zh-tw',   3456),
    ('前進', 'zh-tw',   4320),
    ('半徑', 'zh-tw',   3456),
    ('右轉', 'zh-tw',   4032),
    ('下筆', 'zh-tw',   3888),
    ('顏色', 'zh-tw',   4176),
    ('顏色1', 'zh-tw',   5040),
    ('顏色2', 'zh-tw',   3888),
    ('開始填', 'zh-tw',   4752),
    ('畫圓', 'zh-tw',   4032),
    ('半徑', 'zh-tw',   3456),
    ('結束填', 'zh-tw',   4896),
    ('左轉', 'zh-tw',   3744),
    ('提筆', 'zh-tw',   3456),
    ('後退', 'zh-tw',   3744),
    ('半徑', 'zh-tw',   3456),
    ('下筆', 'zh-tw',   3888),
    ('左轉', 'zh-tw',   3744),
    ('def', 'en',   3024),
    ('主函數', 'zh-tw',   4752),
    ('重設', 'zh-tw',   3888),
    ('陰', 'zh-tw',   2880),
    ('黑', 'zh-tw',   2736),
    ('白', 'zh-tw',   2880),
    ('陰', 'zh-tw',   2880),
    ('白', 'zh-tw',   2880),
    ('黑', 'zh-tw',   2736),
    ('藏龜', 'zh-tw',   4320),
    ('return', 'en',   3456),
    ('if', 'en',   1728),
    ('__name__', 'en',   13536),
    ('主函數', 'zh-tw',   4752),
    ('主迴圈', 'zh-tw',   4752)
    ]

tc_yinyang_py= """#!/usr/bin/env python3
'''龜作圖範例集：

            tdemo_yinyang.py

另一種繪畫適合作為初學者的
程式設計實例。

小圓圈的圓形畫
命令。=== 以上由 Google 翻譯，請協助改善 ===
'''

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

# Above: "tc_yinyang.py", by Renyuan Lyu (呂仁園), 2015-02-02
# Original: "yinyang.py", by Gregor Lingl. 
"""
    
    
    
if __name__=='__main__':
    main()
