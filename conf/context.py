import os
class ConfigContext(object):
    __slots__ = ['_stack', '_levels']

    def __init__(self, *args, **kwargs):
        self._stack  = []
        self._levels = []

    def push(self, name):
        self._levels.append(name)
        self._stack.append({})

    def __setattr__(self, name, value):
        if name in ConfigContext.__slots__:
            object.__setattr__(self, name, value)
            return None
        self._stack[-1][name] = value

    def __getattr__(self, name):
        if name in ConfigContext.__slots__:
            return object.__getattribute__(self, name)
        for stk in self._stack[::-1]:
            if name in stk:
                return stk[name]
        raise AttributeError(name)

    def setdefault(self, name, value):
        try:
            getattr(self, name)
        except AttributeError, e:
            self.__setattr__(name, value)
        else:
            pass

    def clear(self):
        self._stack = []
        self._levels = []

    def info(self, name):
        data = {}
        rows = zip(self._levels, self._stack)
        for lvl, stk in rows[::-1]:
            data[lvl] = stk.get(name, '__undefined__')
        return data

    def print_info(self, name):
        info = self.info(name)
        for lvl in self._levels[::-1]:
            data = info[lvl]
            print '%s %s' % (lvl, data)

CONF_CONTEXT = None 
def ctx():
    global CONF_CONTEXT
    if CONF_CONTEXT is None:
        CONF_CONTEXT = ConfigContext()
    return CONF_CONTEXT

