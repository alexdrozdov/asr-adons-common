 #!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
import localdb

class SndDaemon:
    def __init__(self, manager):
        pass

class RcvDaemon:
    def __init__(self, manager):
        pass


def init_module(manager, gui):
    s = SndDaemon(manager)
    r = RcvDaemon(manager)
    return [r, s]
