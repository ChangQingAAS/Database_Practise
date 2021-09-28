import etc
import psycopg2
from tkinter import messagebox
import datetime

class SqlSearch(object):
    def __init__(self):
        self.get_conn()

    # 获取连接
    def get_conn(self):
        try:
            self.conn = psycopg2.connect(database=etc.database,
                                         user=etc.user,
                                         password=etc.password,
                                         host=etc.host,
                                         port=etc.port)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print('Error: %s' % e)

    # 关闭连接
    def close_conn(self):
        try:
            if self.conn:
                self.cursor.close()
                self.conn.close()
        except Exception as e:
            print('Error: %s' % e)

    # 获取用户信息（登录用）
    def get_userinfo(self):
        sql = 'SELECT * FROM consumer'

        # 使用execute()方法执行SQL语句
        self.cursor.execute(sql)

        # 使用fetchall()方法获取全部数据
        result = self.cursor.fetchall()

        user_passwd_dict = {}
        for item in result:
            user_passwd_dict[item[0]] = item[1]

        # 关闭连接
        self.close_conn()
        return user_passwd_dict

    # 注册
    def insert_userinfo(self, user_id, passwd, username, nickname, tel_num,
                        gender, birth_date):
        self.user_id = user_id
        self.passwd = passwd
        self.username = username
        self.nickname = nickname
        self.tel_num = tel_num
        # 如果用户输入的是'男'，把它转化为'M',或是让他选择男女
        self.gender = gender
        # 想办法做成能自己选的框
        self.birth_date = birth_date

        # 提取出user_id的列表
        sql = 'SELECT * FROM consumer'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        user_id_list = []
        for item in result:
            user_id_list.append(item[0])

        # 判断是否存在该用户id
        if int(self.user_id) in user_id_list:
            messagebox.showerror('警告', message='用户id已存在')
        else:
            #for item in result:
            #ulist.append(item['id'])
            try:
                # 获取登录时间，即为当前时间
                self.last_login = datetime.datetime.now().strftime('%Y-%m-%d')
                # sql = 'INSERT INTO 登陆账户(用户名,密码) VALUES(%s,%s)'
                self.cursor.execute(
                    'insert into consumer (user_id, passwd, username, nickname, tel_num, gender, birth_date, last_login) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
                    (self.user_id, self.passwd, self.username, self.nickname,
                     self.tel_num, self.gender, self.birth_date,
                     self.last_login))
                # 提交事务
                self.conn.commit()
                messagebox.showinfo(title='恭喜', message='注册成功')
                self.close_conn()
                return True
            except:
                #messagebox.showerror('警告', message='用户名已存在')
                # 限制提交
                self.conn.rollback()
