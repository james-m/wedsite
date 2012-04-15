# -*- Mode: Python; tab-width: 4 -*-
'''common/serverlock.py

Common util module for server process locking. We use sockets because
only a single process can bind to one port at a time (lock them) and when 
the process goes away so does the lock. 

The idea is to have a pool of ports on any given host that we try in turn
when doing process initialization. If we can't bind to a given port
we move on to the next in our service list. If we run out then we stop.

NOTE that these files expect a list of dicts with the keys 'host' and
'lockport' which are the hostname:port combination to bind/lock too.
'''
import socket

def servers_by_hostname(confs):
    '''given a server filter out the name ones for this host name'''
    name = socket.gethostname()
    result = []
    for c in confs:
        if c.get('host', 'localhost') in [name, 'localhost']:
            result.append(c)
    return result

def _bindlock(srv):
    srv = dict(srv)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((srv.get('host', ''), srv['lockport']))
    s.listen(1024)
    return s

def lock_server(confs):
    for c in servers_by_hostname(confs):
        try:
            s = _bindlock(c)
            c['lock'] = s
            return c
        except socket.error:
            pass
    return None
