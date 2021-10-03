from tkinter import *
from tkinter.messagebox import *
# from MainPage import *
import choose
import psycopg2
import etc
from signup import *
from Sql_Search import SqlSearch
from for_user_id import write_user_id


class LoginPage(object):
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
        self.createPage()

    def createPage(self):
        '''
        登录页面
        1:创建图片组件
        2:根目录基础上添加Frame容器
        3:Frame容器上添加注册控件
        '''
        bm = PhotoImage(
            file=r'C:\\Users\\admin\\Desktop\\大三上课程\\数据库实践\\databse_practise\\image\\1.png')
        self.lab3 = Label(self.root, image=bm)
        self.lab3.bm = bm
        self.lab3.pack()

        self.page = Frame(self.root,bg = 'AliceBlue')  # 创建Frame
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

        Button(self.page, text='登录', command=self.login).grid(row=3, column=0)
        Button(self.page, text='注册', command=self.signup).grid(row=3, column=1)

        Button(self.page, text='退出', command=self.page.quit).grid(row=3,column=2)

    def cancel(self):
        # 清空用户输入的用户名和密码
        user.set('')
        passwd.set('')

    def login(self):
        deter = True
        tag = 1
        # 获取用户名和密码
        obj = SqlSearch()
        user_passwd_dict = obj.get_userinfo()
        user_id = int(self.user_id.get())
        passwd = self.passwd.get()
        for key in user_passwd_dict:
            if user_id == key and passwd == user_passwd_dict[key]:
                #messagebox.showinfo(title='恭喜', message='登陆成功')  # 登陆成功则执行begin函数
                deter = False
                #self.page.destroy()
                #MainPage(self.root)
                tag = 2
                break
            else:
                tag = 1
                #break
                #self.page.destroy()
                #MainPage(self.root)

        if tag == 1:
            messagebox.showerror('警告', message='用户名或密码错误')
            showinfo(title='错误', message='账号或密码错误！')
        else:
            messagebox.showinfo(title='恭喜', message='登陆成功')  # 登陆成功则执行begin函数
            deter = False
            self.lab3.destroy()
            self.page.destroy()
            self.root.user_id = user_id
            write_user_id(user_id)
            choose.choose_window(self.root)

    def signup(self):
        self.lab3.destroy()
        self.page.destroy()
        SignupPage(self.root)