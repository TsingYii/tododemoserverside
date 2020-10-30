#! /usr/bin/python3
# -*- coding:utf-8 -*-

import tornado.web
import sys
from tornado.escape import json_decode
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
import time
import base64
import hmac


# 从commons中导入http_response方法
from common.commons import (
    http_response,
)

# 从配置文件中导入错误码
from conf.base import (
    ERROR_CODE,
)


from models import (
    Users
)

########## Configure logging #############
logFilePath = "log/users/users.log"
logger = logging.getLogger("Users")  
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
 
class RegistHandle(tornado.web.RequestHandler):
    """handle /user/regist request
    :param phone: users sign up phone
    :param password: users sign up password
    """

    @property
    def db(self):
        return self.application.db
        
        
    def post(self):
        try:
            #获取入参
            args = json_decode(self.request.body)
            phone = args['phone']
            password = args['password']
        except:
            # 获取入参失败时，抛出错误码及错误信息
            logger.info("RegistHandle: request argument incorrect")
            http_response(self, ERROR_CODE['1001'], 1001)
            return 

        if len(phone)==0 or len(password)==0:
        	  logger.debug("RegistHandle: request argument incorrect")
        	  http_response(self,ERROR_CODE['1001'],1001)
        	  return
        
        ex_user = self.db.query(Users).filter_by(phone=phone).first()
        if ex_user:
            #如果手机号已存在，返回用户已注册信息
            http_response(self, ERROR_CODE['1002'], 1002)
            self.db.close()
            return
        else:
            #用户不存在，数据库表中插入用户信息
            logger.debug("RegistHandle: insert db, user: %s" %phone)
            create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            add_user = Users(phone, password,'','',create_time)                         
            self.db.add(add_user)
            self.db.commit()
            self.db.close()
        	  # 处理成功后，返回成功码“0”及成功信息“ok”
        logger.debug("RegistHandle: regist successfully")
        http_response(self, ERROR_CODE['0'], 0)


class LoginHandle(tornado.web.RequestHandler):
    """handle /user/login request
    :param phone: users sign up phone
    :param password: users sign up password
    """

    @property
    def db(self):
        return self.application.db
    
    def generate_token(self,key, expire=60.0):
        ts_str = str(time.time() + expire)
        ts_byte = ts_str.encode("utf-8")
        sha1_tshex_str = hmac.new(key.encode("utf-8"), ts_byte, 'sha1').hexdigest()
        token = ts_str+':'+sha1_tshex_str
        b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))

        return b64_token.decode("utf-8")
   
        
    def post(self):
        try:
            #获取入参
            args = json_decode(self.request.body)
            phone = args['phone']
            password = args['password']
        except:
            # 获取入参失败时，抛出错误码及错误信息
            logger.info("LoginHandle: request argument incorrect")
            http_response(self, ERROR_CODE['1001'], 1001)
            return 
            # 判断参数是否有值
        if len(phone)==0 or len(password)==0:
        	  logger.debug("LoginHandle: request argument incorrect")
        	  http_response(self,ERROR_CODE['1001'],1001)
        	  return
            # 判断是否存在账号信息
        ex_user = self.db.query(Users).filter_by(phone=phone).first()
        if ex_user==None:
            # 如果手机号不存在,提示先注册
            http_response(self, ERROR_CODE['1003'], 1003)
            self.db.close()
            return
        # 用户存在，判断匹配密码是否一致
        if ex_user.password != password:
            http_response(self,ERROR_CODE['1004'],1004)
            return

        # 处理成功后，返回成功码“0”及成功信息“ok”
        token = self.generate_token(phone,300)
        # 存储token
        users = self.db.query(Users).filter_by(phone=phone)
        users.update({'token':token})
        # 查询头像
        user = users.first()
        logger.info("save token %s",token)
        logger.debug("LoginHandle: login successfully")
        http_response(self, ERROR_CODE['0'], 0,{
            "phone":args['phone'],
            "password":args['password'],
            "token":token,
            "avatarUrl": user.avatarUrl
        })

class LogoutHandle(tornado.web.RequestHandler):
    """handle /user/logout request
    """
    def post(self):
        # 处理成功后，返回成功码“0”及成功信息“ok”
        logger.debug("LogoutHandle: logout successfully")
        http_response(self, ERROR_CODE['0'], 0)

class ProtocolHandle(tornado.web.RequestHandler):
    """handle /user/protocol request
    """
    def get(self):
        # 处理成功后，返回成功码“0”及成功信息“ok”
        logger.debug("ProtocolHandle: get html")
        self.render("index.html")