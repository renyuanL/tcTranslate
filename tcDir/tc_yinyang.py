#!/usr/bin/env python3
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

# Above: "tc_yinyang.py", by Renyuan Lyu (呂仁園), 2015-01-31
# Original: "yinyang.py", by Gregor Lingl. 
