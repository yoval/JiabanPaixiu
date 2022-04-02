# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 20:25:11 2022

@author: fuwen
"""

import PySimpleGUI as sg
import datetime,re
from pyecharts.charts import Bar
from pyecharts.charts import Line
from pyecharts import options as opts
from pyecharts.globals import ThemeType

date = datetime.datetime.now().strftime("%m{m}%d{d}").format(m='月', d='日')
sg.theme('TanBlue') 
layout = [
    [sg.Text('排班时间： 09:00-17:00')],
    [sg.Multiline('09:00-17:00',size=(120,10), key='Paiban')],
    [sg.Text('时间间隔（小时）： 0.5')],
    [sg.InputText('0.5', key='jiange')],
    [sg.Text('统计时段： 00:00-24:00')],
    [sg.InputText('00:00-24:00', key='shiduan')],
    [sg.Button('生成')],
    [sg.Text('输出结果： ')],
    [sg.Output(size=(120, 10))],
    ]
window = sg.Window('排班时段统计 v1.0 by F.W.Yue', layout)


while True:
    List = []
    event, values = window.read()
    if event in (None, 'Cancel'):
        break
    paiban = values['Paiban'] #输入的排班
    Range = values['shiduan'] #统计时段
    jiange = float(values['jiange']) #间隔
    paibanList = re.split('\n|&',paiban)
    try:
        for paibanP in paibanList:
            start,end = Range.split('-')
            StartTime,EndTime = paibanP.split('-')
            #排班开始时间
            start_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + StartTime, '%Y-%m-%d%H:%M')
            #排班结束时间
            if EndTime == '24:00':
                end_time = datetime.datetime.strptime(str(datetime.datetime.now().date()+datetime.timedelta(days=1)) + '0:00', '%Y-%m-%d%H:%M')
            else:
                end_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + EndTime, '%Y-%m-%d%H:%M')
            if end == '24:00':
                end = datetime.datetime.strptime(str(datetime.datetime.now().date()+datetime.timedelta(days=1)) + '0:00', '%Y-%m-%d%H:%M')
            else:
                end = datetime.datetime.strptime(str(datetime.datetime.now().date()) + end, '%Y-%m-%d%H:%M')    
            #计算开始时间
            start = datetime.datetime.strptime(str(datetime.datetime.now().date()) + start, '%Y-%m-%d%H:%M')
            while True:
                mid = start+datetime.timedelta(hours=jiange)
                if mid>end:
                    break
                elif start>=start_time and end_time>=mid:
                    str_start = start.strftime("%H:%M")
                    str_mid = mid.strftime("%H:%M")
                    List.append(str_start+'-'+str_mid)
                    start = mid
                else:
                    start = mid
        Set = list(set(List))
        Set.sort()
        
        bar = Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        bar.add_xaxis(Set)
        bar.add_yaxis("人数", [List.count(i) for i in Set])
        bar.set_global_opts(title_opts=opts.TitleOpts(title="排班时段柱状图", subtitle="By F.W.Yue"))
        for i in Set:
            print(i,',',List.count(i))
        bar.render(date+'bar.html')
        print('已生成柱状图……')
        
        line = Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        line.add_xaxis(Set)
        line.add_yaxis(series_name="人数",y_axis= [List.count(i) for i in Set],symbol="时间",is_symbol_show=0)
        line.set_global_opts(title_opts=opts.TitleOpts(title="排班时段折线图", subtitle="By F.W.Yue"))
        line.render(date+'Line.html')
        print('已生成折线图……')
    except:
        print('请检查输入！')

window.close()