 #!/usr/bin/env python
# -*- coding: utf-8 -*-


import wx, interface
import wx.grid
import pickle
import localdb
import tree
import adon_window


class Display_localdb(interface.MyFrame, adon_window.AdonWindow):

    def __init__(self, manager):
        self.man = manager
        interface.MyFrame.__init__(self, None, -1, "")
        adon_window.AdonWindow.__init__(self, window_id='wnd_localdb', window_caption='')
        self.filename = localdb.db.filename
        self.root_dir = '/db'
        tree.buildTree(self, self.root_dir)

    def on_form_close(self, event):
        self.Hide()

    def On_apply_clk(self, event):
        value = eval(self.text_ctrl_1.GetValue())
        print value
        print type(value)
        item_id = self.tree_db.GetSelection()
        path = self.tree_db.GetItemText(item_id)
        if localdb.db.read_persistance(str(path)) == 0:
            localdb.db.write_persistent(str(path), value, description=None)
        elif localdb.db.read_persistance(str(path)) == 1:
            localdb.db.write_once(str(path), value, description=None)
        elif localdb.db.read_persistance(str(path)) == 2:
            localdb.db.write_temporary(str(path), value, description=None)
            
    def On_treeitem_dblclk(self, event):
        item_id = self.tree_db.GetSelection()
        path1 = self.tree_db.GetItemText(item_id)
        print 'type:', type(path1)
        print 'path', path1
        self.text_ctrl_1.SetValue(str(localdb.db.read_value(str(path1))))

    def On_refresh_clk(self, event=None):
        self.tree_db.DeleteAllItems()
        tree.buildTree(self, self.root_dir)

def init_module(manager, gui):
    frame = Display_localdb(manager)
    gui.register_window(frame, u"Просмотр параметров локальной БД", "wnd_view_settings_db")


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = Display_localdb()
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop() 
