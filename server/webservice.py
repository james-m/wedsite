import conf; cfg = conf.get_context()

import server.gogreen.corohttpd
import server.gogreen.wsgi

import www.core

import logging

class InvalidWsgiApp(Exception):
    pass

def testapp(env, start_response):
    if env['PATH_INFO'] == '/':
        start_response('200 OK', [('Content-Type', 'text/html')])
        return ["<b>hello world</b>"]
    else:
        start_response('404 Not Found', [('Content-Type', 'text/html')])
        return ['<h1>Not Found</h1>']

VALID_WSGI_APPS = {
    'test' : testapp,
    'webcore' : www.core.app,
    }

class NodeWSGIAppHandler(server.gogreen.wsgi.WSGIAppHandler):

    def __init__(self, app, *args, **kwargs):
        super(NodeWSGIAppHandler, self).__init__(app, *args, **kwargs)
        self._dbpool = kwargs.get('dbpool')

    def extend_environ(self, environ, *args, **kwargs):
        super(NodeWSGIAppHandler, self).extend_environ(environ, *args, **kwargs)
        environ[cfg.WSGI_ENV_DB_POOL_NAME] = self._dbpool

def make_wsgi(appname, host, port, access_log_name, dbpool=None):
    addr = (host, port)
    app = VALID_WSGI_APPS.get(appname)
    if app is None:
        raise InvalidWsgiApp(appname)
    
    wsgisrv = server.gogreen.corohttpd.HttpServer(
        args=(addr, access_log_name),
        )
    wsgisrv.push_handler(NodeWSGIAppHandler(app, dbpool=dbpool))
    return wsgisrv
