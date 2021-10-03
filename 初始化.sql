drop table if exists type_product, product,consumer,address,orders,product_comments,purchase;
drop  SEQUENCE if exists orders_id_seq;

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
	 price  int,
	 sales  int,
	 launch_time  DATE,
	 out_time  DATE,
	 details  varchar(100),
	 shop_name  varchar(100),
     PRIMARY KEY (product_id ),
  	CONSTRAINT fk_pro_type FOREIGN KEY(product_id) REFERENCES type_product(type_id)
);

-- 创建顾客表
CREATE TABLE IF NOT EXISTS  consumer (
	 user_id  BIGINT,
	 passwd varchar(12) NOT NULL, 
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
     addr_id            BIGINT  PRIMARY KEY,
     receiver           INT REFERENCES consumer(user_id),
     address_detail     VARCHAR(100),
     region             VARCHAR(20),
     country            VARCHAR(20),
     province           VARCHAR(20),
     city               VARCHAR(20)
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

-- 创建购买记录表
CREATE TABLE IF NOT EXISTS purchase (
     user_id       BIGINT  REFERENCES consumer(user_id),
     product_id    BIGINT REFERENCES  product(product_id)
) ;

-- 添加商品类型
insert into type_product (type_id, type_name) VALUES (1,'电子设备');
insert into type_product (type_id, type_name) VALUES (2,'电子设备');
insert into type_product (type_id, type_name) VALUES (3,'日用百货');


-- 添加商品数据
insert into product (product_id, product_name, type_id, price, sales, launch_time, out_time,details, shop_name) VALUES (01,'iPhone 12', 1, 5000,500,'2021-10-30','2031-10-30','一部手机','苹果手机店');
insert into product (product_id, product_name, type_id, price, sales, launch_time, out_time,details, shop_name) VALUES (02,'OPPO reno 6', 1, 6000,600,'2021-05-30','2031-06-30','一部手机','OPPO手机店');
insert into product (product_id, product_name, type_id, price, sales, launch_time, out_time,details, shop_name) VALUES (03,'蓝月亮洗衣液', 1, 30,60000,'2005-05-30','2041-06-30','洗衣液','蓝月亮官网');

-- 创建顾客数据
insert into consumer (user_id, passwd, username, nickname, tel_num, gender, birth_date, last_login) VALUES (001,'why','why','giao','15222168550','M','2004-05-30','2021-09-30');
insert into consumer (user_id, passwd, username, nickname, tel_num, gender, birth_date, last_login) VALUES (002,'changqingaas','changqingaas','JiaRan','110','F','2010-05-30','2021-09-30');

-- 添加地址数据 
insert into address (addr_id, receiver, address_detail, region, country, province, city) VALUES (0001, 001, '海河路250号', '津南区', '中国','天津市','天津市');
 
 
-- 添加订单数据
insert into orders (order_time, user_id, product_id, status, addr_id, total_price) VALUES ('2021-09-18',001,01,'状态：未送达',0001,5000);
insert into orders (order_time, user_id, product_id, status, addr_id, total_price) VALUES ('2000-09-18',001,02,'状态：未送达',0001,6000);


-- 创建商品评论数据
insert into product_comments (release_user, contents, user_level, like_num, reply_num, star, comment_date) VALUES (001,'good',87,77,2,5,'2021-09-08');


-- 创建购买记录 
insert into purchase(user_id, product_id) VALUES (001,01);
insert into purchase(user_id, product_id) VALUES (001,02);
