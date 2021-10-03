import datetime
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

order_time =datetime.datetime.now().strftime("%Y-%m-%d")
order_time = '\'' + order_time + '\''
print(order_time)

product_id = 1

cursor.execute("select price from product where product_id = %s",
                str(product_id))
total_price = cursor.fetchone()[0]

cursor.execute(
            "insert into orders (order_time, user_id, product_id, status, addr_id, total_price) VALUES (%s,%s,%s,'状态：未送达',0001,%s)" %(str(order_time), str(1), str(product_id), total_price))
        