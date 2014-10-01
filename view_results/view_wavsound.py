#!/usr/bin/env python
# -*- coding: utf-8 -*-

import localdb

class ViewerWav:
    def __init__(self):
    	pass
    def generate(self, ticket, plotter):
        plotter.add_plot(ticket.get_data().get_sound())

def init_module(manager, gui):
	localdb.db.write_temporary("/db/temporary/viewers/wavsound/class", ViewerWav)
	localdb.db.write_temporary("/db/temporary/viewers/wavsound/id", "wavsound")
	localdb.db.write_temporary("/db/temporary/viewers/wavsound/caption", u"Отображение Wav-файлов")
	localdb.db.write_temporary("/db/temporary/viewers/wavsound/tags", ["wav-sound",])
	localdb.db.write_temporary("/db/temporary/viewers/wavsound/data_names", [])
	localdb.db.write_temporary("/db/temporary/viewers/wavsound/plotter/name", "plot")
	localdb.db.write_temporary("/db/temporary/viewers/wavsound/plotter/multiplexable", True)
	return []
