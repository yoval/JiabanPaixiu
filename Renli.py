# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 09:44:50 2022
#https://vfl0uh2un3.feishu.cn/sheets/shtcnNB2Cy3lkrG7kVXmM1yRNHc
@author: Administrator
"""
from datetime import date
import pandas as pd

outputfloder = r'C:\Users\F-\Desktop\数据源'
#班表整合，时段人力
filepath = r'C:\Users\F-\Documents\WPS Cloud Files\993375947\抖音\考勤汇总\班表整合，时段人力.xlsx'
#日报排班表
ribaopath = r'C:\Users\F-\Documents\WPS Cloud Files\993375947\抖音\日报\日报（3月更新).xlsx'
Paiban_sheetname = '3月一线班表'
today = date.today().strftime("%Y%m%d")
#today = '20220323'
Today = pd.to_datetime(today)
DF_Renli  = pd.read_excel(filepath,sheet_name=-2)
DF_Today = DF_Renli[(DF_Renli[Today] !='休') & (DF_Renli[Today] !='外呼')] #排除今日外呼与休息班次
DF_Waihu = DF_Renli[(DF_Renli[Today] == '外呼')]
print('总体')
print(DF_Today['职场'].value_counts()) 

ban = ['早8A','早8B','天地8A','天地8B','天地9A','早10A','天地10A','天地11B','中11A','中12A','晚14A','晚15A','晚15B','早9新人']
df_Table = pd.DataFrame(index = ban)
Zhichanglist = list(set(DF_Today['职场']))
for Zhichang in Zhichanglist:
   print(Zhichang)
   DF_Zhichang = DF_Today[DF_Today['职场']==Zhichang]
   #print(DF_Zhichang[Today].value_counts())
   seri = DF_Zhichang[Today].value_counts()
   seri = seri.rename(Zhichang+'应出勤')
   df_Table = pd.concat([df_Table,seri],axis=1)
   print('-'*6)

del DF_Renli
del DF_Today

df_sjbc = pd.read_excel(ribaopath,sheet_name=Paiban_sheetname)
#df_sjbc = df_sjbc.replace('早9新人ww', '早9新人',inplace = True)
df_sjbc = df_sjbc[(df_sjbc[Today] !='休') & (df_sjbc[Today] !='外呼') ] #& (df_sjbc['职场'].notna())
print(df_sjbc['职场'].value_counts()) 
for Zhichang in Zhichanglist:
    print(Zhichang)
    DF_Zhichang = df_sjbc[df_sjbc['职场']==Zhichang]
    seri = DF_Zhichang[Today].value_counts()
    seri = seri.rename(Zhichang+'实际出勤')
    df_Table = pd.concat([df_Table,seri],axis=1)
# df[1].fillna(0,inplace=True)
df_Table = df_Table.fillna(0)
df_Table = df_Table.round(0)
df_Table = df_Table.astype('int')
col = ['蚌埠应出勤','蚌埠实际出勤','洛阳应出勤','洛阳实际出勤','徐州应出勤','徐州实际出勤','宿迁应出勤','宿迁实际出勤']
df_Table = df_Table[col]
try:
    df_Table.loc['早9新人'] = df_Table.loc['早9新人'] + df_Table.loc['早9新人ww']
except:
    pass
df_Table.loc['早9新人'] = df_Table.loc['早9新人'] + df_Table.loc['早9A']
df_Table= df_Table.drop(index='早9A')
try:
    df_Table= df_Table.drop(index=['早9新人ww','离','带教'])
except:
    df_Table= df_Table.drop(index=['离','带教'])
df_Table.to_excel(outputfloder +'\\'+ today+'-排班与出勤.xlsx',sheet_name = 'sheet1',encoding="utf_8_sig",index=True)