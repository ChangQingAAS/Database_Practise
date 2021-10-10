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


class Address(object):
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

        self.country = StringVar()
        self.province = StringVar()
        self.city = StringVar()
        self.region = StringVar()
        self.address_detail = StringVar()

        self.createPage()

    def createPage(self):

        self.page = Frame(self.root)  # 创建Frame
        self.page.pack()
        Label(self.page).grid(row=0, stick=W)

        Label(self.page, text='国家: ').grid(row=1, stick=W, pady=10)
        Entry(self.page, textvariable=self.country).grid(row=1,
                                                         column=1,
                                                         stick=E)

        Label(self.page, text='省份: ').grid(row=2, stick=W, pady=10)
        Entry(self.page, textvariable=self.province).grid(row=2,
                                                          column=1,
                                                          stick=E)

        Label(self.page, text='城市: ').grid(row=3, stick=W, pady=10)
        Entry(self.page, textvariable=self.city).grid(row=3, column=1, stick=E)

        Label(self.page, text='区: ').grid(row=4, stick=W, pady=10)
        Entry(self.page, textvariable=self.region).grid(row=4,
                                                        column=1,
                                                        stick=E)

        Label(self.page, text='详细地址: ').grid(row=5, stick=W, pady=10)
        Entry(self.page, textvariable=self.address_detail).grid(row=5,
                                                                column=1,
                                                                stick=E)

        Button(self.page, text='确认', command=self.Back,
               bg='AliceBlue').grid(row=8,
                                    column=1,
                                    stick=W,
                                    pady=10,
                                    columnspan=80)

    def Back(self):
        country =    self.country.get()  
        province =  self.province.get() 
        city =  self.city.get()
        region =  self.region.get() 
        address_detail =  self.address_detail.get() 
        user_id = get_user_id()

        try:
            #连接数据库需要提供相应的数据库名称、用户名、密码、地址、端口等信息
            db = psycopg2.connect(database=etc.database,
                                  user=etc.user,
                                  password=etc.password,
                                  host=etc.host,
                                  port=etc.port)
            cursor = db.cursor()
            string = "insert into address (receiver, address_detail, region, country, province,city) VALUES (%s,'%s','%s','%s', '%s', '%s')" % (
                str(user_id), str(address_detail), str(region), str(country),
                str(province), str(city))
            cursor.execute(string)
            db.commit()
            messagebox.showinfo(title='success!', message='添加成功')

        except Exception as err:
            print(err)

        self.page.destroy()
        choose.all_address(self.root)
