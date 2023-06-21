# -*- coding: utf-8 -*-            
# @Time : 2023/6/19 10:36
# @author:ZXZ
# @FileName: mainpage.py
# @Software: PyCharm
import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import json
from main import processing
from subpage import SubPage


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(sticky="nsew")
        self.create_widgets()
        sys.stdout = self  # 重定向标准输出

    def create_widgets(self):
        # 文件路径输入框
        self.path_entry = tk.Entry(self)
        self.path_entry.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.path_entry.insert(0, "文件路径")

        #文件确定输入按钮
        self.change_file_button = tk.Button(self, text="选择文件", command=self.SelectFile)
        self.change_file_button.grid(row=0, column=1, pady=20)

        # 运行信息文本框
        # self.info_text = tk.Text(self, height=10, wrap="word")
        # self.info_text.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.text_area.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # 运行按钮
        self.run_button = tk.Button(self, text="运行", command=self.run)
        self.run_button.grid(row=2, column=1, pady=20)

        # 修改配置
        self.change_config_button = tk.Button(self, text="修改配置", command=self.change_config)
        self.change_config_button.grid(row=1, column=1, pady=20)

        # 配置行和列权重
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

    def write(self, message):
        self.text_area.insert(tk.END, str(message))  # 将消息添加到文本框中
        self.text_area.see(tk.END)  # 滚动到文本框底部

    def SelectFile(self):
        file_path = filedialog.askopenfilename()
        # 将选择的文件路径输出至主界面的输入框中
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(tk.END, file_path)

    def check_config(self) -> bool:
        if os.path.isfile('config.json'):
            print('文件存在')
            return True
        else:
            print('文件不存在')
            return False

    def load_config(self) -> dict:
        with open('config.json') as f:
            config = json.load(f)
            params = {k: config[k] for k in ["flag", "key", "prompt", "select_mode", "write_mode"]}
        return params
    def change_config(self):
        SubPage(root)

    def check_thread(self,t:threading):
        if t.is_alive():
            # 子线程还在执行
            root.after(500, self.check_thread,t)
        else:
            # 子线程执行结束
            self.run_button.config(state=tk.NORMAL)

    def run(self):
        filpath = self.path_entry.get()
        if filpath=='':
            messagebox.showwarning(title="警告", message="这是一个警告对话框")
        else:
            if self.check_config():
                print("存在配置文件")
                params = self.load_config()
                print(params)
                self.run_button.config(state=tk.DISABLED)  # 禁用按钮，防止重复启动任务
                # t = threading.Thread(target=processing(filpath,host=params['host'],key=params["key"],prompt=params['prompt'],select_mode=params['select_mode'],write_mode=params['write_mode']))
                t = threading.Thread(target=processing,kwargs={'file': filpath, 'flag': params['flag'],'key':params['key'],'prompt':params['prompt'],'select_mode':params['select_mode'],"write_mode":params['write_mode']})
                t.start()
                root.after(100, self.check_thread,t)
            else:
                # 在主界面中添加按钮，点击可以打开子页面
                print("不存在配置文件")
                SubPage(root)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("降重工具")
    app = App(root)
    root.mainloop()
