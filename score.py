import tkinter as tk  
from tkinter import font, scrolledtext  
  
root = tk.Tk()  
root.geometry("800x500")  
root.configure(background='black')  
  
# 创建一个滚动文本控件  
text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=font.Font(family="宋体", size=15, weight="bold"), fg='white', bg='black')  
text_widget.pack(pady=40, fill='both', expand=True)  # fill 和 expand 参数使控件填充整个窗口  
  
# 读取文件内容并添加到 Text 控件中  
with open('info.txt', 'r', encoding='utf-8') as file:  
    text_widget.insert(tk.END, file.read())  # 插入整个文件内容到 Text 控件的末尾  
  
root.mainloop()