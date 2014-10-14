#!/usr/bin/env python
# -*- coding: utf-8 -*-


import wx
import traceback
import exception_viewer_interface
import adon_window


class Frame_ExceptionViewer(exception_viewer_interface.ExceptionViewer, adon_window.AdonWindow):
    def __init__(self, manager):
        exception_viewer_interface.ExceptionViewer.__init__(self, None, -1, "")
        adon_window.AdonWindow.__init__(self, window_id='wnd_view_exceptions', window_caption='')
        self.Bind(wx.EVT_SHOW, self.on_form_show, self)
        self.man = manager
        self.man.register_handler("core::exception", self.handle_exception)
        self.exc = []
    def handle_exception(self, ticket):
        try:
            e = ticket.get_data()
            self.exc.append(e)
            wx.CallAfter(self.redraw_list)
            #self.redraw_list()
        except:
            print traceback.format_exc()
    def redraw_list(self):
        self.listExceptions.Clear()
        for e in self.exc:
            exc_info = "{0} - {1}: {2} in {3}".format(e.get_source_file(), str(e.get_line_number()), e.get_reason(), e.get_func_name())
            self.listExceptions.Append(exc_info, e)
    def on_form_close(self, event):
        self.Hide()
    def on_form_show(self, evt):
        adon_window.AdonWindow.on_form_show(self, evt)
        if evt.GetShow():
            pass
    def btnClear_onclick(self, event):
        self.exc = []
        self.redraw_list()

    def btnSave_onclick(self, event):
        pass

    def btnLoad_onclick(self, event):
        pass

    def listExceptions_onselect(self, event):
        sel = self.listExceptions.GetSelection()
        if sel < 0:
            return
        e = self.exc[sel]
        msg = e.get_message()
        with open(e.get_source_file()) as f:
            content = f.readlines()
        start_line = max(0, e.get_line_number()-5)
        stop_line = min(e.get_line_number()+5, len(content))
        msg += '\r\nContent:\r\n'
        for l in content[start_line:stop_line]:
            msg += l
        self.textException.SetValue(msg)

def init_module(manager, gui):
    frame = Frame_ExceptionViewer(manager)
    gui.register_window(frame, u"Просмотр исключений", "wnd_view_exception")

