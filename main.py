#! /usr/bin/python3
# -*- coding:utf-8 -*-
# Author: demo
# Email: demo@demo.com
# Version: demo

import tornado.ioloop
import tornado.web
import os
import sys
from tornado.options import define,options
from common.url_router import include, url_wrapper
from tornado.options import define,options
from models import initdb
from sqlalchemy.orm import scoped_session, sessionmaker
from conf.base import BaseDB, engine

class Application(tornado.web.Application):
    def __init__(self):
        initdb()
        handlers = url_wrapper([
        (r"/users/", include('views.users.users_urls')),
        (r"/todo/", include('views.todos.todos_urls')),
         (r"/upload/", include('views.upload.upload_urls'))
        ])
        #定义 Tornado 服务器的配置项，如 static/templates 目录位置，debug 级别等
        settings = dict(
            debug=True,
            static_path=os.path.join(os.path.dirname(__file__),"static"),
            template_path=os.path.join(os.path.dirname(__file__), "templates")
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        self.db = scoped_session(sessionmaker(bind=engine,
                                  autocommit=False, autoflush=True,
                                  expire_on_commit=False))

if __name__ == '__main__':
    print ("Tornado 服务已经起来了\r")
    tornado.options.parse_command_line()
    Application().listen(8089, xheaders=True)
    tornado.ioloop.IOLoop.instance().start()