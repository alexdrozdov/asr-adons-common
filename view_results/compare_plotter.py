#!/usr/bin/env python
# -*- coding: utf-8 -*-

import localdb
import wx
import compare_wavelet_scales_interface
import numpy
from pyplotter import PyplotPlotter


class CompareWavletScalesInst(compare_wavelet_scales_interface.CompareWaveletScales, PyplotPlotter):
    def __init__(self):
        compare_wavelet_scales_interface.CompareWaveletScales.__init__(self, None, -1, "")
        PyplotPlotter.__init__(self)
        self.Bind(wx.EVT_CLOSE, self.btnClose_handler, self)
        self.wavelets = []
    def btnClose_handler(self, event):
        self.Hide()
    def add_wavelet(self, wavelet, caption = None):
        n = len(self.wavelets)
        self.wavelets.append([wavelet, caption, 0])
        self.lbWavelets.Append(caption, n)
    def lbWavelets_handler(self, event):
        idx = self.lbWavelets.GetSelection()
        n = self.lbWavelets.GetClientData(idx)
        offset = self.wavelets[n][2]
        self.spinOffset.SetValue(offset)
    def btnRedraw_handler(self, event):
        self.plots = []
        first_wavelet = self.wavelets[0][0].get_wavelet()
        cnt = 1
        for scale in range(first_wavelet.shape[0]-1,0, -1):
            cnt += 1
            graph = self.wavelets[0][0].get_wavelet()[scale, :]
            for w in self.wavelets[1:]:
                ww = w[0].get_wavelet()
                off = w[2]
                wavelet_scale=ww[scale, :]
                graph = numpy.vstack((graph, wavelet_scale))
            PyplotPlotter.pyplot_add_plot(self, graph.T)
        PyplotPlotter.pyplot_plot(self)

    def spinOffset_handler(self, event):  # wxGlade: CompareWaveletScales.<event_handler>
        idx = self.lbWavelets.GetSelection()
        n = self.lbWavelets.GetClientData(idx)
        offset = self.spinOffset.GetValue()
        self.wavelets[idx][2] = offset


class ComparePlotter:
    def __init__(self):
        self.wavelets = []
    def add_wavelet(self, wavelet, caption=None):
        self.wavelets.append([wavelet, caption])
    def plot(self):
        cwsi = CompareWavletScalesInst()
        for w in self.wavelets:
            cwsi.add_wavelet(w[0], w[1])
        cwsi.Show()



def init_module(manager, gui):
    localdb.db.write_temporary("/db/temporary/plotters/compare-plot/class", ComparePlotter)
    localdb.db.write_temporary("/db/temporary/plotters/compare-plot/name", "compare-plot")
    localdb.db.write_temporary("/db/temporary/plotters/compare-plot/caption", u"Сравнение вейвлетов")
    return []
