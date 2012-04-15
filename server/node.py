#!/usr/bin/python
#
import time
import sys
import os
import signal 

import conf
cfg = conf.get_context()
import server.base
import server.start
import server.webservice

from server.gogreen import coro
from server.gogreen import backdoor

from db import dbpool

class InvalidService(Exception):
    pass

class ServiceNode(server.base.BaseServer):

    def __init__(self, *args, **kwargs):
        super(ServiceNode, self).__init__(*args, **kwargs)
        self._defns = kwargs.get('defns', [])
        self._thrds = {}

        self._dbpool = None

        self._exit = False
        self._cond = server.gogreen.coro.coroutine_cond()

    def run(self):
        self.info('Starting ServiceNode with %d defns' % len(self._defns)) 
        self.info('PID %s' % os.getpid())
       
        # start the services defined in defns
        # 
        self.services_start()
        while not self._exit:
            self._cond.wait()

        # shutdown each of the services in turn
        #
        self.info('Stopping ServiceNode') 
        self.services_stop()

    def wake(self):
        self._cond.wake_all()

    def shutdown(self):
        self._exit = True
        self.wake()

    def services_start(self):
        # always need a backdoor
        #
        back = backdoor.BackDoorServer(
            args=(self._here['backport'], 'localhost')
            )
        back.start()
        self._thrds['backdoor'] = back
        # and a dbpool
        #
        self._dbpool = dbpool.DBPool(
            args = (), 
            kwargs = {}, 
            size = cfg.DB_POOL_SIZE, 
            )
        self._dbpool.timeout(cfg.DB_POOL_TIMEOUT)

        for defn in self._defns:
            stype = defn.pop('type')
            name, thrd = self.make_service(stype, defn)
            thrd.start()
            self._thrds[name] = thrd

    def services_stop(self):
        for name, thrd in self._thrds.items():
            self.info('shutting down %s' % name)
            thrd.shutdown()
        # wait for these guys to finish
        #
        zombies = self.child_wait(
            cfg.SERVICE_SHUTDOWN_TIMEOUT, 
            set(self._thrds.values()))
        if zombies:
            self.warn('timeout waiting for services to stop. [%s]' % zombies)
            for child in self.chil_list():
                self.warn('  zombie: %s' % child)

        # stop the dbpool
        #
        stopped = self._dbpool.off(
            timeout = cfg.SERVICE_DB_POOL_TIMEOUT, 
            )
        if not stopped:
            self.warn('timeout waiting for dbpool to offline.')

    def make_service(self, stype, defn):
        if stype == 'wsgi':
            appname = defn['appname']
            overwrite = defn.get('overwrite', {})

            host = overwrite.get('host', self._here.get('host', ''))
            port = defn['httpport']
            access_log = defn['access_log']
            self.info('Making web service: %s' % appname)
            return 'wsgi-%s' % appname, server.webservice.make_wsgi(
                appname, 
                host, 
                port, 
                access_log,
                dbpool = self._dbpool,
                )

        raise InvalidService(stype)

def init_node(log, logdir, args, here, **kw):
    defns = map(dict, here.get('defns', []))
    node = ServiceNode(
        here, 
        log = log, 
        defns = defns,
        )
    node.set_log_level(20)
    node.start()
    def shutdown_handler(signum, frame):
        node.shutdown()
    signal.signal(signal.SIGUSR2, shutdown_handler)

    try:
        coro.event_loop()
    except KeyboardInterrupt, e:
        pass

DESCR = '''
Initialize a ServiceNode for this host. See base.ServiceNode for more infomation. 
'''

if __name__ == '__main__':
    parser = server.start.generic_parser(DESCR)
    args = parser.parse_args()
    services = cfg.SERVICE_NODES
    v = server.start.main(
        init_node, 
        args, 
        services, 
        logname = 'node',
        monkey_log = True)  
    sys.exit(v)
