import tkinter as tk
import subprocess
from tkinter import font
# 创建一个主窗口
root = tk.Tk()
frame = tk.Frame(root)
frame.pack(fill='both', expand=True)
root.configure(background='black') 
# 设置窗口标题
root.title("主页面窗口")

# 设置窗口大小（宽度x高度）
root.geometry("800x500")
s1 = "俄罗斯方块\n"
s4 = "小组成员:张明昊 付建豪 张鹏辉"
s2 = "开始游戏\n"
s3 = "查看历史分数\n"
# （可选）添加一个标签到窗口中
custom_font1 = font.Font(family="宋体", size=25, weight="bold")
custom_font2 = font.Font(family="宋体", size=15, weight="bold")
label1 = tk.Label(text=s1, font=custom_font1,fg='white',bg='black')  # 设置标签背景颜色为白色
label12 = tk.Label(text=s4, font=custom_font2,fg='white',bg='black')
label1.pack(pady=40)  # 使用pack布局管理器将标签添加到框架中，并设置垂直填充
label12.pack(pady=40)

# （可选）添加一个按钮到窗口中


def lj1():
    # 替换为你的Python脚本路径
    script_path = "main_game.py"

    # 使用subprocess运行Python脚本
    # 注意：这需要在你的系统上已经安装了Python，并且可以在环境变量中找到
    subprocess.run(["python", script_path],cwd='.')
def lj2():
    # 替换为你的Python脚本路径
    script_path = "score.py"

    # 使用subprocess运行Python脚本
    # 注意：这需要在你的系统上已经安装了Python，并且可以在环境变量中找到
    subprocess.run(["python", script_path],cwd='.')

lj1_button = tk.Button(root, text=s2, font=custom_font1, command=lj1, fg='white',bg='black')
lj1_button.pack(pady=20)
lj2_button = tk.Button(root, text=s3, font=custom_font1, command=lj2, fg='white',bg='black')
lj2_button.pack(pady=20)

root.mainloop()
