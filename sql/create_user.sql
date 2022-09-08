-- auto-generated definition
create table user
(
    id         int auto_increment,
    user_name  varchar(100)                       not null,
    user_pwd   varchar(255)                       not null,
    created_at datetime default CURRENT_TIMESTAMP not null,
    updated_at datetime default CURRENT_TIMESTAMP not null,
    deleted_at datetime                           null,
    constraint user_id_uindex
        unique (id),
    constraint user_user_name_uindex
        unique (user_name)
)
    comment '用户表';

alter table user
    add primary key (id);

