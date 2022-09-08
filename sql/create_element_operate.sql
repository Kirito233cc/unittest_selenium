-- auto-generated definition
create table element_operate
(
    id           int auto_increment,
    operate_type int                                not null comment '操作类型',
    operate_name varchar(100)                       not null comment '操作名称',
    created_at   datetime default CURRENT_TIMESTAMP not null,
    updated_at   datetime default CURRENT_TIMESTAMP not null,
    deleted_at   datetime                           null,
    constraint element_operate_id_uindex
        unique (id)
)
    comment '元素操作表';

alter table element_operate
    add primary key (id);

