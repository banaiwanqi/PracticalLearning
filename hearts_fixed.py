import tkinter as tk, random, time, sys, math

h, a = [], []
t = ['多喝水！', '好好爱自己', '好好吃饭', '保持好心情', '我想你了', '顺顺利利', '别熬夜', '天凉了多穿衣服']
c = ['pink', 'lightblue', 'lemonchiffon', 'hotpink', 'skyblue']

def g(n, w, h):
    p = []
    for i in range(n):
        th = i / n * 2 * math.pi
        x = 16 * math.sin(th) ** 3
        y = 13 * math.cos(th) - 5 * math.cos(2 * th) - 2 * math.cos(3 * th) - math.cos(4 * th)
        sx = int(w / 2 + x * 20 - 50)
        sy = int(h / 2 - y * 20 - 80)
        p.append((max(0, min(sx, w - 150)), max(0, min(sy, h - 60))))
    return p

def wx(x, y, tip=None, is_h=True):
    w = tk.Toplevel()
    w.geometry(f'150x60+{x}+{y}')
    w.title('提示')
    w.attributes('-topmost', 1)
    tk.Label(w, text=tip or random.choice(t),
           bg=random.choice(c),
           font=('微软雅黑', 14),
           width=20,
           height=3).pack()
    # 空格键关闭所有窗口并退出
    def close_all(event):
        for win in h + a:
            try:
                win.destroy()
            except:
                pass
        sys.exit()
    w.bind('<space>', close_all)
    return w

def w():
    global h, a
    h, a = [], []  # 每次调用重置窗口列表
    
    r = tk.Tk()
    r.withdraw()
    # 确保之前的 Tk 实例被清理
    try:
        r.destroy()
    except:
        pass
    
    # 创建新的 Tk 实例
    r = tk.Tk()
    r.withdraw()
    
    sw, sh = r.winfo_screenwidth(), r.winfo_screenheight()
    n = 100

    # 阶段1: 绘制爱心弹窗
    for i, (x, y) in enumerate(g(n, sw, sh)):
        win = wx(x, y, '充实自己' if i == n - 1 else None)
        h.append(win)
        r.update()
        time.sleep(0.03)

    time.sleep(1)  # 爱心显示1秒

    # 关闭爱心弹窗
    for win in h:
        try:
            if win.winfo_exists():
                win.destroy()
        except:
            pass
    r.update()

    # 阶段2: 大面积弹窗
    for _ in range(int((sw // 150 * sh // 40 + 50) * 0.6)):
        x, y = random.randint(0, sw - 150), random.randint(0, sh - 60)
        win = wx(x, y, is_h=False)
        a.append(win)
        r.update()
        time.sleep(0.005)

    # 5秒后自动关闭弹窗
    time.sleep(5)
    for window in a:
        try:
            if window.winfo_exists():
                window.destroy()
        except:
            pass
    r.update()

    # 清理主窗口
    try:
        r.destroy()
    except:
        pass

if __name__ == '__main__':
    w()