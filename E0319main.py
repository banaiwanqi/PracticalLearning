#加载必要库
from E0319 import *
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams ['font.sans-serif'] = ['Microsoft YaHei']	#设置微软雅黑
plt.rcParams['axes.unicode_minus'] = False	#正常显示负号

#连接数据库
conn = get_db_connection('sql学习')
#获取数据1
df = pd.read_sql("select * from 班级1", conn)
conn.close()
print('======== 欢迎使用 ========')
print('===== 学生成绩管理系统 =====')

#清洗
df = filter_data(df)
df = base_df(df)
df = overall_analysis(df)

#运行主程序
main(df)