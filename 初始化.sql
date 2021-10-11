drop table if exists type_product, product,consumer,address,orders,product_comments,purchase;
-- drop  SEQUENCE if exists orders_id_seq;

-- 创建商品类型表
CREATE TABLE IF NOT EXISTS  type_product(
	 type_id  BIGINT,
	 type_name  VARCHAR(100),
	PRIMARY KEY ( type_id )
);

-- 创建商品表
CREATE TABLE IF NOT EXISTS  product(
	 product_id  BIGINT ,
	 product_name  VARCHAR(100) NOT NULL,
	 type_id  int,
	 price  DECIMAL(7,2),
	 sales  int,
	 launch_time  DATE,
	 out_time  DATE,
	 details  varchar(500),
	 shop_name  varchar(100),
     PRIMARY KEY (product_id ),
  	CONSTRAINT fk_pro_type FOREIGN KEY(type_id) REFERENCES type_product(type_id)
);

-- 创建顾客表
CREATE TABLE IF NOT EXISTS  consumer (
	 user_id  BIGINT,
	 passwd varchar(20) NOT NULL, 
	 username  VARCHAR(100) NOT NULL,
	 nickname  VARCHAR(100) NOT NULL,
	 tel_num  VARCHAR(11) NOT NULL,
	 gender  CHAR(1),
	 birth_date  DATE,
	 last_login  DATE,
	PRIMARY KEY ( user_id ),
	CONSTRAINT user_sex CHECK (
		 gender  = 'M' OR  gender  = 'F'
	)
) ;

-- 创建地址表
CREATE TABLE IF NOT EXISTS address (
     addr_id            serial,
     receiver           int REFERENCES consumer(user_id),
     address_detail     varchar(100),
     region             varchar(20),
     country            varchar(20),
     province           varchar(20),
     city               varchar(20),
	PRIMARY KEY(addr_id)
) ;

-- 创建订单表
CREATE TABLE IF NOT EXISTS  orders (
     order_no           serial,
     order_time         DATE,
     user_id            INT REFERENCES consumer(user_id),
     product_id         INT REFERENCES product(product_id),
     status             VARCHAR(10),
     addr_id            INT REFERENCES address(addr_id),
     total_price        DECIMAL(7,2),
	 PRIMARY KEY(order_no)
) ;

-- --增加自增序列
-- CREATE SEQUENCE orders_id_seq 
--     INCREMENT 1 
--     START 1 
--     NO MINVALUE 
--     NO MAXVALUE 
--     CACHE 2;
-- --增加键id
-- alter table orders add column order_no int;
-- --修改键id为自增序列
-- alter table orders alter column order_no set default nextval('orders_id_seq');


-- 创建商品评论表
CREATE TABLE IF NOT EXISTS product_comments (
     release_user       BIGINT  REFERENCES consumer(user_id),
     contents           VARCHAR(100),
     user_level         INT,
     like_num           INT,
     reply_num          INT,
     star               INT,
     comment_date       DATE
) ;

-- 创建商品评论user_level执行函数
CREATE OR REPLACE FUNCTION check_level_func()
returns trigger 
language plpgsql
AS $$
BEGIN
    update product_comments
    set user_level = 0
    where (user_level < 0 or user_level > 5);
    return new;
END;
$$;

-- 创建商品评论user_level触发器
CREATE TRIGGER check_level
after insert on product_comments
for each row
execute procedure check_level_func();

-- 创建商品评论star执行函数
CREATE OR REPLACE FUNCTION check_star_func()
returns trigger 
language 'plpgsql'
AS $$
BEGIN
    update product_comments
    set star = 0
    where (star < 0 or star > 5);
    return new;
END;
$$;

-- 创建商品评论star触发器
CREATE TRIGGER check_star
after insert on product_comments
for each row
execute procedure check_star_func();

-- 创建购买记录表
CREATE TABLE IF NOT EXISTS purchase (
     user_id       BIGINT  REFERENCES consumer(user_id),
     product_id    BIGINT REFERENCES  product(product_id)
) ;

-- 添加商品类型
insert into type_product (type_id, type_name) VALUES (1,'电子设备');
insert into type_product (type_id, type_name) VALUES (2,'日用百货');
insert into type_product (type_id, type_name) VALUES (3,'文具');
insert into type_product (type_id, type_name) VALUES (4,'书籍');




-- 添加商品数据
insert into product (product_id, product_name, type_id, price, sales, launch_time, out_time,details, shop_name) VALUES (01,'iPhone 12', 1, 5000.0,500,'2021-10-30','2031-10-30','一部手机','苹果手机店');
insert into product (product_id, product_name, type_id, price, sales, launch_time, out_time,details, shop_name) VALUES (02,'OPPO reno 6', 1, 6000.0,600,'2021-05-30','2031-06-30','一部手机','OPPO手机店');
insert into product (product_id, product_name, type_id, price, sales, launch_time, out_time,details, shop_name) VALUES (03,'蓝月亮洗衣液', 2, 30.00,56787,'2013-05-30','2041-06-30','洗衣液','蓝月亮官网');
insert into product (product_id, product_name, type_id, price, sales, launch_time, out_time,details, shop_name) VALUES (04,'乐扣水杯', 2, 30.0,60858,'2007-07-27','2071-07-12','新款运动塑料水杯学生杯便携随手带杯子两件套','乐扣乐扣京东自营旗舰店');
insert into product (product_id, product_name, type_id, price, sales, launch_time, out_time,details, shop_name) VALUES (05,'晨光水笔替芯', 3, 16.8,4274,'2004-05-30','2031-04-24','
晨光(M&G) 中性替芯水笔芯 黑 0.7mm学生办公文具 黑色 20支/盒','晨光文具京东自营');
insert into product (product_id, product_name, type_id, price, sales, launch_time, out_time,details, shop_name) VALUES (06,'高等数学同济第七版', 1, 68.8,214,'2005-05-30','2022-06-30','高等数学上下册：教材+习题全解指南','高等教育出版社');

-- 创建顾客数据
insert into consumer (user_id, passwd, username, nickname, tel_num, gender, birth_date, last_login) VALUES (001,'why','why','giao','15222168550','M','2004-05-30','2021-09-30');
insert into consumer (user_id, passwd, username, nickname, tel_num, gender, birth_date, last_login) VALUES (002,'changqingaas','changqingaas','JiaRan','110','F','2010-05-30','2021-09-30');

-- 添加地址数据 
insert into address (receiver, address_detail, region, country, province, city) VALUES ( 001, '海河路250号', '津南区', '中国','天津市','天津市');

-- 添加订单数据
insert into orders (order_time, user_id, product_id, status, addr_id, total_price) VALUES ('2021-09-18',001,01,'状态：未送达',0001,5000);
insert into orders (order_time, user_id, product_id, status, addr_id, total_price) VALUES ('2000-09-18',002,02,'状态：未送达',0001,6000);


-- 创建商品评论数据
insert into product_comments (release_user, contents, user_level, like_num, reply_num, star, comment_date) VALUES (001,'good',87,77,2,5,'2021-09-08');


-- 创建购买记录 
insert into purchase(user_id, product_id) VALUES (001,01);
insert into purchase(user_id, product_id) VALUES (002,02);
