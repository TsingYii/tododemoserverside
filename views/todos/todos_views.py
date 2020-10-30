#! /usr/bin/python3
# -*- coding:utf-8 -*-

import tornado.web
import sys
from tornado.escape import json_decode
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

# 从commons中导入http_response方法
from common.commons import (
    http_response,
)

# 从配置文件中导入错误码
from conf.base import (
    ERROR_CODE,
)


from models import (
    Users,
    Todos
)

########## Configure logging #############
logFilePath = "log/todos/todos.log"
logger = logging.getLogger("Todos")  
logger.setLevel(logging.DEBUG)  
handler = TimedRotatingFileHandler(logFilePath,  
                                   when="D",  
                                   interval=1,  
                                   backupCount=30)  
formatter = logging.Formatter('%(asctime)s \
%(filename)s[line:%(lineno)d] %(levelname)s %(message)s',)  
handler.suffix = "%Y%m%d"
handler.setFormatter(formatter)
logger.addHandler(handler)


class TodosHandle(tornado.web.RequestHandler):
    """handle /todo/todos request
    :param phone: users sign up phone
    """

    @property
    def db(self):
        return self.application.db        
        
    def post(self):
        try:
            #获取入参
            args = json_decode(self.request.body)
            phone = args['phone']
        except:
            # 获取入参失败时，抛出错误码及错误信息
            logger.info("TodosHandle: request argument incorrect")
            http_response(self, ERROR_CODE['1001'], 1001)
            return 

        if len(phone)==0:
        	  logger.debug("TodosHandle: request argument incorrect")
        	  http_response(self,ERROR_CODE['1001'],1001)
        	  return
        # 根据手机号查询todos
        ex_todos = self.db.query(Todos.todo).filter_by(phone=phone).all()
        	  # 处理成功后，返回成功码“0”及成功信息“ok”
        logger.debug("TodosHandle: regist successfully")
        logger.debug(ex_todos)
        http_response(self, ERROR_CODE['0'], 0,ex_todos)


class NewTodoHandle(tornado.web.RequestHandler):
    """handle /todo/newtodo request
    :param phone: users sign up phone
    :param todo: user create todo 
    """

    @property
    def db(self):
        return self.application.db
        
        
    def post(self):
        try:
            #获取入参
            args = json_decode(self.request.body)
            phone = args['phone']
            todo = args['todo']
        except:
            # 获取入参失败时，抛出错误码及错误信息
            logger.info("NewTodoHandle: request argument incorrect")
            http_response(self, ERROR_CODE['1001'], 1001)
            return 

        if len(phone)==0 or len(todo)==0:
        	  logger.debug("NewTodoHandle: request argument incorrect")
        	  http_response(self,ERROR_CODE['1001'],1001)
        	  return
        

        #用户不存在，数据库表中插入用户信息
        logger.debug("NewTodoHandle: insert db, todo: %s" %todo)
        create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        add_todo = Todos(phone, todo, create_time)                         
        self.db.add(add_todo)
        self.db.commit()
        self.db.close()
        	  # 处理成功后，返回成功码“0”及成功信息“ok”
        logger.debug("NewTodoHandle: add successfully")
        http_response(self, ERROR_CODE['0'], 0)