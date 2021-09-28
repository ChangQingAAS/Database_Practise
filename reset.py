# 如果选择reset参数，则执行该文件，重置数据库
import psycopg2
import etc

def reset():  
    conn = psycopg2.connect(database = etc.database,user=etc.user,password=etc.password, host=etc.host, port=etc.port)
    cursor = conn.cursor()

    strings = "drop table if exists type_product, product,consumer,address,orders,product_comments,purchase;"

    try:
        cursor.execute(strings)
        print("success reset!")
    except Exception as e:
        print('Error: %s' % e)


    conn.commit()