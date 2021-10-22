from tkinter import *
import tkinter
from tkinter.messagebox import *
import datetime
import login
import psycopg2
import etc
from for_user_id import get_user_id
from address import *
from comment import *

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
        self.user_id = get_user_id()
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
        self.createPage()

    def createPage(self):
        bm = PhotoImage(
            file=
            r'C:\\Users\\admin\\Desktop\\大三上课程\\数据库实践\\databse_practise\\image\\1.png'
        )
        self.lab3 = Label(self.root, image=bm)
        self.lab3.bm = bm
        self.lab3.pack()

        # 创建Frame
        self.page = Frame(self.root)
        self.page.pack()
        # 按键设置
        Button(self.page, text='商品列表', command=self.product,
               bg='AliceBlue').grid(row=9, column=5, stick=E)
        Button(self.page, text='我的订单', command=self.orders,
               bg='AliceBlue').grid(row=10, column=5, stick=E)
        Button(self.page, text='我的地址', command=self.address,
               bg='AliceBlue').grid(row=11, column=5, stick=E)
        Button(self.page, text='商品评论', command=self.comment,
               bg='AliceBlue').grid(row=12, column=5)
        self.back = tkinter.Button(width=5,
                                   height=1,
                                   text='后退',
                                   padx=1,
                                   pady=1,
                                   anchor='w',
                                   background='AliceBlue',
                                   command=self.goback)
        self.back.place(x=650 - 40, y=400 - 15, anchor='w')

    def product(self):
        self.back.destroy()
        self.lab3.destroy()
        self.page.destroy()
        all_product(self.root)

    def orders(self):
        self.back.destroy()
        self.lab3.destroy()
        self.page.destroy()
        all_orders(self.root)

    def address(self):
        self.back.destroy()
        self.lab3.destroy()
        self.page.destroy()
        all_address(self.root)

    def comment(self):
        self.back.destroy()
        self.lab3.destroy()
        self.page.destroy()
        all_comment(self.root)

    def goback(self):
        self.back.destroy()
        self.lab3.destroy()
        self.page.destroy()
        login.LoginPage(self.root)


class all_product(object):
    def __init__(self, master=None):

        self.user_id = get_user_id()
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

        self.product_id = StringVar()

        self.createPage()

    def createPage(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack()

        try:
            values = []
            cursor.execute("select product_id from product")
            data = cursor.fetchone()
            while data != None:
                values.append(str(data[0]))
                data = cursor.fetchone()
        except Exception as err:
            print(err)

        Label(self.page, text='购买商品: ').grid(row=1, stick=W, pady=10)
        self.product_id.set('1')
        self.combobox = ttk.Combobox(
            master=self.page,  # 父容器
            height=4,  # 高度,下拉显示的条目数量
            width=8,  # 宽度
            state='normal',  # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled
            cursor='arrow',  # 鼠标移动时样式 arrow, circle, cross, plus...
            font=('', 14),  # 字体
            textvariable=self.product_id,  # 通过StringVar设置可改变的值
            values=values,  # 设置下拉框的选项
        )
        self.combobox.grid(row=1, column=1, stick=W)
        Button(self.page, text='确定', command=self.buy,
               bg='AliceBlue').grid(row=1, column=5)

        self.button = Button(self.root,
                             text='返回',
                             command=self.goback,
                             bg='AliceBlue')
        self.button.pack(side=RIGHT, padx=(0, 20), pady=(0, 20))
        self.list = Listbox(self.root)
        self.list.pack(fill=BOTH, expand=1, padx=10, pady=10)
        string = " | 商品id | 商品名 | 商品类型 | 商品价格 | 销量 | 商品描述 | 店铺名"
        self.list.insert("end", string)

        try:

            cursor.execute(
                "select product_id, product_name, type_name, price,sales, details, shop_name from product,type_product where product.type_id = type_product.type_id order by product_id "
            )
            data = cursor.fetchone()

            while data != None:
                string = ""
                for item in data:
                    string = string + " | " + str(item)
                self.list.insert("end", string)
                data = cursor.fetchone()
        except Exception as err:
            print(err)

    def buy(self):
        product_id = self.product_id.get()
        order_time = datetime.datetime.now().strftime("%Y-%m-%d")
        order_time = '\'' + order_time + '\''

        try:
            string = "select price from product where product_id = %s" % str(
                product_id)
            cursor.execute(string)
            total_price = cursor.fetchone()[0]
            cursor.execute(
                "insert into purchase (user_id, product_id) VALUES (%s,%s) " %
                (str(self.user_id), str(product_id)))
            cursor.execute(
                "insert into orders (order_time, user_id, product_id, status, addr_id, total_price) VALUES (%s,%s,%s,'状态：未送达',0001,%s)"
                %
                (order_time, str(self.user_id), str(product_id), total_price))
            db.commit()
            messagebox.showinfo(title='恭喜', message='购买成功')

        except Exception as err:
            print(err)

    def goback(self):
        self.list.destroy()
        self.button.destroy()
        self.page.destroy()
        choose_window(self.root)


class all_orders(object):
    def __init__(self, master=None):

        self.user_id = get_user_id()
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
        self.createPage()

    def createPage(self):
        self.list = Listbox(self.root)
        self.list.pack(fill=BOTH, expand=1, padx=10, pady=10)
        self.button = Button(self.root,
                             text='返回',
                             command=self.goback,
                             bg='AliceBlue')
        self.button.pack(side=RIGHT, padx=(0, 20), pady=(0, 20))
        string = ' | 订单编号  | 购买时间 | 商品id | 物流状态 | 价格'
        self.list.insert("end", string)

        try:
            string = "SELECT order_no,order_time,product_id,status,total_price from orders where user_id = %s order by order_time" % str(
                self.user_id)
            cursor.execute(string)
            data = cursor.fetchone()

            while data != None:
                string = ""
                for item in data:
                    string = string + " | " + str(item)
                self.list.insert("end", string)
                data = cursor.fetchone()
        except Exception as err:
            print(err)

    def goback(self):
        self.list.destroy()
        self.button.destroy()
        choose_window(self.root)


class all_address(object):
    def __init__(self, master=None):

        self.user_id = get_user_id()
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

        self.address = StringVar()

        self.createPage()

    def createPage(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack()

        self.list = Listbox(self.root)
        self.list.pack(fill=BOTH, expand=1, padx=10, pady=10)
        self.button1 = Button(self.root,
                              text='返回',
                              command=self.goback,
                              bg='AliceBlue')
        self.button1.pack(side=RIGHT, padx=(0, 20), pady=(0, 20))
        self.button2 = Button(self.root,
                              text='添加地址',
                              command=self.create_new_addr,
                              bg='AliceBlue')
        self.button2.pack(side=LEFT, padx=(20, 40), pady=(0, 20))
        string = ' | 地址编号 | 具体地址  |  区  |  国家  |  省  |  市'
        self.list.insert("end", string)

        try:
            string = "SELECT addr_id, address_detail,region,country, province,city  FROM address where receiver =  %s" % str(
                self.user_id)
            cursor.execute(string)
            data = cursor.fetchone()

            while data != None:
                string = ""
                for item in data:
                    string = string + " | " + str(item)
                self.list.insert("end", string)
                data = cursor.fetchone()
        except Exception as err:
            print(err)

    def goback(self):
        self.list.destroy()
        self.button1.destroy()
        self.button2.destroy()
        choose_window(self.root)

    def create_new_addr(self):
        self.list.destroy()
        self.button1.destroy()
        self.button2.destroy()
        self.page.destroy()
        Address(self.root)


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
        self.root.iconbitmap("./image/3.ico")
        # 设置窗口宽高固定
        self.root.resizable(0, 0)
        self.createPage()

    def createPage(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack()

        self.list = Listbox(self.root)
        self.list.pack(fill=BOTH, expand=1, padx=10, pady=10)

        self.button1 = Button(self.root,
                              text='返回',
                              command=self.goback,
                              bg='AliceBlue')
        self.button1.pack(side=RIGHT, padx=(0, 20), pady=(0, 20))
        self.button2 = Button(self.root,
                              text='添加评论',
                              command=self.create_new_comment,
                              bg='AliceBlue')
        self.button2.pack(side=LEFT, padx=(20, 40), pady=(0, 20))
        string = " | 用户编号 | 商品编号 | 用户评论 | 用户等级 | 评论点赞数 | 商品打分 | 评论日期 "
        self.list.insert("end", string)

        try:
            cursor.execute(
                "select release_user, product_id, contents,user_level,like_num, star, comment_date from product_comments order by comment_date"
            )
            data = cursor.fetchone()

            while data != None:
                string = ''
                for item in data:
                    string = string + " | " + str(item)
                self.list.insert("end", string)
                data = cursor.fetchone()
        except Exception as err:
            print(err)

    def goback(self):
        self.list.destroy()
        self.button1.destroy()
        self.button2.destroy()
        choose_window(self.root)

    def create_new_comment(self):
        self.list.destroy()
        self.button1.destroy()
        self.button2.destroy()
        self.page.destroy()
        Comment(self.root)
