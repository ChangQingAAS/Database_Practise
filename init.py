# 如果选择初始化参数，则执行该文件，初始化数据库
import psycopg2
import etc

def init():  
    conn = psycopg2.connect(database = etc.database,user=etc.user,password=etc.password, host=etc.host, port=etc.port)
    cursor = conn.cursor()

    # 读取sql语句，以进行初始化
    with open('./初始化.sql', 'r',encoding = 'utf-8') as f:
        strings = f.read()

    try:
        cursor.execute(strings)
        print("success init!")
    except Exception as e:
        print('Error: %s' % e)


    conn.commit()