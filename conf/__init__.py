import os
import sys
import context

def get_env_config():
    env = 'dev' # the default
    env = os.environ.get('ENV_NAME', env)
    env = env.lower()
    return 'conf.%s' % env

def get_context():
    return context.ctx()

CONF_DIR = os.path.split(os.path.abspath(__file__))[0]
MODULES = [
    # module name, required?
    ('conf.local_pre', False), 
    ('conf.all',       True),
    (get_env_config(), True),
    ('conf.local',     False),
    ]
LOADED = False
def load(_reload=False):
    global LOADED
    if LOADED and not _reload:
        return None
    ctx = get_context()
    ctx.clear()
    for name, opt in MODULES:
        try:
            if name in sys.modules:
                reload(sys.modules[name])
            else:
                __import__(name)
        except ImportError, e:
            if opt:
                raise
    LOADED = True

load()

# for backwards compat
#
def get(name, default = None):
    cfg = get_context()
    try:
        return cfg.__getattr__(name)
    except AttributeError, e:
        return default

