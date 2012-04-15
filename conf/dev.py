#######
# CONFIG SETUP do not change or configs will break
#    this goes a the top of any config file. it adds stuff to the global config
#    context. 
import context
cfg = context.ctx()
cfg.push(__name__)
# END CONFIG SETUP
#######

cfg.setdefault('user', 'expedite_dev')
cfg.setdefault('host', 'localhost') 

# BASE SERVICE CONFS
#

cfg.SERVICE_NODES = [
    {
        'defns': [
            {
                'type': 'wsgi',
                'appname': 'webcore',
                'httpport': 6000,
                'access_log': 'expedite_access',
                'overwrite': { 'host': '0.0.0.0'},
            },
        ], 
        'host': cfg.host,
        'lockport': 6101,
        'backport': 6102,
        'logdir': 'log0', 
        'pidfile': 'serv.pid',
    },
]

# WEBSERVICE
#
cfg.WEB_SRV_DEBUG = True
cfg.WEB_SRV_AUTORELOAD = True

