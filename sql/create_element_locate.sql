-- auto-generated definition
create table element_locate
(
    id                  int auto_increment
        primary key,
    element_type        int                                not null comment '定位方法ID',
    element_locate_name varchar(50)                        not null comment '定位元素名称',
    created_at          datetime default CURRENT_TIMESTAMP not null,
    updated_at          datetime default CURRENT_TIMESTAMP not null,
    deleted_at          datetime                           null
)
    comment '元素定位方法';

