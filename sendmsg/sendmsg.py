 #!/usr/bin/env python
# -*- coding: utf-8 -*-


import wx, sendmsg_interface
import traceback
import localdb
import copy

class RemoteHostConnectionInfo:
    def __init__(self, params):
        self.params = params
        self.enabled = True
        self.messages_to_send = []
    def get_channel(self):
        pass
    def get_address(self):
        pass
    def get_channel_params(self):
        pass
    def set_address(self, address):
        pass
    def set_channel_params(self, param_string):
        pass
    def set_enabled(self, en):
        self.enabled = en
    def get_enabled(self):
        return self.enabled
    
class UdpConnectionInfo(RemoteHostConnectionInfo):
    def __init__(self, params=None):
        if None==params:
            params={"ip":"255.255.255.255", "port":1000}
        RemoteHostConnectionInfo.__init__(self, params)
    def get_channel(self):
        return "udp"
    def get_address(self):
        return self.params["ip"]
    def get_channel_params(self):
        return str(self.params["port"])
    def set_address(self, address):
        self.params["ip"] = address
    def set_channel_params(self, param_string):
        self.params["port"] = int(param_string)
        if self.params["port"]<1 or self.params["port"]>65535:
            raise ValueError(u"Номер udp-порта выходит за допустимые границы 1...65535")

class SendMsgInterface(sendmsg_interface.SendMessageInterface):
    def __init__(self, manager):
        sendmsg_interface.SendMessageInterface.__init__(self, None, -1, "")
        self.Bind(wx.EVT_SHOW, self.on_show, self)
        self.Bind(wx.EVT_CLOSE, self.on_form_close, self)
        self.Bind(wx.grid.EVT_GRID_CMD_CELL_CHANGE, self.gridHosts_on_cell_changed, self.gridHosts)
        self.man = manager
        self.remote_hosts = []

    def on_form_close(self, event):
        self._load_from_localdb()
        self.Hide()
    def _fill_msglist_combo(self, combo):
        for k in self.man.handlers.keys():
            combo.Append(str(self.man.dis.get_name_by_id(k)))
    def on_show(self, evt):
        if evt.GetShow():
            self._load_from_localdb()
            self._fill_msglist_combo(self.comboSendMessages)
            self._fill_msglist_combo(self.comboRcvMessages)
            self._fill_hosts_list()
                        
    def _fill_hosts_list(self):
        try:
            try:
                self.gridHosts.DeleteRows(0, self.gridHosts.GetNumberRows(), True)
            except:
                pass
            r_cnt = 0
            for h in self.remote_hosts:
                self.gridHosts.AppendRows(1, True)
                self.gridHosts.SetCellValue(r_cnt, 0, h.get_channel())
                self.gridHosts.SetCellValue(r_cnt, 1, h.get_address())
                self.gridHosts.SetCellValue(r_cnt, 2, h.get_channel_params())
                r_cnt += 1
        except:
            print traceback.format_exc()
            
    def _fill_host_messages_list(self, host):
        #print dir(self.listSendMessages)
        self.listSendMessages.ClearAll()
        self.listSendMessages.InsertColumn(0, u"Типы сообщений", width=300)
        for m in host.messages_to_send:
            self.listSendMessages.Append([m])
    
    def btLoadMsgConfig_on_click(self, event): # wxGlade: SendMessageInterface.<event_handler>
        print "Event handler `btLoadMsgConfig_on_click' not implemented!"
        event.Skip()

    def btnExportMsgConfig_on_click(self, event): # wxGlade: SendMessageInterface.<event_handler>
        print "Event handler `btnExportMsgConfig_on_click' not implemented!"
        event.Skip()

    def comboMsgConfigs_on_select(self, event): # wxGlade: SendMessageInterface.<event_handler>
        print "Event handler `comboMsgConfigs_on_select' not implemented!"
        event.Skip()

    def btnEditConfig_on_click(self, event): # wxGlade: SendMessageInterface.<event_handler>
        print "Event handler `btnEditConfig_on_click' not implemented!"
        event.Skip()

    def gridHosts_on_select(self, event): # wxGlade: SendMessageInterface.<event_handler>
        try:
            r = event.GetRow()
            h = self.remote_hosts[r]
            self._fill_host_messages_list(h)
        except:
            print traceback.format_exc()

    def btnAddHost_on_click(self, event): # wxGlade: SendMessageInterface.<event_handler>
        self.remote_hosts.append(UdpConnectionInfo())
        self._fill_hosts_list()

    def btnRemoveHost_on_click(self, event): # wxGlade: SendMessageInterface.<event_handler>
        try:
            sel_rows = self.gridHosts.GetSelectedRows()
            rh = []
            for r_cnt in range(len(self.remote_hosts)):
                if r_cnt in sel_rows:
                    continue
                rh.append(self.remote_hosts[r_cnt])
            self.remote_hosts = rh
            self._fill_hosts_list()
        except:
            print traceback.format_exc()

    def btnDisableHost_on_click(self, event): # wxGlade: SendMessageInterface.<event_handler>
        print "Event handler `btnDisableHost_on_click' not implemented!"
        event.Skip()

    def btnScanHosts_on_click(self, event): # wxGlade: SendMessageInterface.<event_handler>
        print "Event handler `btnScanHosts_on_click' not implemented!"
        event.Skip()
        
    def gridHosts_on_cell_changed(self, event): # wxGlade: UdpConfigInterface.<event_handler>
        try:
            r = event.GetRow()
            h = self.remote_hosts[r]
            h.set_address(self.gridHosts.GetCellValue(r, 1))
            h.set_channel_params(self.gridHosts.GetCellValue(r, 2))
        except:
            print traceback.format_exc()

    def comboSendMessages_on_select(self, event): # wxGlade: SendMessageInterface.<event_handler>
        pass

    def get_selected_host(self):
        sel_rows = self.gridHosts.GetSelectedRows()
        if len(sel_rows) != 1:
            return None
        r = sel_rows[0]
        return self.remote_hosts[r]
    
    def btnAddSendMessage_on_click(self, event): # wxGlade: SendMessageInterface.<event_handler>
        try:
            if self.comboSendMessages.GetSelection() < 0:
                return
            h = self.get_selected_host()
            if None == h:
                return
            msg_name = self.comboSendMessages.GetValue()
            if not msg_name in h.messages_to_send:
                h.messages_to_send.append(msg_name)
            self._fill_host_messages_list(h)
        except:
            print traceback.format_exc()

    def btnRemoveSendMessage_on_click(self, event): # wxGlade: SendMessageInterface.<event_handler>
        try:
            host = self.get_selected_host()
            if None == host:
                return
            
            r = self.listSendMessages.GetFirstSelected()
            sel_rows = []
            while r>=0:
                sel_rows.append(r)
                r = self.listSendMessages.GetNextSelected(r)
            msgs = []
            for r_cnt in range(len(host.messages_to_send)):
                if r_cnt in sel_rows:
                    continue
                msgs.append(host.messages_to_send[r_cnt])
            host.messages_to_send = msgs
            self._fill_host_messages_list(host)
        except:
            print traceback.format_exc()

    def comboRcvMessages_on_select(self, event): # wxGlade: SendMessageInterface.<event_handler>
        print "Event handler `comboRcvMessages_on_select' not implemented!"
        event.Skip()

    def btnAddRcvMessage_on_click(self, event): # wxGlade: SendMessageInterface.<event_handler>
        print "Event handler `btnAddRcvMessage_on_click' not implemented!"
        event.Skip()

    def btnRemoveRcvMessage_on_click(self, event): # wxGlade: SendMessageInterface.<event_handler>
        print "Event handler `btnRemoveRcvMessage_on_click' not implemented!"
        event.Skip()

    def btnCancel_on_click(self, event): # wxGlade: SendMessageInterface.<event_handler>
        self.Hide()
    
    def _save_to_localdb(self):
        localdb.db.write_persistent("/db/persistent/sendmsg/localhost/remote_hosts", self.remote_hosts)
    
    def _load_from_localdb(self):
        try:
            self.remote_hosts = localdb.db.read_value("/db/persistent/sendmsg/localhost/remote_hosts")
            self.remote_hosts = copy.deepcopy(self.remote_hosts)
        except:
            pass

    def btnSaveToBase_on_click(self, event): # wxGlade: SendMessageInterface.<event_handler>
        try:
            self._save_to_localdb()
            self.Hide()
        except:
            print traceback.format_exc()


def init_module(manager, gui):
    frame = SendMsgInterface(manager)
    gui.register_window(frame, u"Управление обменом сообщениями ", "wnd_sndmsg")

if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = Frame_ViewHandlers()
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
