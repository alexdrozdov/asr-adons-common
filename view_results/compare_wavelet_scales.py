#!/usr/bin/env python
# -*- coding: utf-8 -*-

import localdb
import wx
import compare_wavelet_scales_interface


class ViewerCompareWaveletScales:
    def __init__(self):
    	pass
    def supported_tags(self):
        return ["signal", "spectrum",]
    def get_viewer_id_name(self):
        return u"viewer-2d"
    def get_viewer_caption(self):
        return u"Отображение 2-D графиков"
    def generate(self, ticket, plotter):
        plotter.add_wavelet(ticket.get_data(), caption=ticket.description)


def init_module(manager, gui):
	localdb.db.write_temporary("/db/temporary/viewers/compare-wavelet-scales/class", ViewerCompareWaveletScales)
	localdb.db.write_temporary("/db/temporary/viewers/compare-wavelet-scales/id", "compare-wavelet-scales")
	localdb.db.write_temporary("/db/temporary/viewers/compare-wavelet-scales/caption", u"Сравнение вейвлетов по масштабам")
	localdb.db.write_temporary("/db/temporary/viewers/compare-wavelet-scales/tags", ["wavelet",])
	localdb.db.write_temporary("/db/temporary/viewers/compare-wavelet-scales/data_names", [])
	localdb.db.write_temporary("/db/temporary/viewers/compare-wavelet-scales/plotter/name", "compare-plot")
	localdb.db.write_temporary("/db/temporary/viewers/compare-wavelet-scales/plotter/multiplexable", True)
	return []
