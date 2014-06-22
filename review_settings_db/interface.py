#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.4 on Thu Apr 17 12:42:12 2014

import wx

# begin wxGlade: extracode
# end wxGlade


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.tree_db = wx.TreeCtrl(self, -1, style=wx.TR_HAS_BUTTONS | wx.TR_NO_LINES | wx.TR_DEFAULT_STYLE | wx.SUNKEN_BORDER)
        self.btn_refresh = wx.Button(self, -1, u"Обновить")
        self.sizer_3_staticbox = wx.StaticBox(self, -1, "Tree_db")
        self.label_1 = wx.StaticText(self, -1, u"Значение:")
        self.text_ctrl_1 = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE)
        self.btn_apply = wx.Button(self, -1, u"Применить")
        self.sizer_4_staticbox = wx.StaticBox(self, -1, "Edit Node")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.On_treeitem_dblclk, self.tree_db)
        self.Bind(wx.EVT_BUTTON, self.On_refresh_clk, self.btn_refresh)
        self.Bind(wx.EVT_BUTTON, self.On_apply_clk, self.btn_apply)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("Display_localdb")
        self.SetSize((900, 500))
        self.tree_db.SetMinSize((600, 395))
        self.text_ctrl_1.SetMinSize((250, 60))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_4_staticbox.Lower()
        sizer_4 = wx.StaticBoxSizer(self.sizer_4_staticbox, wx.VERTICAL)
        self.sizer_3_staticbox.Lower()
        sizer_3 = wx.StaticBoxSizer(self.sizer_3_staticbox, wx.VERTICAL)
        sizer_3.Add(self.tree_db, 1, wx.EXPAND, 0)
        sizer_3.Add(self.btn_refresh, 0, wx.TOP | wx.ALIGN_CENTER_HORIZONTAL, 20)
        sizer_2.Add(sizer_3, 0, wx.EXPAND, 0)
        sizer_4.Add(self.label_1, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_4.Add(self.text_ctrl_1, 0, wx.TOP, 5)
        sizer_4.Add(self.btn_apply, 0, wx.TOP | wx.ALIGN_CENTER_HORIZONTAL, 10)
        sizer_2.Add(sizer_4, 0, wx.LEFT | wx.EXPAND, 20)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

    def On_refresh_clk(self, event):  # wxGlade: MyFrame.<event_handler>
        print "Event handler `On_refresh_clk' not implemented!"
        event.Skip()

    def On_apply_clk(self, event):  # wxGlade: MyFrame.<event_handler>
        print "Event handler `On_apply_clk' not implemented!"
        event.Skip()

    def On_treeitem_dblclk(self, event):  # wxGlade: MyFrame.<event_handler>
        print "Event handler `On_treeitem_dblclk' not implemented"
        event.Skip()

# end of class MyFrame
if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = MyFrame(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()