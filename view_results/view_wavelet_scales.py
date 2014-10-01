#!/usr/bin/env python
# -*- coding: utf-8 -*-

import localdb

class ViewerWaveletScales:
    def __init__(self):
    	pass
    def supported_tags(self):
        return ["signal", "spectrum",]
    def get_viewer_id_name(self):
        return u"viewer-2d"
    def get_viewer_caption(self):
        return u"Отображение 2-D графиков"
    def generate(self, ticket, plotter):
        wavelet = ticket.get_data().get_wavelet()
    	plotter.add_image(wavelet)
        print wavelet.shape
        for scale in range(wavelet.shape[0]-1,0, -1):
            plotter.add_plot(wavelet[scale, :], caption='Scale={0}'.format(scale-1))


def init_module(manager, gui):
	localdb.db.write_temporary("/db/temporary/viewers/wavelet-scales/class", ViewerWaveletScales)
	localdb.db.write_temporary("/db/temporary/viewers/wavelet-scales/id", "wavelet-scales")
	localdb.db.write_temporary("/db/temporary/viewers/wavelet-scales/caption", u"Отображение вейвлетов по масштабам")
	localdb.db.write_temporary("/db/temporary/viewers/wavelet-scales/tags", ["wavelet",])
	localdb.db.write_temporary("/db/temporary/viewers/wavelet-scales/data_names", [])
	localdb.db.write_temporary("/db/temporary/viewers/wavelet-scales/plotter/name", "plot")
	localdb.db.write_temporary("/db/temporary/viewers/wavelet-scales/plotter/multiplexable", True)
	return []
