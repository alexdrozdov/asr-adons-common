#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Thu Sep 11 04:53:01 2014

import wx
import wx.grid

# begin wxGlade: extracode
# end wxGlade



class SendMessageInterface(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: SendMessageInterface.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.nbDirection = wx.Notebook(self, -1, style=0)
        self.nbpReceive = wx.Panel(self.nbDirection, -1)
        self.nbpSend = wx.Panel(self.nbDirection, -1)
        self.sizer_3_staticbox = wx.StaticBox(self.nbpSend, -1, u"Отправляемые сообщения")
        self.sizer_2_staticbox = wx.StaticBox(self.nbpSend, -1, u"Удаленные машины")
        self.gridHosts = wx.grid.Grid(self.nbpSend, -1, size=(1, 1))
        self.btnAddHost = wx.Button(self.nbpSend, -1, u"Добавить")
        self.btnRemoveHost = wx.Button(self.nbpSend, -1, u"Удалить")
        self.btnDisableHost = wx.Button(self.nbpSend, -1, u"Отключить")
        self.btnScanHosts = wx.Button(self.nbpSend, -1, u"Сканировать сеть")
        self.comboSendMessages = wx.ComboBox(self.nbpSend, -1, choices=[], style=wx.CB_DROPDOWN|wx.CB_DROPDOWN|wx.CB_READONLY)
        self.btnAddSendMessage = wx.Button(self.nbpSend, -1, u"Добавить")
        self.listSendMessages = wx.ListCtrl(self.nbpSend, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.btnRemoveSendMessage = wx.Button(self.nbpSend, -1, u"Удалить")
        self.gridRcvPorts = wx.grid.Grid(self.nbpReceive, -1, size=(1, 1))
        self.btnAddRcvPort = wx.Button(self.nbpReceive, -1, u"Добавить")
        self.btnRemoveRcvPort = wx.Button(self.nbpReceive, -1, u"Удалить")
        self.btnDisableRcvPort = wx.Button(self.nbpReceive, -1, u"Отключить")
        self.btnSaveToBase = wx.Button(self, -1, u"Сохранить в базу")
        self.btnCancel = wx.Button(self, -1, u"Отменить изменения")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.grid.EVT_GRID_CMD_SELECT_CELL, self.gridHosts_on_select, self.gridHosts)
        self.Bind(wx.EVT_BUTTON, self.btnAddHost_on_click, self.btnAddHost)
        self.Bind(wx.EVT_BUTTON, self.btnRemoveHost_on_click, self.btnRemoveHost)
        self.Bind(wx.EVT_BUTTON, self.btnDisableHost_on_click, self.btnDisableHost)
        self.Bind(wx.EVT_BUTTON, self.btnScanHosts_on_click, self.btnScanHosts)
        self.Bind(wx.EVT_COMBOBOX, self.comboSendMessages_on_select, self.comboSendMessages)
        self.Bind(wx.EVT_BUTTON, self.btnAddSendMessage_on_click, self.btnAddSendMessage)
        self.Bind(wx.EVT_BUTTON, self.btnRemoveSendMessage_on_click, self.btnRemoveSendMessage)
        self.Bind(wx.grid.EVT_GRID_CMD_SELECT_CELL, self.gridRcvPorts_on_select, self.gridRcvPorts)
        self.Bind(wx.EVT_BUTTON, self.btnAddRcvPort_on_click, self.btnAddRcvPort)
        self.Bind(wx.EVT_BUTTON, self.btnRemoveRcvPort_on_click, self.btnRemoveRcvPort)
        self.Bind(wx.EVT_BUTTON, self.btnDisableRcvPort_on_click, self.btnDisableRcvPort)
        self.Bind(wx.EVT_BUTTON, self.btnSaveToBase_on_click, self.btnSaveToBase)
        self.Bind(wx.EVT_BUTTON, self.btnCancel_on_click, self.btnCancel)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: SendMessageInterface.__set_properties
        self.SetTitle(u"Обмен сообщениями")
        self.SetSize((700, 600))
        self.gridHosts.CreateGrid(0, 3)
        self.gridHosts.SetSelectionMode(wx.grid.Grid.wxGridSelectRows)
        self.gridHosts.SetColLabelValue(0, u"Канал")
        self.gridHosts.SetColLabelValue(1, u"Адрес")
        self.gridHosts.SetColLabelValue(2, u"Параметры канала")
        self.gridRcvPorts.CreateGrid(0, 2)
        self.gridRcvPorts.SetColLabelValue(0, u"Канал")
        self.gridRcvPorts.SetColLabelValue(1, u"Параметры канала")
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: SendMessageInterface.__do_layout
        sizer_1 = wx.FlexGridSizer(2, 1, 0, 0)
        grid_sizer_9 = wx.GridSizer(1, 2, 0, 0)
        grid_sizer_6 = wx.FlexGridSizer(2, 1, 0, 0)
        grid_sizer_7 = wx.GridSizer(1, 3, 0, 0)
        grid_sizer_1 = wx.FlexGridSizer(2, 1, 0, 0)
        sizer_3 = wx.StaticBoxSizer(self.sizer_3_staticbox, wx.VERTICAL)
        grid_sizer_3 = wx.FlexGridSizer(3, 1, 0, 0)
        grid_sizer_4 = wx.FlexGridSizer(1, 2, 0, 0)
        sizer_2 = wx.StaticBoxSizer(self.sizer_2_staticbox, wx.HORIZONTAL)
        grid_sizer_2 = wx.FlexGridSizer(2, 1, 0, 0)
        grid_sizer_5 = wx.GridSizer(1, 4, 0, 0)
        grid_sizer_2.Add(self.gridHosts, 1, wx.EXPAND, 0)
        grid_sizer_5.Add(self.btnAddHost, 0, wx.EXPAND, 0)
        grid_sizer_5.Add(self.btnRemoveHost, 0, wx.EXPAND, 0)
        grid_sizer_5.Add(self.btnDisableHost, 0, wx.EXPAND, 0)
        grid_sizer_5.Add(self.btnScanHosts, 0, wx.EXPAND, 0)
        grid_sizer_2.Add(grid_sizer_5, 1, wx.EXPAND, 0)
        grid_sizer_2.AddGrowableRow(0)
        grid_sizer_2.AddGrowableCol(0)
        sizer_2.Add(grid_sizer_2, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(sizer_2, 1, wx.EXPAND, 2)
        grid_sizer_4.Add(self.comboSendMessages, 0, wx.EXPAND, 0)
        grid_sizer_4.Add(self.btnAddSendMessage, 0, 0, 0)
        grid_sizer_4.AddGrowableCol(0)
        grid_sizer_3.Add(grid_sizer_4, 1, wx.EXPAND, 0)
        grid_sizer_3.Add(self.listSendMessages, 1, wx.EXPAND, 0)
        grid_sizer_3.Add(self.btnRemoveSendMessage, 0, 0, 0)
        grid_sizer_3.AddGrowableRow(1)
        grid_sizer_3.AddGrowableCol(0)
        sizer_3.Add(grid_sizer_3, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(sizer_3, 1, wx.EXPAND, 0)
        self.nbpSend.SetSizer(grid_sizer_1)
        grid_sizer_1.AddGrowableRow(0)
        grid_sizer_1.AddGrowableRow(1)
        grid_sizer_1.AddGrowableCol(0)
        grid_sizer_6.Add(self.gridRcvPorts, 1, wx.EXPAND, 0)
        grid_sizer_7.Add(self.btnAddRcvPort, 0, 0, 0)
        grid_sizer_7.Add(self.btnRemoveRcvPort, 0, 0, 0)
        grid_sizer_7.Add(self.btnDisableRcvPort, 0, 0, 0)
        grid_sizer_6.Add(grid_sizer_7, 1, 0, 0)
        self.nbpReceive.SetSizer(grid_sizer_6)
        grid_sizer_6.AddGrowableRow(0)
        grid_sizer_6.AddGrowableCol(0)
        self.nbDirection.AddPage(self.nbpSend, u"Отправка сообщений")
        self.nbDirection.AddPage(self.nbpReceive, u"Прием сообщений")
        sizer_1.Add(self.nbDirection, 1, wx.EXPAND, 0)
        grid_sizer_9.Add(self.btnSaveToBase, 0, 0, 0)
        grid_sizer_9.Add(self.btnCancel, 0, 0, 0)
        sizer_1.Add(grid_sizer_9, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.AddGrowableRow(0)
        sizer_1.AddGrowableCol(0)
        self.Layout()
        # end wxGlade

    def gridHosts_on_select(self, event): # wxGlade: SendMessageInterface.<event_handler>
        print "Event handler `gridHosts_on_select' not implemented!"
        event.Skip()

    def btnAddHost_on_click(self, event): # wxGlade: SendMessageInterface.<event_handler>
        print "Event handler `btnAddHost_on_click' not implemented!"
        event.Skip()

    def btnRemoveHost_on_click(self, event): # wxGlade: SendMessageInterface.<event_handler>
        print "Event handler `btnRemoveHost_on_click' not implemented!"
        event.Skip()

    def btnDisableHost_on_click(self, event): # wxGlade: SendMessageInterface.<event_handler>
        print "Event handler `btnDisableHost_on_click' not implemented!"
        event.Skip()

    def btnScanHosts_on_click(self, event): # wxGlade: SendMessageInterface.<event_handler>
        print "Event handler `btnScanHosts_on_click' not implemented!"
        event.Skip()

    def comboSendMessages_on_select(self, event): # wxGlade: SendMessageInterface.<event_handler>
        print "Event handler `comboSendMessages_on_select' not implemented!"
        event.Skip()

    def btnAddSendMessage_on_click(self, event): # wxGlade: SendMessageInterface.<event_handler>
        print "Event handler `btnAddSendMessage_on_click' not implemented!"
        event.Skip()

    def btnRemoveSendMessage_on_click(self, event): # wxGlade: SendMessageInterface.<event_handler>
        print "Event handler `btnRemoveSendMessage_on_click' not implemented!"
        event.Skip()

    def btnAddRcvPort_on_click(self, event): # wxGlade: SendMessageInterface.<event_handler>
        print "Event handler `btnAddRcvPort_on_click' not implemented!"
        event.Skip()

    def btnRemoveRcvPort_on_click(self, event): # wxGlade: SendMessageInterface.<event_handler>
        print "Event handler `btnRemoveRcvPort_on_click' not implemented!"
        event.Skip()

    def btnDisableRcvPort_on_click(self, event): # wxGlade: SendMessageInterface.<event_handler>
        print "Event handler `btnDisableRcvPort_on_click' not implemented!"
        event.Skip()

    def btnSaveToBase_on_click(self, event): # wxGlade: SendMessageInterface.<event_handler>
        print "Event handler `btnSaveToBase_on_click' not implemented!"
        event.Skip()

    def btnCancel_on_click(self, event): # wxGlade: SendMessageInterface.<event_handler>
        print "Event handler `btnCancel_on_click' not implemented!"
        event.Skip()

    def gridRcvPorts_on_select(self, event): # wxGlade: SendMessageInterface.<event_handler>
        print "Event handler `gridRcvPorts_on_select' not implemented"
        event.Skip()

# end of class SendMessageInterface


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = SendMessageInterface(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
