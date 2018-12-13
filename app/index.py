#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 ykharuk <ykharuk@Yuriis-MBP.lan>
#
# Distributed under terms of the MIT license.
from flask import Flask, Response
from flask import request
import prometheus_client
import time
from random import uniform
from prometheus_client import Counter, Histogram, Gauge, Summary, Info
from prometheus_client import multiprocess, CollectorRegistry

CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')

registry = CollectorRegistry()
multiprocess.MultiProcessCollector(registry)

STATTIC_REQUEST_COUNT = Counter(
    'static_request_count_loop', 'App Request Count',
    ['app_name', 'method', 'endpoint', 'http_status'],
)

REQUEST_COUNTER = Counter(
    'counter_number_occurances', 'other path to gaether sta',
    ['app_name', 'method', 'endpoint', 'http_status'],
    registry=registry,
)

ERROR_COUNTER = Counter(
    'counter_responce_occurances', 'other path to gaether sta',
    ['app_name', 'method', 'endpoint', 'http_status'],
    registry=registry,
)

APP_GAUGE = Gauge('gauge_current_value', 'gauge of application',
    ['app_name'],
    registry=registry,
    multiprocess_mode='min',
)

TRACEBACK_COUNTER = Counter(
    'trace_traceback_number', 'number of traceback produced by function',
    ['app_name', 'endpoint', 'func'],
    registry=registry,
)

TRACEBACK_COUNTER_FUNC1 = TRACEBACK_COUNTER.labels(app_name='poc_app', endpoint='/trace', func='tracefail')
TRACEBACK_COUNTER_FUNC2 = TRACEBACK_COUNTER.labels(app_name='poc_app', endpoint='/trace2', func='tracefail2')

REQUEST_DECORATED = Histogram('root_request_processing_seconds', 'Time spent processing request',
    ['app_name', 'endpoint'],
    registry=registry,
)

REQUEST_DECORATED_TIME = REQUEST_DECORATED.labels(app_name='poc_app', endpoint='/')
REQUEST_DECORATED_TIME2 = REQUEST_DECORATED.labels(app_name='poc_app', endpoint='/counter')
REQUEST_DECORATED_TIME3 = REQUEST_DECORATED.labels(app_name='poc_app', endpoint='/gauge')
REQUEST_DECORATED_TIME4 = REQUEST_DECORATED.labels(app_name='poc_app', endpoint='/trace')
REQUEST_DECORATED_TIME5 = REQUEST_DECORATED.labels(app_name='poc_app', endpoint='/trace2')

INFO_TYPE = Info('my_build_version', 'Description of info', registry=registry,)
INFO_TYPE.info({'version': '0.0.1', 'buildhost': 'foo@bar'})

app = Flask(__name__)

for k in range(0,9):
    STATTIC_REQUEST_COUNT.labels('poc_app', 'GET', '/',
            '200').inc()

@app.route('/')
@REQUEST_DECORATED_TIME.time()
def root():
    print(request.path)
    print(request.method)
    sleeping_value = uniform(0, 5)
    time.sleep(sleeping_value)
    return  str(sleeping_value)

@app.route('/counter')
@REQUEST_DECORATED_TIME2.time()
def wow():
    REQUEST_COUNTER.labels('poc_app', request.method, request.path,
                             '200').inc()
    return 'wow'

@app.route('/gauge')
@REQUEST_DECORATED_TIME3.time()
def gug():
    value = uniform(0,100)
    APP_GAUGE.labels('poc_app').set(value)
    return str(value)

@app.route('/trace')
@REQUEST_DECORATED_TIME4.time()
@TRACEBACK_COUNTER_FUNC1.count_exceptions()
def tracefail():
    return str(value)

@app.route('/trace2')
@REQUEST_DECORATED_TIME5.time()
@TRACEBACK_COUNTER_FUNC2.count_exceptions()
def tracefail2():
    return str(value)


@app.route('/metrics')
def metrics():
    return Response(prometheus_client.generate_latest(registry), mimetype=CONTENT_TYPE_LATEST)

@app.errorhandler(404)
def handle_500(error):
    ERROR_COUNTER.labels('poc_app', request.method, request.path,
                             '404').inc()
    return str(error), 404

@app.errorhandler(500)
def handle_500(error):
    ERROR_COUNTER.labels('poc_app', request.method, request.path,
                             '500').inc()
    return str(error), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0')
