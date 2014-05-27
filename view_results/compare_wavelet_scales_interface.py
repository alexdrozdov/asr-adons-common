#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# generated by wxGlade 0.6.6 on Wed Mar 12 22:32:32 2014
#

import wx

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class CompareWaveletScales(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: CompareWaveletScales.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.lbWavelets = wx.ListBox(self, wx.ID_ANY, choices=[])
        self.spinOffset = wx.SpinCtrl(self, wx.ID_ANY, "", min=0, max=100)
        self.btnRedraw = wx.Button(self, wx.ID_ANY, u"Перестроить")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_LISTBOX, self.lbWavelets_handler, self.lbWavelets)
        self.Bind(wx.EVT_SPINCTRL, self.spinOffset_handler, self.spinOffset)
        self.Bind(wx.EVT_BUTTON, self.btnRedraw_handler, self.btnRedraw)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: CompareWaveletScales.__set_properties
        self.SetTitle(u"Сравнение вейвлетов по масштабам")
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: CompareWaveletScales.__do_layout
        sizer_1 = wx.FlexGridSizer(2, 1, 0, 0)
        sizer_2 = wx.GridSizer(1, 2, 0, 0)
        sizer_1.Add(self.lbWavelets, 0, wx.EXPAND, 0)
        sizer_2.Add(self.spinOffset, 0, wx.EXPAND, 0)
        sizer_2.Add(self.btnRedraw, 0, wx.EXPAND, 0)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        sizer_1.AddGrowableRow(0)
        sizer_1.AddGrowableCol(0)
        self.Layout()
        # end wxGlade

    def lbWavelets_handler(self, event):  # wxGlade: CompareWaveletScales.<event_handler>
        print "Event handler 'lbWavelets_handler' not implemented!"
        event.Skip()

    def spinOffset_handler(self, event):  # wxGlade: CompareWaveletScales.<event_handler>
        print "Event handler 'spinOffset_handler' not implemented!"
        event.Skip()

    def btnRedraw_handler(self, event):  # wxGlade: CompareWaveletScales.<event_handler>
        print "Event handler 'btnRedraw_handler' not implemented!"
        event.Skip()

# end of class CompareWaveletScales
if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    compare_wavelet_scales = CompareWaveletScales(None, wx.ID_ANY, "")
    app.SetTopWindow(compare_wavelet_scales)
    compare_wavelet_scales.Show()
    app.MainLoop()