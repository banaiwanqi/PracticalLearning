#导入必须库
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams				#字体设置
import matplotlib.dates as mdates			#处理日期坐标轴
import seaborn as sns
from E0324_main import *
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 100)

#导入数据
df = pd.read_csv(r'C:\Users\ASUS\Project\Project\data\house_sales.csv')

#数据清洗
    #删除无用列
df.drop(columns='origin_url',inplace=True)
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)


#面积转换
df['area'] = df['area'].str.replace('㎡','').astype(float)
#售价转换
df['price'] = df['price'].str.replace('万','').astype(float)
df['unit'] = df['unit'].str.replace('元/㎡','').astype(float)
df['toward'] = df['toward'].astype('category')
df['year'] = df['year'].str.replace('年建','').astype(int)


#异常值处理
#房屋面积异常值
print('-'*50)
df = df[(df['area']<600) & (df['area']>20)]
print(len(df))
#房屋售价异常值
Q1 = df['price'].quantile(0.25)                             #利用IQR找出异常值
Q3 = df['price'].quantile(0.75)
IQR = Q3-Q1
low_price = Q1 - 1.5*IQR
high_price = Q3 + 1.5*IQR
df = df[(df['price']<high_price) & (df['price']>low_price)]


#新数据特征构造
#地区district
df['district'] = df['address'].str.split('-').str[0]    #这里str[0]是pandas专用取指定列
#楼层类型floor_type
df['floor_type'] = df['floor'].apply(fun1).astype('category')    #把一个函数批量作用到一整列的每一个元素上
#是否是直辖市zxs
df['zxs'] = df['province'].apply(lambda x:fun2(x))
#卧室数量bedrooms
df['bedrooms'] = df['rooms'].str.split('室').str[0]
#客厅数量livingrooms
#df['livingrooms'] = df['rooms'].str.split('室').str[1].str.split('厅').str[0]
df['livingrooms'] = df['rooms'].str.extract((r'(\d+)厅'))
#楼龄buliding_age
df['buliding_age'] = 2025 - df['year']
#价格分段price_labels
labels = ['低价','中价','高价','豪华']
df['price_labels'] = pd.cut(df['price'],
       bins = 4,
       labels = labels)

#数据分析

#数据概览
print('-'*50)
print(len(df))
print('-'*50)
print(df.info())
print('-'*50)
print(df.sample(10))

#可视化呈现
#plt.figure(figsize = ( ))	#设置画布大小
#rcParams ['font.sans-serif'] = ['Microsoft YaHei']	#设置微软雅黑
#plt.rcParams['axes.unicode_minus'] = False	#正常显示负号
#plt.show()
