from tkinter import *
from tkinter.messagebox import *
# from MainPage import *
from tkinter import messagebox
import psycopg2
import etc
from Sql_Search import SqlSearch
import page1
from date import Date
from for_user_id import get_user_id
import etc
import choose
import datetime
from tkinter import ttk


class Comment(object):
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

        self.contents = StringVar()
        self.star = StringVar()

        self.createPage()

    def createPage(self):

        self.page = Frame(self.root)  # 创建Frame
        self.page.pack()
        Label(self.page).grid(row=0, stick=W)

        Label(self.page, text='评论内容: ').grid(row=1, stick=W, pady=10)
        Entry(self.page, textvariable=self.contents).grid(row=1,
                                                          column=1,
                                                          stick=W
                                                            )

        Label(self.page, text='商品打分: ').grid(row=3, stick=W, pady=10)
        self.star.set('5')  # 默认选中CCC==combobox.current(2)
        values = ['1', '2', '3', '4', '5']
        self.combobox = ttk.Combobox(
            master=self.page,  # 父容器
            height=4,  # 高度,下拉显示的条目数量
            width=8,  # 宽度
            state='normal',  # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled
            cursor='arrow',  # 鼠标移动时样式 arrow, circle, cross, plus...
            font=('', 16),  # 字体
            textvariable=self.star,  # 通过StringVar设置可改变的值
            values=values,  # 设置下拉框的选项
        )
        self.combobox.grid(row=3, column=1, stick=W )

        Button(self.page, text='确认', command=self.Back,
               bg='AliceBlue').grid(row=10,
                                    column=1,
                                    stick=W,
                                    columnspan=40
                                      )

    def Back(self):
        user_id = get_user_id()
        contents = self.contents.get()
        user_level = 0
        like_num = 0
        reply_num = 0
        star = self.star.get()
        comment_date = datetime.datetime.now().strftime("%Y-%m-%d")

        try:
            #连接数据库需要提供相应的数据库名称、用户名、密码、地址、端口等信息
            db = psycopg2.connect(database=etc.database,
                                  user=etc.user,
                                  password=etc.password,
                                  host=etc.host,
                                  port=etc.port)
            cursor = db.cursor()
            string = "insert into product_comments (release_user, contents, user_level, like_num, reply_num,star,comment_date) VALUES (%s,'%s',%s,%s, %s, %s,'%s')" % (
                user_id, contents, user_level, like_num, reply_num, star,
                comment_date)
            cursor.execute(string)
            db.commit()
            messagebox.showinfo(title='success!', message='添加成功')

        except Exception as err:
            print(err)

        self.page.destroy()
        choose.all_comment(self.root)
