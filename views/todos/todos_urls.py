#! /usr/bin/python3
# -*- coding:utf-8 -*-


from __future__ import unicode_literals
from .todos_views import (
    TodosHandle,
    NewTodoHandle
)

urls = [
    #从 /todo/todos 过来的请求，将调用 todos_views 里面的 TodosHandle 类
    (r'todos', TodosHandle),
    (r'newtodo', NewTodoHandle),
]
	