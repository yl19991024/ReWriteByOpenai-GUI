# -*- coding: utf-8 -*-            
# @Time : 2023/6/19 10:18
# @author:ZXZ
# @FileName: subpage.py
# @Software: PyCharm
import json
import os
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox


class SubPage(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        # if self.check_config():
        #     with open('config.json') as f:
        #         config = json.load(f)
        #         params = {k: config[k] for k in ["flag", "key", "prompt", "select_mode", "write_mode"]}
        #         self.flag=params['flag']
        #         self.key=params['key']
        #         self.prompt=params['prompt']
        #         self.write_mode=params['write_mode']
        #         self.select_mode=params['select_mode']
        # else:
        self.title("输入配置信息")
        self.flag = BooleanVar()
        self.key = StringVar()
        self.prompt = StringVar()
        self.select_mode = StringVar()
        self.write_mode = StringVar()

        self.create_widgets()

    def create_widgets(self):
        # 是否使用第三方平台的服务
        flag = Label(self, text="是否使用第三方平台的服务：")
        flag.grid(row=0, column=0, padx=5, pady=5)
        flag_check = Checkbutton(self, variable=self.flag)
        flag_check.grid(row=0, column=1, padx=5, pady=5)


        # key输入框
        key_label = Label(self, text="key：")
        key_label.grid(row=2, column=0, padx=5, pady=5)
        key_entry = Entry(self, textvariable=self.key)
        key_entry.grid(row=2, column=1, padx=5, pady=5)

        # prompt输入框
        prompt_label = Label(self, text="prompt：")
        prompt_label.grid(row=3, column=0, padx=5, pady=5)
        prompt_entry = Entry(self, textvariable=self.prompt)
        prompt_entry.grid(row=3, column=1, padx=5, pady=5)

        # select_mode选项
        select_mode_label = Label(self, text="降重模式：")
        select_mode_label.grid(row=4, column=0, padx=5, pady=5)
        select_mode_combo = Combobox(self, textvariable=self.select_mode, values=["onlu_red", "all"])
        select_mode_combo.current(0)
        select_mode_combo.grid(row=4, column=1, padx=5, pady=5)

        # write_mode选项
        flag = Label(self, text="写入模式：")
        flag.grid(row=5, column=0, padx=5, pady=5)
        write_mode_combo = Combobox(self, textvariable=self.write_mode, values=["insert", "replace"])
        write_mode_combo.current(0)
        write_mode_combo.grid(row=5, column=1, padx=5, pady=5)

        # 保存按钮
        save_button = Button(self, text="保存", command=self.save)
        save_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    def save(self):
        data = {
            "flag": self.flag.get(),
            "key": self.key.get(),
            "prompt": self.prompt.get(),
            "select_mode": self.select_mode.get(),
            "write_mode": self.write_mode.get(),
        }
        with open("config.json", "w") as f:
            json.dump(data, f, indent=4)
        print("参数已保存至config.json")
        self.destroy()
    def check_config(self) -> bool:
        if os.path.isfile('config.json'):
            print('文件存在')
            return True
        else:
            print('文件不存在')
            return False