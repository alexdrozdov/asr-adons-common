#!/usr/bin/env python
# -*- coding: utf-8 -*-

import localdb

class Viewer2D:
    def __init__(self):
    	pass
    def generate(self, ticket, plotter):
        try:
            plotter.add_plot(ticket.get_data().data, x=ticket.get_data().freq)
        except:
            plotter.add_plot(ticket.get_data().data)

def init_module(manager, gui):
	localdb.db.write_temporary("/db/temporary/viewers/signal/class", Viewer2D)
	localdb.db.write_temporary("/db/temporary/viewers/signal/id", "viewer-2d")
	localdb.db.write_temporary("/db/temporary/viewers/signal/caption", u"Отображение 2-D графиков")
	localdb.db.write_temporary("/db/temporary/viewers/signal/tags", ["signal", "spectrum",])
	localdb.db.write_temporary("/db/temporary/viewers/signal/data_names", [])
	localdb.db.write_temporary("/db/temporary/viewers/signal/plotter/name", "gnuplot")
	localdb.db.write_temporary("/db/temporary/viewers/signal/plotter/multiplexable", True)
	return []
