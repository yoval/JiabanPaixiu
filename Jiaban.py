# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 10:04:43 2022

@author: Administrator

"""

import PySimpleGUI as sg
import pandas as pd
import time


#'11:00-15:00&19:00-23:00'格式转换为[11, 12, 13, 14, 19, 20, 21, 22]
def to_shijiandian(p):
    p = str(p).replace(':00', '')
    pl = p.split('&')
    h = []
    for pr in pl:
        pll = pr.split('-')
        hl = [i for i in range(int(pll[0]),int(pll[1]))]
        h=h+hl
    return h

#[11, 12, 13, 14, 19, 20, 21, 22] 格式转换为 11:00-15:00&19:00-23:00
def to_shijianduan(h):
    s = h[0]
    p = ''
    for i in range(len(h)-1):
        if h[i+1]-h[i] == 1:
            pass
        else:
            p=p+'&%s:00-%s:00'%(s,h[i]+1)
            s = h[i+1]
    p2 = '&%s:00-%s:00'%(s,h[-1]+1)
    if p2 !=p:
        p = p+p2
        p=p[1:]
    return p

sg.theme('LightBlue')
layout = [  
    [sg.Multiline('原班表姓名',size=(40,10), key='YuanNames'),sg.Multiline('原班表排班',size=(40,10), key='YuanPaiban')],
    [sg.Multiline('加班表姓名',size=(40,10), key='FangNames'),sg.Multiline('加班表时段',size=(40,10), key='FangPaiban')],
    [sg.Button('整合排班')],
    [sg.Output(size=(85, 20))],
    ]
window = sg.Window('加班排班表整合 beta 版', layout)

while True:
    event, values = window.read()
    if event in (None, 'Cancel'):
        break
    try:
        now = time.strftime("%Y-%m-%d %H-%M%S", time.localtime())
        YuanNameList = values['YuanNames'].split('\n')
        YuanPaibanList = values['YuanPaiban'].split('\n')
        FangNameList = values['FangNames'].split('\n')
        FangPaibanList = values['FangPaiban'].split('\n')
        df_Yuan = pd.DataFrame()
        df_Yuan[YuanNameList[0]] = YuanNameList[1:]
        df_Yuan[YuanPaibanList[0]] = YuanPaibanList[1:]
        try:
            df_Yuan= df_Yuan.set_index('姓名')
        except:
            print('表头必须为“姓名”!')
            continue
        
        df_Fang = pd.DataFrame()
        df_Fang[FangNameList[0]] = FangNameList[1:]
        df_Fang[FangPaibanList[0]] = FangPaibanList[1:]
        #df_Fang= df_Fang.set_index('姓名') 
    
        for df_Fang_row in df_Fang.itertuples():
            name = df_Fang_row.姓名
            if name =='':
                continue
            try:
                shiduan = df_Fang_row.时段
                df_Yuan_row = df_Yuan[df_Yuan.index.isin([name])]
                date = list(df_Yuan_row)[0]
                Yuanshiduan = df_Yuan_row.loc[name][0]
                NewShiduan = list(set((to_shijiandian(Yuanshiduan)+ to_shijiandian(shiduan))))
                NewShiduan.sort() 
                NewShiduan = to_shijianduan(NewShiduan)
                df_Yuan.at[name,date] = NewShiduan
            except Exception as e:
                if e =="'Pandas' object has no attribute '时段'":
                    print('时段列表标头必须为 时段')
                print('e')
                print('%s 班次修改错误'%name)
        df_Yuan.to_csv('加班之后的班表-%s.csv'%now,encoding="utf_8_sig",index=True)
    except:
        print('输入有误！请检查输入的数据！')
window.close()