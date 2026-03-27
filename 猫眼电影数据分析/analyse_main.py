import pandas as pd
import matplotlib.pyplot as plt
import itertools
import numpy as np

# 1. 演员口碑分析
def analyze_actor_reputation(df):
    actors_exploded = df['author'].str.split(',').explode().str.strip()
    actor_count = actors_exploded.value_counts().reset_index()
    result = []

    for idx, row in actor_count.iterrows():
        actor = row['author']
        cnt = row['count']
        mask = df['author'].str.contains(actor, na=False)
        total_star = df.loc[mask, 'star'].sum()
        avg_star = total_star / cnt if cnt != 0 else 0
        result.append({
            'actor': actor,
            'movie_count': cnt,
            'avg_star': round(avg_star, 2)
        })

    actor_df = pd.DataFrame(result)
    actor_df = actor_df.sort_values('avg_star', ascending=False)
    return actor_df


# 2. 演员组合分析
def analyze_actor_combination(df, top_n=15):
    combo_list = []
    for idx, row in df.dropna(subset=['author']).iterrows():
        authors = row['author']
        star = row['star']
        actor_list = [a.strip() for a in authors.split(',')]
        pairs = list(itertools.combinations(actor_list, 2))
        for p in pairs:
            combo_list.append({'pair': p, 'star': star})

    combo_df = pd.DataFrame(combo_list)
    combo_summary = combo_df.groupby('pair')['star'].agg(
        合作次数='count',
        平均评分='mean'
    ).reset_index()
    combo_summary = combo_summary.sort_values(['平均评分', '合作次数'], ascending=False)
    return combo_summary.head(top_n)


# 3. 画图：演员口碑TOP20
def plot_top_actors(actor_df, top_n=20):
    top = actor_df.head(top_n)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(12, 6))
    plt.barh(top['actor'][::-1], top['avg_star'][::-1], color='#4472C4')
    plt.xlabel('平均评分')
    plt.title(f'TOP{top_n} 演员口碑评分', fontsize=14)
    plt.tight_layout()
    plt.show()


# 4. 画图：演员组合TOP15
def plot_top_combinations(combo_df):
    combo_df['组合名'] = combo_df['pair'].apply(lambda x: f'{x[0]} & {x[1]}')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(12, 6))
    plt.barh(combo_df['组合名'][::-1], combo_df['平均评分'][::-1], color='#ED7D31')
    plt.xlabel('平均评分')
    plt.title('TOP15 演员组合口碑效果', fontsize=14)
    plt.tight_layout()
    plt.show()


# ================= 1. 风格口碑分析（哪些类型是口碑保障） =================
def analyze_style_reputation(df):
    # 拆分风格、去空格、展开
    styles_exploded = df['style'].str.split(',').explode().str.strip()
    style_count = styles_exploded.value_counts().reset_index()

    result = []
    for idx, row in style_count.iterrows():
        style = row['style']  # 风格名
        cnt = row['count']  # 出现次数
        # 匹配所有包含该风格的影片
        mask = df['style'].str.contains(style, na=False)
        total_star = df.loc[mask, 'star'].sum()
        avg_star = total_star / cnt if cnt != 0 else 0
        result.append({
            'style': style,
            'movie_count': cnt,
            'avg_star': round(avg_star, 2)
        })

    style_df = pd.DataFrame(result)
    # 按平均分降序排序
    style_df = style_df.sort_values('avg_star', ascending=False)
    return style_df


# ================= 2. 风格组合分析（哪些类型搭配效果好） =================
def analyze_style_combination(df, top_n=15):
    combo_list = []
    # 遍历每一行，生成两两风格组合
    for idx, row in df.dropna(subset=['style']).iterrows():
        styles = row['style']
        star = row['star']
        style_list = [s.strip() for s in styles.split(',')]
        pairs = list(itertools.combinations(style_list, 2))
        for p in pairs:
            combo_list.append({'pair': p, 'star': star})

    combo_df = pd.DataFrame(combo_list)
    # 按组合分组，统计合作次数和平均评分
    combo_summary = combo_df.groupby('pair')['star'].agg(
        搭配次数='count',
        平均评分='mean'
    ).reset_index()
    # 按平均评分、搭配次数双维度降序
    combo_summary = combo_summary.sort_values(['平均评分', '搭配次数'], ascending=False)
    return combo_summary.head(top_n)


# ================= 3. 可视化：TOP风格口碑柱状图 =================
def plot_top_styles(style_df, top_n=20):
    top = style_df.head(top_n)
    # 解决中文显示问题
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    plt.figure(figsize=(12, 6))
    # 倒序排列，让高分在上方
    plt.barh(top['style'][::-1], top['avg_star'][::-1], color='#2E8B57')
    plt.xlabel('平均评分')
    plt.ylabel('影片风格')
    plt.title(f'TOP{top_n} 影片风格口碑评分（口碑保障类型）', fontsize=14)
    plt.tight_layout()
    plt.show()


# ================= 4. 可视化：TOP风格组合柱状图 =================
def plot_top_style_combinations(combo_df):
    # 把元组组合转为可读字符串
    combo_df['组合名'] = combo_df['pair'].apply(lambda x: f'{x[0]} & {x[1]}')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    plt.figure(figsize=(12, 6))
    plt.barh(combo_df['组合名'][::-1], combo_df['平均评分'][::-1], color='#FF6347')
    plt.xlabel('平均评分')
    plt.ylabel('风格组合')
    plt.title('TOP 影片风格组合口碑效果', fontsize=14)
    plt.tight_layout()
    plt.show()

# ================= 年代趋势分析 =================
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


# ================= 4. 可视化：年代趋势对比图 =================
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