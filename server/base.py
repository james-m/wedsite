import os

from server.gogreen import coro
from server.gogreen import emulate
#emulate.init()

class BaseServer(coro.Thread):

    def __init__(self, here, *args, **kwargs):
        super(BaseServer, self).__init__(*args, **kwargs)
        self._here = here


