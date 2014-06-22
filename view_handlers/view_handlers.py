 #!/usr/bin/env python
# -*- coding: utf-8 -*-


import wx, interface_view_handlers


class Frame_ViewHandlers(interface_view_handlers.ViewHandlers):
    def __init__(self, manager):
        interface_view_handlers.ViewHandlers.__init__(self, None, -1, "")
        self.Bind(wx.EVT_SHOW, self.on_show, self)
        self.Bind(wx.EVT_CLOSE, self.on_form_close, self)
        self.man = manager

    def on_form_close(self, event):
        self.Hide()
    def on_show(self, evt):
        if evt.GetShow():
            try:
                self.tree_handlers.DeleteAllItems()
            except:
                pass
            root = self.tree_handlers.AddRoot(u"Обработчики сообщений")
            for k in self.man.handlers.keys():
                info = str(self.man.dis.get_name_by_id(k))+' (id='+str(k)+'; tag='+str(self.man.dis.get_tag_by_id(k))+')'
                key_itm = self.tree_handlers.AppendItem(root, info)
                self.tree_handlers.SetItemBold(key_itm, True)
                handlers = self.man.handlers[k]
                for h in handlers:
                    try:
                        self.tree_handlers.AppendItem(key_itm, str(h.im_class)+"."+str(h.func_name))
                    except:
                        self.tree_handlers.AppendItem(key_itm, str(h.im_class)+"."+str(h.func_name))
                self.tree_handlers.Expand(key_itm)
            self.tree_handlers.Expand(self.tree_handlers.GetRootItem())
                        
    def _set_adons_tree(self, tree, parent_item = None):
        if None == parent_item:
            parent_item = self.tree_ctrl_1.AddRoot(tree.name)
            itm = parent_item
        else:
            itm = self.tree_ctrl_1.AppendItem(parent_item, tree.name)
        self.tree_ctrl_1.SetItemPyData(itm, tree)
        if tree.disabled:
            return
        self.tree_ctrl_1.SetItemBold(itm, True)
        for m in tree.submodules:
            self._set_adons_tree(m, itm)
        self.tree_ctrl_1.Expand(itm)


def init_module(manager, gui):
    frame = Frame_ViewHandlers(manager)
    gui.register_window(frame, u"Контроль обработчиков", "wnd_view_handlers")

if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = Frame_ViewHandlers()
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
