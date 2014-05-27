#!/usr/bin/env python
# -*- coding: utf-8 -*-

import localdb

class ViewerWavelet:
    def __init__(self):
    	pass
    def generate(self, ticket, plotter):
    	plotter.add_image(ticket.get_data().get_wavelet())


def init_module(manager, gui):
	localdb.db.write_temporary("/db/temporary/viewers/wavelet/class", ViewerWavelet)
	localdb.db.write_temporary("/db/temporary/viewers/wavelet/id", "wavelet")
	localdb.db.write_temporary("/db/temporary/viewers/wavelet/caption", u"Отображение вейвлетов")
	localdb.db.write_temporary("/db/temporary/viewers/wavelet/tags", ["wavelet",])
	localdb.db.write_temporary("/db/temporary/viewers/wavelet/data_names", [])
	localdb.db.write_temporary("/db/temporary/viewers/wavelet/plotter/name", "plot")
	localdb.db.write_temporary("/db/temporary/viewers/wavelet/plotter/multiplexable", True)
	return []
