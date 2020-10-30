#! /usr/bin/python3
# -*- coding:utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
engine = create_engine('mysql://root:123456@localhost:3306/demo?charset=utf8', encoding="utf8", echo=False)
BaseDB = declarative_base()

#服务器端 IP+Port，请修改对应的IP
SERVER_HEADER = "http://140.143.135.116:8089"

ERROR_CODE = {
    "-1": "失败",
    "0": "成功",
    #Users error code
    "1001": "入参非法",
    "1002": "用户已注册，请直接登录",
    "1003": "账号不存在,请先注册",
    "1004": "密码错误",

    "2001": "上传图片不能为空"
}