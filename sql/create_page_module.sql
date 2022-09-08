-- auto-generated definition
create table page_module
(
    id          int auto_increment
        primary key,
    module_name varchar(50)                        null,
    created_at  datetime default CURRENT_TIMESTAMP null,
    updated_at  datetime default CURRENT_TIMESTAMP null,
    deleted_at  datetime                           null
)
    comment '页面模块表';

