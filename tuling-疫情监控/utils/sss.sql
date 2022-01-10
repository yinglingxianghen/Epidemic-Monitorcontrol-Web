create table text (id int(11) not null auto_increment primary key,
    update_time datetime default null comment '数据最后更新时间',
    content TEXT,
    username varchar(50)
    )engine=InnoDB default charset=utf8mb4;




grant all PRIVILEGES on *.* to %username%@'%' identified by '%password%';
grant all PRIVILEGES on *.* to root@'%' identified by 'xiaozhang';