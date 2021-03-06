#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Fri Jan 31 16:49:36 2014

import wx

# begin wxGlade: extracode
# end wxGlade



class ViewHandlers(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: ViewHandlers.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.tree_handlers = wx.TreeCtrl(self, -1, style=wx.TR_HAS_BUTTONS|wx.TR_NO_LINES|wx.TR_FULL_ROW_HIGHLIGHT|wx.TR_DEFAULT_STYLE|wx.SUNKEN_BORDER)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: ViewHandlers.__set_properties
        self.SetTitle(u"Контроль обработчиков сообщений")
        self.SetSize((700, 500))
        self.tree_handlers.SetMinSize((405, 136))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: ViewHandlers.__do_layout
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(self.tree_handlers, 1, wx.EXPAND|wx.FIXED_MINSIZE, 0)
        self.SetSizer(sizer_2)
        self.Layout()
        # end wxGlade

# end of class ViewHandlers


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    fmg_frame = (None, -1, "")
    app.SetTopWindow(fmg_frame)
    fmg_frame.Show()
    app.MainLoop()
