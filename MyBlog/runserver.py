#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.options
import tornado.httpserver
from tornado.options import options
from myblog import Application

def start():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    start()
