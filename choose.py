from tkinter import *
import tkinter
from tkinter.messagebox import *
import login  
import psycopg2
import etc

#连接数据库需要提供相应的数据库名称、用户名、密码、地址、端口等信息
db = psycopg2.connect(database=etc.database,
                      user=etc.user,
                      password=etc.password,
                      host=etc.host,
                      port=etc.port)

# 使用cursor()方法创建一个游标对象cursor
cursor = db.cursor()


class choose_window(object):
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
        self.root.iconbitmap("./my/image/3.ico")
        # 设置窗口宽高固定
        self.root.resizable(0, 0)
        self.createPage()

    def createPage(self):
        bm = PhotoImage(
            file=r'C:\\Users\\admin\\Desktop\\大三上课程\\数据库实践\\my\\image\\1.png')
        self.lab3 = Label(self.root, image=bm)
        self.lab3.bm = bm
        self.lab3.pack()

        # 创建Frame
        self.page = Frame(self.root)
        self.page.pack()
        # 按键设置
        Button(self.page, text='商品', command=self.product).grid(row=9,
                                                                column=1,
                                                                stick=E)
        Button(self.page, text='用户', command=self.consumer).grid(row=9,
                                                                 column=2,
                                                                 stick=E)
        Button(self.page, text='类型', command=self.type_product).grid(row=9,
                                                                     column=3,
                                                                     stick=E)
        Button(self.page, text='订单', command=self.orders).grid(row=9,
                                                               column=4,
                                                               stick=E)
        Button(self.page, text='地址', command=self.address).grid(row=9,
                                                                column=5,
                                                                stick=E)
        Button(self.page, text='评论', command=self.comment).grid(row=9,
                                                                column=6,
                                                                stick=E)
        Button(self.page, text='后退', command=self.goback).grid(row=11,
                                                               column=10, )

    def product(self):
        self.lab3.destroy()
        self.page.destroy()
        all_product(self.root)

    def consumer(self):
        self.lab3.destroy()
        self.page.destroy()
        all_consumer(self.root)

    def type_product(self):
        self.lab3.destroy()
        self.page.destroy()
        all_type_product(self.root)

    def orders(self):
        self.lab3.destroy()
        self.page.destroy()
        all_orders(self.root)

    def address(self):
        self.lab3.destroy()
        self.page.destroy()
        all_address(self.root)

    def comment(self):
        self.lab3.destroy()
        self.page.destroy()
        all_comment(self.root)

    def goback(self):
        self.lab3.destroy()
        self.page.destroy()
        login.LoginPage(self.root)


class all_product(object):
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
        self.root.iconbitmap("./my/image/3.ico")
        # 设置窗口宽高固定
        self.root.resizable(0, 0)
        self.createPage()

    def createPage(self):
        self.button = Button(self.root, text='返回', command=self.goback)
        self.button.pack(side=RIGHT, padx=(0, 20), pady=(0, 20))
        self.list = Listbox(self.root)
        self.list.pack(fill=BOTH, expand=1, padx=10, pady=10)

        try:
            cursor.execute("SELECT * FROM product")
            data = cursor.fetchone()
        except Exception as e:
            # 准备在这里加一个弹窗
            pass

        while data != None:
            string = ""
            for item in data:
                string = string + " " + str(item)
            self.list.insert("end", string)
            data = cursor.fetchone()

    def goback(self):
        self.list.destroy()
        self.button.destroy()
        choose_window(self.root)


class all_consumer(object):
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
        self.root.iconbitmap("./my/image/3.ico")
        # 设置窗口宽高固定
        self.root.resizable(0, 0)
        self.createPage()

    def createPage(self):
        self.list = Listbox(self.root)
        self.list.pack(fill=BOTH, expand=1, padx=10, pady=10)
        self.button = Button(self.root, text='返回', command=self.goback)
        self.button.pack(side=RIGHT, padx=(0, 20), pady=(0, 20))

        cursor.execute("SELECT * FROM consumer")
        data = cursor.fetchone()

        while data != None:
            string = ""
            for item in data:
                string = string + " " + str(item)
            self.list.insert("end", string)
            data = cursor.fetchone()

    def goback(self):
        self.list.destroy()
        self.button.destroy()
        choose_window(self.root)


class all_type_product(object):
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
        self.root.iconbitmap("./my/image/3.ico")
        # 设置窗口宽高固定
        self.root.resizable(0, 0)
        self.createPage()

    def createPage(self):
        self.list = Listbox(self.root)
        self.list.pack(fill=BOTH, expand=1, padx=10, pady=10)
        self.button = Button(self.root, text='返回', command=self.goback)
        self.button.pack(side=RIGHT, padx=(0, 20), pady=(0, 20))

        cursor.execute("SELECT * FROM type_product")
        data = cursor.fetchone()

        while data != None:
            string = ""
            for item in data:
                string = string + " " + str(item)
            self.list.insert("end", string)
            data = cursor.fetchone()

    def goback(self):
        self.list.destroy()
        self.button.destroy()
        choose_window(self.root)


class all_orders(object):
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
        self.root.iconbitmap("./my/image/3.ico")
        # 设置窗口宽高固定
        self.root.resizable(0, 0)
        self.createPage()

    def createPage(self):
        self.list = Listbox(self.root)
        self.list.pack(fill=BOTH, expand=1, padx=10, pady=10)
        self.button = Button(self.root, text='返回', command=self.goback)
        self.button.pack(side=RIGHT, padx=(0, 20), pady=(0, 20))

        cursor.execute("SELECT * FROM orders")
        data = cursor.fetchone()

        while data != None:
            string = ""
            for item in data:
                string = string + " " + str(item)
            self.list.insert("end", string)
            data = cursor.fetchone()

    def goback(self):
        self.list.destroy()
        self.button.destroy()
        choose_window(self.root)


class all_address(object):
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
        self.root.iconbitmap("./my/image/3.ico")
        # 设置窗口宽高固定
        self.root.resizable(0, 0)
        self.createPage()

    def createPage(self):
        self.list = Listbox(self.root)
        self.list.pack(fill=BOTH, expand=1, padx=10, pady=10)
        self.button = Button(self.root, text='返回', command=self.goback)
        self.button.pack(side=RIGHT, padx=(0, 20), pady=(0, 20))

        cursor.execute("SELECT * FROM address")
        data = cursor.fetchone()

        while data != None:
            string = ""
            for item in data:
                string = string + " " + str(item)
            self.list.insert("end", string)
            data = cursor.fetchone()

    def goback(self):
        self.list.destroy()
        self.button.destroy()
        choose_window(self.root)


class all_comment(object):
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
        self.root.iconbitmap("./my/image/3.ico")
        # 设置窗口宽高固定
        self.root.resizable(0, 0)
        self.createPage()

    def createPage(self):
        self.list = Listbox(self.root)
        self.list.pack(fill=BOTH, expand=1, padx=10, pady=10)
        self.button = Button(self.root, text='返回', command=self.goback)
        self.button.pack(side=RIGHT, padx=(0, 20), pady=(0, 20))

        cursor.execute("SELECT * FROM product_comments")
        data = cursor.fetchone()

        while data != None:
            string = ''
            for item in data:
                string = string + " " + str(item)
            self.list.insert("end", string)
            data = cursor.fetchone()

    def goback(self):
        self.list.destroy()
        self.button.destroy()
        choose_window(self.root)