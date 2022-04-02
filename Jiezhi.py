# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 15:50:44 2022

@author: F-
"""
import PySimpleGUI as sg
import datetime

sg.theme('TanBlue')   # 设置当前主题
layout = [
    [sg.Text('排班时间： 09:00-17:00')],
    [sg.Multiline('09:00-17:00',size=(120,10), key='Paiban')],
    [sg.Text('放休时间： 11:00')],
    [sg.InputText('11:00', key='Fangxiu')],
    [sg.Button('放休')],
    [sg.Text('输出结果： ')],
    [sg.Output(size=(120, 10))],
    ]
window = sg.Window('放休工作时长计算 v1.0 by F.W.Yue', layout)
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):
        break
    PaibanList = values['Paiban']
    PaibanList = PaibanList.split('\n')
    xiutime = values['Fangxiu']
    for time in PaibanList:
        try:
            xiu_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + xiutime, '%Y-%m-%d%H:%M')
            timeL = time.split('&')
        except:
            print('放休输入有误，请检查！')
            break
        hours = 0 #上班时间
        shiji = ''#实际班次
        for timeP in timeL:
            try:
                StartTime,EndTime = timeP.split('-')
                start_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + StartTime, '%Y-%m-%d%H:%M')
                end_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + EndTime, '%Y-%m-%d%H:%M')
            except :
                print('排班输入有误，请检查！')
                break
            if start_time <= xiu_time <= end_time:
                end_time = xiu_time
                hour = end_time-start_time
                hour=(hour.seconds)/3600
                hours=hours+hour
                start_time = start_time.strftime("%H:%M")
                end_time = end_time.strftime("%H:%M")
                shijiP = start_time + '-' +end_time +'&'
                shiji = shiji+shijiP
                break
            elif xiu_time < start_time:
                    break
            hour = end_time-start_time
            hour = end_time-start_time
            hour=(hour.seconds)/3600
            hours=hours+hour
            start_time = start_time.strftime("%H:%M")
            end_time = end_time.strftime("%H:%M")
            shijiP = start_time + '-' +end_time +'&'
            shiji = shiji+shijiP
        try:
            StartTime
        except:
            continue
        if shiji =='':
            break
        elif shiji[-1] == '&':
            shiji = shiji[:-1]
        hours = round(hours,2)
        print('排: %s , 放: %s , 实: %s , 工作时长: %s 小时'%(time,xiutime,shiji,hours))

window.close()