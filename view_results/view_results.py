#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import re
import manager
import view_results_interface
import traceback
import os
import pickle
import pprint
import time
import localdb
import adon_window

from view_core import *

class TicketNode:
    def __init__(self, ticket, id_track_from_node):
        self.nodes = {}
        self.ticket = None
        self.id = id_track_from_node[0]
        if len(id_track_from_node)==1:
            #Это последний элемент в пути id_track, соответсвенно, сохраняем тикет в этом элементе и заканчиваем обработку
            self.ticket = ticket.export_standalone_ticket()
        elif len(id_track_from_node)>1:
            #Это не последний элемент в дереве. Продолжаем создавать элементы
            self.nodes[id_track_from_node[1]] = TicketNode(ticket, id_track_from_node[1:])
        else:
            #Fuckup!
            raise "Куда-то пропал элемент дерева"
    def add_ticket(self, ticket, id_track_from_node):
        if len(id_track_from_node)==0:
            self.ticket = ticket
            return

        leading_id = id_track_from_node[0]
        if self.nodes.has_key(leading_id):
            self.nodes[leading_id].add_ticket(ticket, id_track_from_node[1:])
        else:
            self.nodes[leading_id] = TicketNode(ticket, id_track_from_node)

    def print_node(self, tab_count = 0):
        try:
            if None != self.ticket:
                print '  '*tab_count, self.ticket.description, self.ticket.get_data_name()
            else:
                print '  '*tab_count, self.id
            for k in self.nodes.keys():
                self.nodes[k].print_node(tab_count+1)
        except:
            pass
    
    def get_node_name(self):
        return unicode(self.ticket.description) + u" " + unicode(self.ticket.get_data_name()) + " " + unicode(self.ticket.get_data_tag())

class TicketTree:
    def __init__(self):
        self.root_nodes = {}
        self.max_ticket_id = 0
    def clear(self):
        pass
    def add_ticket(self, ticket):
        try:
            id_track = ticket.get_id_track()
            leading_id = id_track[0]
            if self.root_nodes.has_key(leading_id):
                self.root_nodes[leading_id].add_ticket(ticket, id_track[1:])
            else:
                self.root_nodes[leading_id] = TicketNode(ticket, id_track)
            if self.max_ticket_id<leading_id:
                self.max_ticket_id = leading_id
        except:
            print traceback.format_exc()
            print ticket
    def print_tree(self):
        for k in self.root_nodes.keys():
            self.root_nodes[k].print_node()
    def get_max_ticket_id(self):
        return self.max_ticket_id


class ResultFrame:
    def __init__(self, manager = None):
        self.man = manager
        if None != self.man:
            self.man.register_handler(None, self.handle_all_tickets)
        self.tt = TicketTree()
        self.readonly = False

    def handle_all_tickets(self, ticket):
        if self.readonly:
            return
        self.tt.add_ticket(ticket)
    def add_ticket(self, ticket):
        self.tt.add_ticket(ticket)
    def store(self, filename):
        slf = StandaloneResultFrame(self.tt)
        slf.store(filename)
    def load(self, filename, readonly=False):
        try:
            with open(filename, 'r') as fd_store_file:
                slf = pickle.load(fd_store_file)
            self.tt = slf.tt
            self.readonly = readonly
        except:
            print traceback.format_exc()
    def get_max_ticket_id(self):
        return self.tt.get_max_ticket_id()

class StandaloneResultFrame:
    def __init__(self, ticket_tree):
        self.tt = ticket_tree
    def store(self, filename):
        try:
            with open(filename, 'w') as fd_store_file:
                pickle.dump(self, fd_store_file)
        except:
            print traceback.format_exc()
    
class MenuEx(wx.Menu):
    def __init__(self):
        wx.Menu.__init__(self)
        self.pydata = {}
    def Append(self, caption, handler, pydata=None):
        item_id = wx.NewId()
        mmi = wx.MenuItem(self, item_id, caption)
        wx.Menu.AppendItem(self, mmi)
        self.Bind(wx.EVT_MENU, handler, mmi)
        self.pydata[item_id] = pydata
    def GetPyData(self, item_id):
        return self.pydata[item_id]

class ViewResultsInst(view_results_interface.ViewResults, adon_window.AdonWindow):
    def __init__(self, manager):
        view_results_interface.ViewResults.__init__(self, None, -1, "")
        adon_window.AdonWindow.__init__(self, window_id='wnd_results', window_caption='')
        #self.Bind(wx.EVT_CLOSE, self.btnClose_handler, self)
        #self.Bind(wx.EVT_SHOW,  self.OnShow_handler, self)
        self.Bind(wx.EVT_CONTEXT_MENU, self.treeResults_on_right_click)
        self.lbShowableResults.Bind(wx.EVT_RIGHT_UP, self.lbShowableResults_rightclick)
        self.treeResults.SetMinSize(wx.Size(w=100, h=100))
        self.man = manager
        self.rf = ResultFrame(self.man)
        self.view_manager = ViewManager()
        self.results_to_view = ResultsToView(self.view_manager)
        self.re = None
        self.load_ticket_filter()
        
    def _add_tree_node(self, parent_item, node):
        node_name = node.get_node_name()
        itm = self.treeResults.AppendItem(parent_item, node_name)
        self.treeResults.SetItemPyData(itm, node.ticket)
        if None!=self.re:
            if None != self.re.match(node_name):
                self.treeResults.SetItemBold(itm, True)
        for v in node.nodes.values():
            self._add_tree_node(itm, v)
        self.treeResults.Expand(itm)
        
    def show_result_frame(self):
        try:
            filter_string = self.comboFilter.GetValue()
            if len(filter_string):
                filter_string = filter_string.replace('.', '\\.').replace('*', '.*')
                self.re = re.compile(filter_string)
            else:
                self.re = None
            self.treeResults.DeleteAllItems()
            parent_item = self.treeResults.AddRoot(u'Перехваченные сообщения')
            for v in self.rf.tt.root_nodes.values():
                self._add_tree_node(parent_item, v)
            self.treeResults.Expand(parent_item)
        except:
            print traceback.format_exc()

    def store_ticket_filter(self):
        try:
            filter_string = self.comboFilter.GetValue()
            filter_items = self.comboFilter.GetItems()
            if not filter_string in filter_items:
                filter_items.insert(0, filter_string)
                localdb.db.write_persistent('/db/persistent/view_results/filters', filter_items)
                self.comboFilter.SetItems(filter_items)
        except:
            print traceback.format_exc()

    def load_ticket_filter(self):
        try:
            filter_items = localdb.db.read_value('/db/persistent/view_results/filters')
            self.comboFilter.SetItems(filter_items)
        except:
            pass
    
    def treeResults_on_right_click(self, event):
        itm = self.treeResults.GetSelection()
        ticket = self.treeResults.GetItemPyData(itm)
        if None == ticket:
            return
        
        menu = MenuEx()
        menu.Append(u"Отправить выбранное повторно", self.treeResults_on_send_again, ticket)
        menu.Append(u"Сохранить выбранное как фрейм...", self.treeResults_on_save_as_frame, ticket)
        menu.AppendSeparator()
        
        view_manager = ViewManager()
        for view_wrapper in view_manager.get_ticket_capability_list(ticket):
            menu.Append(u"Отобразить с помощью "+view_wrapper.get_viewer_caption(), self.treeResults_on_show_as, (view_wrapper, ticket))
        menu.AppendSeparator()
        for view_wrapper in view_manager.get_ticket_capability_list(ticket):
            menu.Append(u"Добавить к отображению как "+view_wrapper.get_viewer_caption(), self.treeResults_on_add_as, (view_wrapper, ticket))
        self.treeResults.PopupMenu(menu)
        
    def treeResults_on_send_again(self, event):
        item_id = event.GetId()
        menu = event.GetEventObject()
        original_ticket = menu.GetPyData(item_id)
        self.man.push_ticket(self.man.ticket(original_ticket.get_data_name(), original_ticket.get_data(), original_ticket.description))
    def treeResults_on_save_as_frame(self, event):
        item_id = event.GetId()
        menu = event.GetEventObject()
        ticket = menu.GetPyData(item_id)
        
        filename = None
        wildcard = u"Сохраненные фреймы (*.frm)|*.frm|Все файлы  (*.*)|*.*"
        dialog = wx.FileDialog(None, u"Сохранить выбранный тикет как фрейм", self.get_user_store_path(),time.ctime(time.time()) + ".frm", wildcard, wx.SAVE)
        if dialog.ShowModal() == wx.ID_OK:
            filename = dialog.GetPath()
            user_store_path = os.path.dirname(os.path.realpath(filename))
            localdb.db.write_persistent('/db/persistent/view_results/default_store_path', user_store_path)
        dialog.Destroy()
        if None == filename:
            return
        rf = ResultFrame(None)
        rf.add_ticket(ticket)
        rf.store(filename)
    def treeResults_on_show_as(self, event):
        item_id = event.GetId()
        menu = event.GetEventObject()
        view_wrapper, ticket = menu.GetPyData(item_id)
        vt = ViewTicket(ticket, view_wrapper)
        vt.show()
    def treeResults_on_add_as(self, event):
        item_id = event.GetId()
        menu = event.GetEventObject()
        view_wrapper, ticket = menu.GetPyData(item_id)
        self.results_to_view.add_ticket(ticket, view_wrapper)
        self.results_to_view.update_view_widget(self.lbShowableResults)

    def comboFilter_Enter_handler(self, event):
        self.show_result_frame()
        self.store_ticket_filter()

    def comboFilter_handler(self, event):
        self.show_result_frame()
        
    def btnNewFrame_handler(self, event):
        self.rf = ResultFrame(self.man)

    def get_user_store_path(self):
        user_store_path = os.path.expanduser('~/')
        try:
            user_store_path = localdb.db.read_value('/db/persistent/view_results/default_store_path')
        except:
            pass
        return user_store_path

    def btnRefresh_handler(self, event):
        self.show_result_frame()

    def btnLoadFrame_handler(self, event):
        filename = None
        wildcard = u"Сохраненные фреймы (*.frm)|*.frm|Все файлы  (*.*)|*.*"
        dialog = wx.FileDialog(None, u"Загрузить фрейм", self.get_user_store_path(),"", wildcard, wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            filename = dialog.GetPath()
            user_store_path = os.path.dirname(os.path.realpath(filename))
            localdb.db.write_persistent('/db/persistent/view_results/default_store_path', user_store_path)
        dialog.Destroy()
        if None == filename:
            return
        self.rf.load(filename, readonly=False)
        self.man.set_ticketid_low_limit(self.rf.get_max_ticket_id()+1)
        self.show_result_frame()

    def OnShow_handler(self, event):
        try:
            if event.GetShow():
                self.show_result_frame()
        except:
            print traceback.format_exc()

    def btnLoadFrameRo_handler(self, event):
        filename = None
        wildcard = u"Сохраненные фреймы (*.frm)|*.frm|Все файлы  (*.*)|*.*"
        dialog = wx.FileDialog(None, u"Загрузить фрейм для просмотра (readonly)", self.get_user_store_path(),"", wildcard, wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            filename = dialog.GetPath()
            user_store_path = os.path.dirname(os.path.realpath(filename))
            localdb.db.write_persistent('/db/persistent/view_results/default_store_path', user_store_path)
        dialog.Destroy()
        if None == filename:
            return
        self.rf.load(filename, readonly=True)
        self.show_result_frame()

    def btnStoreFrame_handler(self, event):
        filename = None
        wildcard = u"Сохраненные фреймы (*.frm)|*.frm|Все файлы  (*.*)|*.*"
        dialog = wx.FileDialog(None, u"Сохранить фрейм", self.get_user_store_path(),time.ctime(time.time()) + ".frm", wildcard, wx.SAVE)
        if dialog.ShowModal() == wx.ID_OK:
            filename = dialog.GetPath()
            user_store_path = os.path.dirname(os.path.realpath(filename))
            localdb.db.write_persistent('/db/persistent/view_results/default_store_path', user_store_path)
        dialog.Destroy()
        if None == filename:
            return
        self.rf.store(filename)

    def btnApplyFilter_handler(self, event):
        self.show_result_frame()
        self.store_ticket_filter()

    def btnMovePlotUp_handler(self, event):
        selection = self.lbShowableResults.GetSelection()
        if wx.NOT_FOUND == selection or selection<1:
            return
        self.results_to_view.move_up(selection)
        self.results_to_view.update_view_widget(self.lbShowableResults)
        self.lbShowableResults.SetSelection(selection - 1)

    def btnPlotDown_handler(self, event):
        selection = self.lbShowableResults.GetSelection()
        if wx.NOT_FOUND == selection or selection>=self.lbShowableResults.GetCount()-1:
            return
        self.results_to_view.move_down(selection)
        self.results_to_view.update_view_widget(self.lbShowableResults)
        self.lbShowableResults.SetSelection(selection + 1)
    
    def treeResults_activate_handler(self, event):
        itm = event.GetItem()
        self.treeResults.Expand(itm)
        ticket = self.treeResults.GetItemPyData(itm)
        self.results_to_view.add_ticket(ticket, None)
        self.results_to_view.update_view_widget(self.lbShowableResults)
        
    def lbShowableResults_dblclick(self, event):
        selection = self.lbShowableResults.GetSelection()
        if wx.NOT_FOUND == selection:
            return
        itm_data = self.lbShowableResults.GetClientData(selection)
        self.results_to_view.remove_ticket(itm_data[0])
        self.results_to_view.update_view_widget(self.lbShowableResults)

    def lbShowableResults_handler(self, event):
        selection = self.lbShowableResults.GetSelection()
        if wx.NOT_FOUND == selection:
            return
        itm_data = self.lbShowableResults.GetClientData(selection)
        ticket_data = itm_data[0].get_data()
        self.textResultInfo.Clear()
        self.textResultInfo.AppendText(pprint.pformat(ticket_data))
        
    def lbShowableResults_rightclick(self, event):
        selection = self.lbShowableResults.GetSelection()
        if wx.NOT_FOUND == selection:
            return
        itm_data = self.lbShowableResults.GetClientData(selection)
        popupmenu = MenuEx()
        popupmenu.Append("Удалить элемент", self.OnDeleteItem, itm_data)
        popupmenu.AppendSeparator()
        popupmenu.Append(u"Просмотр: " + itm_data[1].get_viewer_caption(), self.OnEmtyHandler)
        viewers_list = self.results_to_view.view_manager.get_ticket_capability_list(itm_data[0])
        if len(viewers_list) > 1:
            popupmenu.AppendSeparator()
            for v in viewers_list:
                popupmenu.Append(u"Изменить на: "+v.get_viewer_caption(), self.OnSelectViewer, [itm_data[0], v])
        self.lbShowableResults.PopupMenu(popupmenu)
    def OnDeleteItem(self, event):
        item_id = event.GetId()
        menu = event.GetEventObject()
        itm_data = menu.GetPyData(item_id)
        self.results_to_view.remove_ticket(itm_data[0])
        self.results_to_view.update_view_widget(self.lbShowableResults)
    def OnSelectViewer(self, event):
        item_id = event.GetId()
        menu = event.GetEventObject()
        itm_data = menu.GetPyData(item_id)
        self.results_to_view.update_ticket_viewer(itm_data[0], itm_data[1])
        self.results_to_view.update_view_widget(self.lbShowableResults)
    def OnEmtyHandler(self, event):
        pass
    def btnClose_handler(self, event):
        self.Hide()
    def btnPlot_handler(self, event):
        self.results_to_view.show_results()

def init_module(manager, gui):
    vi = ViewResultsInst(manager)
    gui.register_window(vi, u"Отображение результатов", "wnd_results")
    return vi

