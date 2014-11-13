#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

class IdleExit(object):
    def __init__(self, manager):
        self.man = manager
        if '--exit-on-idle' in sys.argv:
            self.man.register_handler("core::idle", self.idle_handler)
    def idle_handler(self, ticket):
        print "Exiting on idle"
        sys.exit(0)
def init_module(manager, gui):
    r = IdleExit(manager)
    return [r,]


