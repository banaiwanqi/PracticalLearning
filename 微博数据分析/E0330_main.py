import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
rcParams ['font.sans-serif'] = ['Microsoft YaHei']	#设置微软雅黑
plt.rcParams['axes.unicode_minus'] = False	#正常显示负号

def top_by_star(df):
    arr = df[['title','star']].sort_values(by ='star' ,ascending=False).head(15)
    plt.figure(figsize=(12,8))  # 设置画布大小
    plt.barh(arr['title'], arr['star'])
    plt.gca().invert_yaxis()
    plt.grid(False)
    plt.yticks(arr['title'])
    plt.title('Top15 榜单')
    for index, value in enumerate(arr['star']):
        plt.text(value + 0.05, index, f'{value}', va='center')
    plt.show()

def analyze_decade_trend(df):
    df['year'] = pd.to_datetime(df['pub_time'], errors='coerce').dt.year
    # 按10年分组（如1990-1999为90年代）
    df['decade'] = (df['year'] // 10) * 10

    decade_trend = df.groupby('decade').agg(
        影片数量=('star', 'count'),
        平均评分=('star', 'mean')
    ).reset_index()

    decade_trend['年代'] = decade_trend['decade'].astype(str) + '年代'
    return decade_trend

def plot_decade_trend(decade_trend):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    fig, ax1 = plt.subplots(figsize=(12, 6))

    # 左轴：数量
    ax1.bar(decade_trend['年代'], decade_trend['影片数量'], color='#2E8B57', alpha=0.7, label='影片数量')
    ax1.set_xlabel('年代', fontsize=12)
    ax1.set_ylabel('影片数量', color='#2E8B57', fontsize=12)
    ax1.tick_params(axis='y', labelcolor='#2E8B57')

    # 右轴：评分
    ax2 = ax1.twinx()
    ax2.plot(decade_trend['年代'], decade_trend['平均评分'], color='#FF6347', linewidth=3, marker='o', label='平均评分')
    ax2.set_ylabel('平均评分', color='#FF6347', fontsize=12)
    ax2.tick_params(axis='y', labelcolor='#FF6347')

    plt.title('电影行业年代趋势对比', fontsize=16, pad=20)
    fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9), fontsize=12)
    plt.tight_layout()
    plt.show()