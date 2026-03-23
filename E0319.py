import pandas as pd
import pymysql
from matplotlib import pyplot as plt, rcParams


def get_db_connection(db_name):
    conn = pymysql.connect(host = 'localhost',
                           port = 3306,
                           user = 'root',
                           password = 'soldierbar8',
                           database = db_name,
                            charset = 'utf8mb4'
                           )
    return conn
#str
def to_numeric(df):
    for i in range(3,19):
        try:
            df.iloc[:, 1:20] = df.iloc[:, 1:20].apply(pd.to_numeric, errors='coerce')
        except:
            pass
    return df

#清洗空值
def drop_nan(df):
    try:
        df = df.dropna(thresh=3)
        df = df.dropna(thresh=4, axis=1)
        return df
    except Exception as e:
        print('清洗空值出错了',e)

#筛选数据
def filter_data(df):
    try:
        df = df[df['学号'].astype(str).str.startswith('24111466')]
        df.dropna(subset=['学号'],inplace = True)
        return df
    except Exception as e:
        print('筛选数据出错了',e)

#重组数据 按n为起始位置 m为科目尾部位置
def base_df(df):
    df = df.iloc[:,1:19].copy()
    return df

#整体平均分
def overall_analysis(df):
    score_df = df.iloc[:, 1:20].copy()
    score_df = score_df.apply(pd.to_numeric, errors='coerce')
    df['平均分'] = score_df.mean(axis=1)

    return df

#班级平均分
def class_avg(df):
    return df['平均分'].mean()

#统计平均分以上人数
def over_mean(df):
    avg = class_avg(df)
    over_mean_students = (df['平均分']>=avg).sum()
    return over_mean_students

#局部分析 每科第一
def max_subject_students(df):
    result = []
    for i in range(2,18):
        subject_name = df.columns[i]
        max_score = df.iloc[:, i].max()
        max_students = df[df.iloc[:, i] == max_score]['姓名'].tolist()
        result.append({
            "科目": subject_name,
            "最高分": max_score,
            "学生姓名": ", ".join(max_students)
        })
    result_df = pd.DataFrame(result)
    return result_df

#数据分箱
def score_binning(df):
    bins = [0,60,70,80,90,101]
    labels = ['不及格','合格','中等','良好','优秀']
    for i in range(2,18):
        col_name = df.columns[i]
        df[f'{col_name}_等级'] = pd.cut(df[col_name],
                                              bins = bins,
                                              labels = labels,
                                              right=False)
    return  df

#可视化
#直方图 平均分可视化
def class_mean_visual(df):
    plt.figure(figsize=(10, 6))
    df_temp = df.sort_values('平均分', ascending=False).head(10)
    df_temp = df_temp.set_index('姓名')['平均分']
    df_temp.sort_values(ascending=True).plot(kind='barh')
    plt.title('学生成绩平均分排名 TOP10', fontsize=14, pad=15)
    plt.xlabel('平均分', fontsize=12)
    plt.ylabel('学生姓名', fontsize=12)
    plt.box(on=None)
    plt.grid(axis='x', alpha=0.3)
    for i, v in enumerate(df_temp.sort_values(ascending=True)):
        plt.text(v + 0.5, i, f'{v:.1f}', va='center', fontsize=11)

    plt.tight_layout()
    plt.show()

#直方图 每学科的各个阶段人数
def subject_visual(df):
    bins = [-1, 59, 69, 79, 89, 100]  # 关键修复
    labels = ['不及格', '合格', '中等', '良好', '优秀']
    subjects = df.columns[2:18].tolist()
    for idx_batch in range(0, len(subjects), 8):
        batch = subjects[idx_batch: idx_batch + 8]
        if not batch:
            break
        fig, axes = plt.subplots(2, 4, figsize=(20, 10))
        axes = axes.flatten()
        for i, sub in enumerate(batch):
            ax = axes[i]
            s = pd.to_numeric(df[sub], errors='coerce')
            cnt = pd.cut(
                s,
                bins=bins,
                labels=labels,
                right=True,
                include_lowest=True
            ).value_counts(sort=False)

            cnt.plot(kind='bar', ax=ax, color=['red', 'blue', 'blue', 'blue', 'blue'])
            ax.set_title(sub, fontsize=14, fontweight='bold')
            ax.tick_params(axis='x', rotation=0)
            ax.grid(axis='y', alpha=0.3)

            for x, v in enumerate(cnt):
                ax.text(x, v + 0.1, str(int(v)), ha='center', fontsize=12, fontweight='bold')

        for j in range(len(batch), 8):
            axes[j].set_visible(False)

        plt.suptitle('成绩分布统计（8科/图）', fontsize=18, y=0.98)
        plt.tight_layout()
        plt.subplots_adjust(top=0.92)
        plt.show()

#打包数据
def create_data_dict(df):
    data = {}

    for i in range(2, 19):
        subject_name = df.columns[i]
        col_data = df.iloc[:, i]
        scores = pd.to_numeric(col_data, errors='coerce')
        scores = scores.dropna().tolist()
        data[subject_name] = scores
    return data

#箱型图
def student_boxplot(data):
    plt.figure(figsize=(20, 10))
    box = plt.boxplot(
        [scores for scores in data.values()],
        tick_labels=list(data.keys()),
        patch_artist=True,
        showfliers=True
    )
    for i, flier in enumerate(box['fliers']):
        # 获取异常点的坐标
        x = flier.get_xdata()
        y = flier.get_ydata()

        # 给每个点标注分数
        for xi, yi in zip(x, y):
            plt.text(
                xi, yi, f'{int(yi)}',
                ha='center', va='bottom',
                fontsize=10, color='red', fontweight='bold'
            )
    plt.title('各科成绩箱线图对比', fontsize=16)
    plt.xlabel('科目', fontsize=12)
    plt.ylabel('分数', fontsize=12)
    plt.xticks(rotation=30)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

# 主程序
def main(df):

    while True:
        print("1. 查看班级平均分及平均分以上人数")
        print("2. 查询处理完成的表")
        print('3. 查询每科第一')
        print("4. 查看前十名")
        print('5. 查看每学科的各个阶段人数')
        print('6. 查看箱型图')
        print("0. 退出系统")
        choice = int(input('请输入编号：'))

        if choice == 1:
            result1 = class_avg(df)
            print(f'班级平均分是：{result1:.2f}')
            result2 = over_mean(df)
            print(f'本次平均分超过{result1:.2f}的人数是{result2}')
            print('-'*70)

        elif choice == 2:
            print(df)
            print('-' * 70)

        elif choice == 3:
            max_df = max_subject_students(df)
            print(max_df)
            print('-' * 70)

        elif choice == 4:
            class_mean_visual(df)

        elif choice == 5:
            subject_visual(df)

        elif choice == 6:
            data = create_data_dict(df)
            student_boxplot(data)

        elif choice == 0:
            break
        else:
            print('编号输入错误，请重新输入！')


