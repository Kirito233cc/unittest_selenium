-- auto-generated definition
create table page_module_detail
(
    id             int auto_increment
        primary key,
    page_module_id int                                not null comment '对应模块表的ID',
    element_id     int                                not null comment '对应要寻找的element的表id',
    operate_type   int                                null comment '元素所要执行的操作',
    send_msg       varchar(255)                       null comment '部分操作下所要传输的值',
    operate_step   int                                not null comment '操作顺序',
    created_at     datetime default CURRENT_TIMESTAMP not null,
    updated_at     datetime default CURRENT_TIMESTAMP null,
    deleted_at     datetime                           null
)
    comment '页面模块详情表（具体调用的元素及顺序）';

