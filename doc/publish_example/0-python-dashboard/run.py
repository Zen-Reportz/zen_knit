# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""
from werkzeug.middleware.proxy_fix import ProxyFix

from app import app, db
from os import getenv
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

#
def _root_app(_, resp):
    resp(b'404 Not Found', [('Content-Type', 'text/plain')])
    return [b'Apache Airflow is not at this location']
#
# application = DispatcherMiddleware(
#     _root_app , { "/foo": app}
# )
app.wsgi_app = ProxyFix(app.wsgi_app,  x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)
# app.wsgi_app = DispatcherMiddleware(simple, {'/abc/123': app.wsgi_app})


if __name__ == "__main__":
    app.run(port=5001)
    # run_simple(
    #     "0.0.0.0",
    #     int("5001"),
    #     application,
    #     use_debugger=False,
    #     threaded=True,
    # )
#
# from flask import Flask
#
# from werkzeug.middleware.dispatcher import DispatcherMiddleware
# from werkzeug.serving import run_simple
# from werkzeug.contrib.fixers import ProxyFix
# app = Flask(__name__)
#
# def _root_app(_, resp):
#     resp(b'404 Not Found', [('Content-Type', 'text/plain')])
#     return [b'Apache Airflow is not at this location']
#
# application = DispatcherMiddleware(
#     _root_app , { "/foo": app}
# )
# app.wsgi_app = ProxyFix(app.wsgi_app,  x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)
#
# @app.route('/')
# def hello_world():
#     return 'Hello, World!'


