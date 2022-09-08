-- auto-generated definition
create table element
(
    id              int unsigned auto_increment
        primary key,
    element_name    varchar(100) default ''                not null comment '元素名称',
    element_type    int          default 0                 not null comment '元素定位方式：0-XPATH，1-id，2-css',
    element_address varchar(250) default ''                not null comment '元素位置',
    created_at      timestamp    default CURRENT_TIMESTAMP null,
    updated_at      timestamp    default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP,
    deleted_at      timestamp                              null
)
    comment '元素对象表';

