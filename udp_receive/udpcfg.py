#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import udpcfg_interface
import traceback
import localdb

class UdpCfg(udpcfg_interface.UdpConfigInterface):
    def __init__(self, manager, gui):
        self.gui = gui
        self.man = manager
        udpcfg_interface.UdpConfigInterface.__init__(self, None, -1, "")
        self.Bind(wx.EVT_CLOSE, self.on_form_close, self)
        self.Bind(wx.EVT_SHOW, self.on_form_show, self)
        self.receivers = []
        self.load()
        self.redraw()
    def load(self):
        self.receivers = []
        try:
            self.receivers = localdb.db.read_value("/db/persistent/udp_receive/receivers")
        except:
            pass
    def redraw(self):
        try:
            try:
                self.gridUdpPorts.DeleteRows(0, self.gridUdpPorts.GetNumberRows(), True)
            except:
                pass
            r_cnt = 0
            for rcv_cfg in self.receivers:
                self.gridUdpPorts.AppendRows(1, True)
                self.gridUdpPorts.SetCellValue(r_cnt, 0, rcv_cfg["port"])
                self.gridUdpPorts.SetCellValue(r_cnt, 1, rcv_cfg["data_id"])
                self.gridUdpPorts.SetCellValue(r_cnt, 2, rcv_cfg["data_description"])
                self.gridUdpPorts.SetCellValue(r_cnt, 3, rcv_cfg["ticket_name"])
                r_cnt += 1
        except:
            print traceback.format_exc()
    def read_cells_from_grid(self):
        try:
            max_row = len(self.receivers)
            for r_cnt in range(max_row):
                self.receivers[r_cnt]["port"] = self.gridUdpPorts.GetCellValue(r_cnt, 0)
                self.receivers[r_cnt]["data_id"] = self.gridUdpPorts.GetCellValue(r_cnt, 1)
                self.receivers[r_cnt]["data_description"] = self.gridUdpPorts.GetCellValue(r_cnt, 2)
                self.receivers[r_cnt]["ticket_name"] = self.gridUdpPorts.GetCellValue(r_cnt, 3)
        except:
            print traceback.format_exc()
    def validate_receivers(self):
        port_list = []
        for r_cnt in range(len(self.receivers)):
            try:
                rcv_cfg = self.receivers[r_cnt]
                p = 0
                try:
                    p = int(rcv_cfg["port"], 0)
                except:
                    raise ValueError(u"Неправильно указан номер порта в строке "+str(r_cnt+1))
                if p<1 or p>65535:
                    raise ValueError(u"Номер порта в строке "+str(r_cnt+1) + u" выходит за допустимый диапазон 1...65535")
                if p in port_list:
                    raise ValueError(u"Повторяющийся номер порта в строке "+str(r_cnt+1))
                port_list.append(p)
                if len(rcv_cfg["data_id"])<1:
                    raise ValueError(u"Не задан тип данных в строке "+str(r_cnt+1))
                if len(rcv_cfg["data_id"])<1:
                    raise ValueError(u"Не задано описание данных в строке "+str(r_cnt+1))
                if len(rcv_cfg["data_id"])<1:
                    raise ValueError(u"Не задано название тикета в строке "+str(r_cnt+1))
            except ValueError as e:
                wx.MessageBox(e.message, u"Недопустимые настройки", wx.OK | wx.CENTRE, self)
                raise e
            
    def on_form_close(self, event):
        self.Hide()
    def on_form_show(self, event):
        self.load()
        self.redraw()
    def btnAddPort_on_click(self, event):
        self.receivers.append({"port":"", "data_id": "", "data_description":"", "ticket_name":""})
        self.redraw()
    def btnRemovePort_on_click(self, event):
        try:
            sel_rows = self.gridUdpPorts.GetSelectedRows()
            receivers = []
            for r_cnt in range(len(self.receivers)):
                if r_cnt in sel_rows:
                    continue
                receivers.append(self.receivers[r_cnt])
            self.receivers = receivers
            self.redraw()
        except:
            print traceback.format_exc()
    def btnSave_on_click(self, event):
        try:
            self.read_cells_from_grid()
            self.validate_receivers()
            localdb.db.write_persistent("/db/persistent/udp_receive/receivers", self.receivers)
            self.Hide()
        except:
            print traceback.format_exc()
    def btnCancel_on_click(self, event):
        self.Hide()
    def gridUdpPorts_on_cell_changed(self, event):
        self.read_cells_from_grid()

def init_module(manager, gui):
    frame = UdpCfg(manager, gui)
    gui.register_window(frame, u"Параметры приема сообщений UDP", "wnd_udp_cfg")
