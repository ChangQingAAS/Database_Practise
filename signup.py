from tkinter import *
from tkinter.messagebox import *
import datetime
# from MainPage import *
from tkinter import messagebox
import psycopg2
import etc
from Sql_Search import SqlSearch
import page1
from date import Date


class SignupPage(object):
    def __init__(self, master=None):

        self.root = master
        winWidth = 650
        winHeight = 400
        screenWidth = self.root.winfo_screenwidth()
        screenHeight = self.root.winfo_screenheight()

        x = int((screenWidth - winWidth) / 2)
        y = int((screenHeight - winHeight) / 2)
        # 设置窗口初始位置在屏幕居中
        self.root.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
        # 设置窗口图标
        self.root.iconbitmap("./image/3.ico")
        # 设置窗口宽高固定
        self.root.resizable(0, 0)

        self.user_id = StringVar()
        self.passwd = StringVar()
        self.username = StringVar()
        self.nickname = StringVar()
        self.tel_num = StringVar()
        self.gender = StringVar()
        self.v = IntVar()
        self.birth_date = StringVar()
        self.createPage()

    def createPage(self):

        self.page = Frame(self.root)  # 创建Frame
        self.page.pack()
        Label(self.page).grid(row=0, stick=W)

        Label(self.page, text='用户id: ').grid(row=1, stick=W, pady=10)
        Entry(self.page, textvariable=self.user_id).grid(row=1,
                                                         column=1,
                                                         stick=E)

        Label(self.page, text='密码: ').grid(row=2, stick=W, pady=10)
        Entry(self.page, textvariable=self.passwd, show='*').grid(row=2,
                                                                  column=1,
                                                                  stick=E)

        Label(self.page, text='用户名: ').grid(row=3, stick=W, pady=10)
        Entry(self.page, textvariable=self.username).grid(row=3,
                                                          column=1,
                                                          stick=E)
        Label(self.page, text='昵称: ').grid(row=4, stick=W, pady=10)
        Entry(self.page, textvariable=self.nickname).grid(row=4,
                                                          column=1,
                                                          stick=E)

        Label(self.page, text='电话: ').grid(row=5, stick=W, pady=10)
        Entry(self.page, textvariable=self.tel_num).grid(row=5,
                                                         column=1,
                                                         stick=E)

        Label(self.page, text='性别: ').grid(row=6, stick=W, pady=10)
        rbt = Radiobutton(self.page, text='男', variable=self.v,
                    value='M')
        rbt.grid(row=6, column=0 ,padx=5 ,columnspan=2)
        rbt = Radiobutton(self.page, text='女', variable=self.v,
                    value='F')
        rbt.grid(row=6, column=1,padx=80 ,columnspan=90)
        
        # Label(self.page, text='出生日期: ').grid(row=7, stick=W, pady=10) 
        Button(self.page, text='出生日期：', command=lambda: self.getdate('start')).grid(row=7,stick=W,pady=10)
        Entry(self.page, textvariable=self.birth_date).grid(row=7, column=1)

        Button(self.page, text='注册', command=self.signupCheck).grid(row=8,
                                                                    stick=W,
                                                                    pady=10)
        Button(self.page, text='退出', command=self.page.quit).grid(row=8,
                                                                  column=1,
                                                                  stick=E)
    def getdate(self, type):  #获取选择的日期
        for date in [Date().selection()]:
            if date:
                if (type == 'start'):  #如果是开始按钮，就赋值给开始日期
                    self.birth_date.set(date) 

    def signupCheck(self):
        user_id = self.user_id.get()
        passwd = self.passwd.get()
        username = self.username.get()
        nickname = self.nickname.get()
        tel_num = self.tel_num.get()
        if self.v == 'M':
            self.gender = 'M'
        else:
            self.gender = 'F'
        gender = self.gender
        birth_date = self.birth_date.get()

        obj_r = SqlSearch()
        tag = obj_r.insert_userinfo(user_id, passwd, username, nickname,
                                    tel_num, gender, birth_date)

        if (tag == True):
            self.page.destroy()
            page1.Page1(self.root)
