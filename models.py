#! /usr/bin/python3
# -*- coding:utf-8 -*-

from conf.base import BaseDB, engine
import sys
from sqlalchemy import (
Column, 
Integer,
    String, 
    DateTime
)

    
class Users(BaseDB):
    """table for users
    """
    __tablename__ = "users"
    #定义表结构，包括id，phone，password，createTime,avatarUrl
    id = Column(Integer, primary_key=True)
    phone = Column(String(50), nullable=False)
    password = Column(String(50), nullable=True)
    avatarUrl = Column(String(200), nullable=True)
    token = Column(String(500), nullable=True)
    createTime = Column(DateTime, nullable=True)
    
    def __init__(self, phone, password,avatarUrl, token,createTime):
        self.phone = phone
        self.password = password
        self.avatarUrl = avatarUrl
        self.token = token
        self.createTime = createTime

class Todos(BaseDB):
    """table for todos
    """
    __tablename__ = "todos"
    #定义表结构，包括id，todo,createTime
    id = Column(Integer, primary_key=True)
    phone = Column(String(50), nullable=False)
    todo = Column(String(50), nullable=False)
    createTime = Column(DateTime, nullable=True)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

    
    
    def __init__(self, phone,todo, createTime):
        self.phone = phone
        self.todo = todo
        self.createTime = createTime    
    
def initdb():
    BaseDB.metadata.create_all(engine)
    
if __name__ == '__main__':
    print ("Initialize database")
    initdb()