import pandas as pd

#提取floor
def fun1(str):
    if '低' in str:
        return  '低楼层'
    elif '中' in str:
        return  '中楼层'
    elif '高' in str:
        return  '高楼层'
    else:
        return '未知'

#判断直辖市
def fun2(str):
    if str in ['北京','上海','天津','重庆']:
        return 1
    else:
        return 0
