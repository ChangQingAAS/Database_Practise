----------------------------------------------------
-- 初始化，先把表清空
drop table if exists sell,favorite,subscribe,coupon,trolley,merchant;
drop table if exists recommend,type_product, product,consumer,address,orders,product_comments,purchase,courier,delivery;
-- drop  SEQUENCE if exists orders_id_seq;
----------------------------------------------------

----------------------------------------------------
-- 建表
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

-- 创建转运商表
CREATE TABLE IF NOT EXISTS courier (
    courier_id      BIGINT,
    courier_name    VARCHAR(100) NOT NULL,
    setup_date      DATE,
    PRIMARY KEY ( courier_id )
);

-- 创建卖家店铺表
CREATE TABLE IF NOT EXISTS merchant (
    merchant_id     BIGINT,
    merchant_level  BIGINT,
    location        VARCHAR(100),
    evaluation      BIGINT,
    PRIMARY KEY ( merchant_id )
);

-- 创建地址表
CREATE TABLE IF NOT EXISTS address (
     addr_id            serial  PRIMARY KEY,
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
     comment_date       DATE,
     product_id         BIGINT
) ;

-- 创建购买记录表
CREATE TABLE IF NOT EXISTS purchase (
     user_id            BIGINT REFERENCES consumer(user_id),
     product_id         BIGINT REFERENCES  product(product_id)
) ;

-- 创建购物车记录表
CREATE TABLE IF NOT EXISTS trolley (
     consumer_id        BIGINT REFERENCES consumer(user_id),
     want_item          BIGINT REFERENCES product(product_id),
     sum                BIGINT
) ;

-- 创建发送货物记录表
CREATE TABLE IF NOT EXISTS delivery (
    deliver_courier     BIGINT REFERENCES courier(courier_id),
    deliver_order       BIGINT REFERENCES orders(order_no),
    original_place      VARCHAR(100) NOT NULL,
    destination         VARCHAR(100) NOT NULL,
    deliver_time        DATE,
    arrival_time        DATE
) ;

-- 创建售卖商品列表
CREATE TABLE IF NOT EXISTS sell (
	seller              BIGINT REFERENCES merchant(merchant_id),
    purchaser           BIGINT REFERENCES consumer(user_id),
    sell_product        BIGINT REFERENCES product(product_id)
) ;

-- 创建推荐表
CREATE TABLE IF NOT EXISTS recommend (
	user_id             BIGINT REFERENCES consumer(user_id),
	product_id          BIGINT REFERENCES product(product_id)
) ;

-- 创建收藏夹列表
CREATE TABLE IF NOT EXISTS favorite (
	user_id             BIGINT REFERENCES consumer(user_id),
	favorite_product    BIGINT REFERENCES product(product_id)
) ;

-- 创建订阅列表
CREATE TABLE IF NOT EXISTS subscribe (
	user_id             BIGINT REFERENCES consumer(user_id),
	subscribe_merchant  BIGINT REFERENCES merchant(merchant_id)
) ;

-- 创建优惠券列表
CREATE TABLE IF NOT EXISTS coupon (
	user_id             BIGINT REFERENCES consumer(user_id),
	discount            DECIMAL(3,2),
    deadline            DATE
) ;
----------------------------------------------------


----------------------------------------------------
-- 创建执行函数

-- 创建商品product_id执行函数
CREATE OR REPLACE FUNCTION product_id_func()
returns trigger
language plpgsql
AS $$
BEGIN
    delete 
    from product
    where (product_id < 0);
    return new;
END;
$$;

-- 创建商品price执行函数
CREATE OR REPLACE FUNCTION product_price_func()
returns trigger
language 'plpgsql'
AS $$
BEGIN
    update product
    set price = 99999
    where price < 0;
    return new;
END;
$$;

-- 创建商品sales执行函数
CREATE OR REPLACE FUNCTION product_sales_func()
returns trigger
language 'plpgsql'
AS $$
BEGIN
    update product
    set sales = 0
    where sales < 0;
    return new;
END;
$$;

-- 创建商品out_time执行函数
CREATE OR REPLACE FUNCTION product_outtime_func()
returns trigger
language 'plpgsql'
AS $$
BEGIN
    update product
    set out_time = launch_time
    where out_time < launch_time;
    return new;
END;
$$;

-- 创建消费者id执行函数
CREATE OR REPLACE FUNCTION consumer_id_func()
returns trigger
language 'plpgsql'
AS $$
BEGIN
    delete
    from consumer
    where user_id < 0;
    return new;
END;
$$;

-- 创建消费者last_login执行函数
CREATE OR REPLACE FUNCTION consumer_lastlogin_func()
returns trigger
language 'plpgsql'
AS $$
BEGIN
    update consumer
    set last_login = birth_date
    where last_login < birth_date;
    return new;
END;
$$;

-- 创建商品类型id执行函数
CREATE OR REPLACE FUNCTION type_id_func()
returns trigger
language 'plpgsql'
AS $$
BEGIN
    delete
    from type_product
    where type_id < 0;
    return new;
END;
$$;

-- 创建订单id执行函数
CREATE OR REPLACE FUNCTION order_id_func()
returns trigger
language 'plpgsql'
AS $$
BEGIN
    delete
    from orders
    where order_no < 0;
    return new;
END;
$$;

-- 创建订单order_time执行函数
CREATE OR REPLACE FUNCTION order_time_func()
returns trigger
language 'plpgsql'
AS $$
BEGIN
    update orders
    set order_time = '1990-01-01'
    where order_time < '1990-01-01';
    return new;
END;
$$;

-- 创建订单total_price执行函数
CREATE OR REPLACE FUNCTION order_totalprice_func()
returns trigger
language 'plpgsql'
AS $$
BEGIN
    update orders
    set total_price = 0
    where total_price < 0;
    return new;
END;
$$;

-- 创建地址id执行函数
CREATE OR REPLACE FUNCTION address_id_func()
returns trigger
language 'plpgsql'
AS $$
BEGIN
    delete
    from address
    where addr_id < 0;
    return new;
END;
$$;

-- 创建商品评论user_level执行函数
CREATE OR REPLACE FUNCTION comments_userlevel_func()
returns trigger 
language 'plpgsql'
AS $$
BEGIN
    update product_comments
    set user_level = 0
    where user_level < 0 or user_level > 100;
    return new;
END;
$$;

-- 创建商品评论like_num执行函数
CREATE OR REPLACE FUNCTION comments_likenum_func()
returns trigger 
language 'plpgsql'
AS $$
BEGIN
    update product_comments
    set like_num = 0
    where like_num < 0;
    return new;
END;
$$;

-- 创建商品评论reply_num执行函数
CREATE OR REPLACE FUNCTION comments_replynum_func()
returns trigger 
language 'plpgsql'
AS $$
BEGIN
    update product_comments
    set reply_num = 0
    where reply_num < 0;
    return new;
END;
$$;

-- 创建商品评论star执行函数
CREATE OR REPLACE FUNCTION comments_star_func()
returns trigger 
language 'plpgsql'
AS $$
BEGIN
    update product_comments
    set star = 0
    where star < 0 or star > 5;
    return new;
END;
$$;

-- 创建商品评论comment_date执行函数
CREATE OR REPLACE FUNCTION comments_date_func()
returns trigger 
language 'plpgsql'
AS $$
BEGIN
    update product_comments
    set comment_date = '1990-01-01'
    where comment_date < '1990-01-01';
    return new;
END;
$$;

-- 创建转运商id执行函数
CREATE OR REPLACE FUNCTION courier_id_func()
returns trigger 
language 'plpgsql'
AS $$
BEGIN
    delete
    from courier
    where courier_id < 0;
    return new;
END;
$$;

-- 创建转运商setup_time执行函数
CREATE OR REPLACE FUNCTION courier_setuptime_func()
returns trigger 
language 'plpgsql'
AS $$
BEGIN
    update courier
    set setup_date = '1990-01-01'
    where setup_date < '1990-01-01';
    return new;
END;
$$;

-- 创建发送货物deliver_time执行函数
CREATE OR REPLACE FUNCTION delivery_delivertime_func()
returns trigger 
language 'plpgsql'
AS $$
BEGIN
    update delivery
    set deliver_time = '1990-01-01'
    where deliver_time < '1990-01-01';
    return new;
END;
$$;

-- 创建发送货物arrival_time执行函数
CREATE OR REPLACE FUNCTION delivery_arrivaltime_func()
returns trigger 
language 'plpgsql'
AS $$
BEGIN
    update delivery
    set arrival_time = deliver_time
    where arrival_time < deliver_time;
    return new;
END;
$$;

-- 创建推荐列表recommend_from_orders的函数
CREATE OR REPLACE FUNCTION recomend_from_orders_func()
returns trigger
language 'plpgsql'
AS $$
begin
	insert into recommend VALUES(new.user_id, new.product_id);
	return NULL;
end;
$$;

-- 创建推荐列表recommend_from_product_comments的函数
CREATE OR REPLACE FUNCTION recomend_from_product_comments_func()
returns trigger
language 'plpgsql'
AS $$
begin
	if new.star >= 4 then
		insert into recommend VALUES(new.release_user, new.product_id);
	end if;
	return NULL;
end;
$$;
----------------------------------------------------

----------------------------------------------------
-- 创建触发器

-- 创建商品product_id触发器
CREATE TRIGGER check_product_insert_id
after insert on product
for each row
execute procedure product_id_func();

-- 创建商品price触发器
CREATE TRIGGER check_product_insert_price
after insert on product
for each row
execute procedure product_price_func();

CREATE TRIGGER check_product_up_price
after update on product
for each row
execute procedure product_price_func();

-- 创建商品sales触发器
CREATE TRIGGER check_product_insert_sales
after insert on product
for each row
execute procedure product_sales_func();

CREATE TRIGGER check_product_update_sales
after update on product
for each row
execute procedure product_sales_func();

-- 创建商品out_time触发器
CREATE TRIGGER check_product_insert_outtime
after insert on product
for each row
execute procedure product_outtime_func();

CREATE TRIGGER check_product_update_outtime
after update on product
for each row
execute procedure product_outtime_func();

-- 创建消费者id触发器
CREATE TRIGGER check_consumer_insert_id
after insert on consumer
for each row
execute procedure consumer_id_func();

-- 创建消费者last_login触发器
CREATE TRIGGER check_consumer_insert_lastlogin
after insert on consumer
for each row
execute procedure consumer_lastlogin_func();

CREATE TRIGGER check_consumer_update_lastlogin
after update on consumer
for each row
execute procedure consumer_lastlogin_func();

-- 创建商品类型id触发器
CREATE TRIGGER check_type_insert_id
after insert on type_product
for each row
execute procedure type_id_func();

-- 创建订单id触发器
CREATE TRIGGER check_orders_insert_id
after insert on orders
for each row
execute procedure order_id_func();

-- 创建订单order_time触发器
CREATE TRIGGER check_orders_insert_time
after insert on orders
for each row
execute procedure order_time_func();

CREATE TRIGGER check_orders_update_time
after update on orders
for each row
execute procedure order_time_func();

-- 创建订单total_price触发器
CREATE TRIGGER check_orders_insert_totalprice
after insert on orders
for each row
execute procedure order_totalprice_func();

CREATE TRIGGER check_orders_update_totalprice
after update on orders
for each row
execute procedure order_totalprice_func();

-- 创建地址id触发器
CREATE TRIGGER check_address_insert_id
after insert on address
for each row
execute procedure address_id_func();

-- 创建商品评论user_level触发器
CREATE TRIGGER check_comments_insert_userlevel
after insert on product_comments
for each row
execute procedure comments_userlevel_func();

CREATE TRIGGER check_comments_update_userlevel
after update on product_comments
for each row
execute procedure comments_userlevel_func();

-- 创建商品评论like_num触发器
CREATE TRIGGER check_comments_insert_likenum
after insert on product_comments
for each row
execute procedure comments_likenum_func();

CREATE TRIGGER check_comments_update_likenum
after update on product_comments
for each row
execute procedure comments_likenum_func();

-- 创建商品评论reply_num触发器
CREATE TRIGGER check_comments_insert_replynum
after insert on product_comments
for each row
execute procedure comments_replynum_func();

CREATE TRIGGER check_comments_update_replynum
after update on product_comments
for each row
execute procedure comments_replynum_func();

-- 创建商品评论star触发器
CREATE TRIGGER check_comments_insert_star
after insert on product_comments
for each row
execute procedure comments_star_func();

CREATE TRIGGER check_comments_update_star
after update on product_comments
for each row
execute procedure comments_star_func();

-- 创建商品评论comment_date触发器
CREATE TRIGGER check_comments_insert_date
after insert on product_comments
for each row
execute procedure comments_date_func();

CREATE TRIGGER check_comments_update_date
after update on product_comments
for each row
execute procedure comments_date_func();

-- 创建转运商id触发器
CREATE TRIGGER check_courier_insert_id
after insert on courier
for each row
execute procedure courier_id_func();

-- 创建转运商setup_date触发器
CREATE TRIGGER check_courier_insert_setuptime
after insert on courier
for each row
execute procedure courier_setuptime_func();

CREATE TRIGGER check_courier_update_setuptime
after update on courier
for each row
execute procedure courier_setuptime_func();

-- 创建发送货物deliver_time触发器
CREATE TRIGGER check_delivery_insert_delivertime
after insert on delivery
for each row
execute procedure delivery_delivertime_func();

-- 创建发送货物arrival_time触发器
CREATE TRIGGER check_delivery_insert_arrivaltime
after insert on delivery
for each row
execute procedure delivery_arrivaltime_func();

-- 创建推荐列表recommend_from_orders触发器
CREATE TRIGGER recomend_from_orders
after insert on orders
for each row
execute procedure recomend_from_orders_func();

-- 创建推荐列表recommend_from_product_comments触发器
CREATE TRIGGER recomend_from_product_comments
after insert on product_comments
for each row
execute procedure recomend_from_product_comments_func();
----------------------------------------------------

----------------------------------------------------
-- 数据库操作：增删改查

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
----------------------------------------------------
