#!/usr/bin/env python
# -*- coding: utf-8 -*-


import wx
import objview_interface
import localdb
import numpy
import traceback
import pprint
import os
import pickle

class ObjViewInst(objview_interface.ObjView):
    def __init__(self):
        objview_interface.ObjView.__init__(self, None, -1, "")
        self.load_config();
        self.obj = []
        
    def load_config(self):
        self.expand_all = False
        self.max_unroll_list = 10
        self.max_unroll_dict = 10
        self.max_unroll_matrix = 10
        try:
            self.expand_all = localdb.db.read_value("/db/persistent/objview/unroll_all")
            self.max_unroll_list = localdb.db.read_value("/db/persistent/objview/max_unroll_list")
            self.max_unroll_dict = localdb.db.read_value("/db/persistent/objview/max_unroll_dict")
            self.max_unroll_matrix = localdb.db.read_value("/db/persistent/objview/max_unroll_matrix")
        except:
            pass
        self.max_list.SetValue(str(self.max_unroll_list))
        self.max_dict.SetValue(str(self.max_unroll_dict))
        self.max_matr.SetValue(str(self.max_unroll_matrix))
        self.unroll_all.SetValue(self.expand_all)
        
    def add_object(self, obj):
        self.obj.append(obj)
    def view_objects(self):
        root_item = self.tree_obj.AddRoot(u"Объекты")
        for o in self.obj:
            try:
                self.objstack = []
                self.objtraverse(o, parent_item=root_item)
            except:
                pass
        self.tree_obj.Expand(root_item)
        
    def plot(self):
        self.view_objects()
        self.Show()

    def list_has_objects(self, obj):
        """ Определяет наличие в списке объектов со сложной структурой """
        for v in obj:
            if not isinstance(v, int) and not isinstance(v, float) and \
                not isinstance(v, complex) and not isinstance(v, str):
                return True
        return False
    def traverse_list(self, obj, name="object", parent_item=None):
        has_objects = self.list_has_objects(obj)
        unroll = False
        if len(obj) <= self.max_unroll_list and not has_objects:
            #Простейший вариант списка - содержимое можно отобразить прямо в дереве
            obj_name = 'list '+name+' = '+str(obj)
        elif len(obj) > self.max_unroll_list and not has_objects:
            #Объектов нет, но размер превышает максимально разворачиваемый размер
            obj_name = 'list '+name+' = [...*'+str(len(obj))+']'
        elif len(obj) > self.max_unroll_list:
            #Есть объекты, но размер превышает максимально разворачиваемый размер
            obj_name = 'list '+name+' = [obj*'+str(len(obj))+']'
        else:
            #Есть объекты и их необходмо отобразить
            obj_name = 'list '+name+' = [obj*'+str(len(obj))+']'
            unroll = True
        
        if None == parent_item:
            itm = self.tree_obj.AddRoot(obj_name)
        else:
            itm = self.tree_obj.AppendItem(parent_item, obj_name)
        self.tree_obj.SetItemPyData(itm, obj)
        
        if unroll:
            obj_cnt = 0
            for v in obj:
                self.objtraverse(v, name+"["+str(obj_cnt)+"]", itm)
                obj_cnt += 1
        self.tree_obj.Expand(itm)
        
    def traverse_tuple(self, obj, name="object", parent_item=None):
        has_objects = self.list_has_objects(obj)
        unroll = False
        if len(obj) <= self.max_unroll_list and not has_objects:
            #Простейший вариант списка - содержимое можно отобразить прямо в дереве
            obj_name = 'tuple '+name+' = '+str(obj)
        elif len(obj) > self.max_unroll_list and not has_objects:
            #Объектов нет, но размер превышает максимально разворачиваемый размер
            obj_name = 'tuple '+name+' = (...*'+str(len(obj))+')'
        elif len(obj) > self.max_unroll_list:
            #Есть объекты, но размер превышает максимально разворачиваемый размер
            obj_name = 'tuple '+name+' = (obj*'+str(len(obj))+')'
        else:
            #Есть объекты и их необходмо отобразить
            obj_name = 'tuple '+name+' = (obj*'+str(len(obj))+')'
            unroll = True
        
        if None == parent_item:
            itm = self.tree_obj.AddRoot(obj_name)
        else:
            itm = self.tree_obj.AppendItem(parent_item, obj_name)
        self.tree_obj.SetItemPyData(itm, obj)
        
        if unroll:
            obj_cnt = 0
            for v in obj:
                self.objtraverse(v, name+"("+str(obj_cnt)+")", itm)
                obj_cnt += 1
        self.tree_obj.Expand(itm)

    def traverse_dict(self, obj, name="object", parent_item=None):
        has_objects = self.list_has_objects(obj.values())
        unroll = False
        if len(obj) <= self.max_unroll_dict and not has_objects:
            #Простейший вариант списка - содержимое можно отобразить прямо в дереве
            obj_name = 'dict '+name+' = '+str(obj)
        elif len(obj) > self.max_unroll_dict and not has_objects:
            #Объектов нет, но размер превышает максимально разворачиваемый размер
            obj_name = 'dict '+name+' = {...*'+str(len(obj))+'}'
        elif len(obj) > self.max_unroll_dict:
            #Есть объекты, но размер превышает максимально разворачиваемый размер
            obj_name = 'dict '+name+' = {obj*'+str(len(obj))+'}'
        else:
            #Есть объекты и их необходмо отобразить
            obj_name = 'dict '+name+' = {obj*'+str(len(obj))+'}'
            unroll = True
        
        if None == parent_item:
            itm = self.tree_obj.AddRoot(obj_name)
        else:
            itm = self.tree_obj.AppendItem(parent_item, obj_name)
        self.tree_obj.SetItemPyData(itm, obj)
        
        if unroll:
            for k in obj.keys():
                self.objtraverse(obj[k], name+"["+str(k)+"]", itm)
        self.tree_obj.Expand(itm)

    def traverse_numpy(self, obj, name="object", parent_item = None):
        if obj.size <= self.max_unroll_matrix:
            obj_name = 'numpy '+name+' = '+str(obj)
        else:
            obj_name = 'numpy '+name+' = [...*'+str(obj.shape)+']'
        if None == parent_item:
            itm = self.tree_obj.AddRoot(obj_name)
        else:
            itm = self.tree_obj.AppendItem(parent_item, obj_name)
        self.tree_obj.SetItemPyData(itm, obj)
        self.tree_obj.Expand(itm)
    
    def objtraverse(self, obj, name="object", parent_item=None):
        is_object = False
        if isinstance(obj, dict):
            self.traverse_dict(obj, name, parent_item)
            return
        elif isinstance(obj, list):
            self.traverse_list(obj, name, parent_item)
            return
        elif isinstance(obj, tuple):
            self.traverse_tuple(obj, name, parent_item)
            return
        elif isinstance(obj, str):
            obj_name = 'string '+name+' = \''+str(obj)+"'"
        elif isinstance(obj, unicode):
            obj_name = 'string '+name+' = u\''+obj+"'"
        elif isinstance(obj, int):
            obj_name = 'int '+name+' = ' + str(obj)
        elif isinstance(obj, type):
            obj_name = 'type '+name+' = ' + str(obj)
        elif None==obj:
            obj_name = 'NoneType '+name+' = None'
        elif isinstance(obj, long):
            obj_name = 'long '+name+' = ' + str(obj)
        elif isinstance(obj, numpy.ndarray):
            self.traverse_numpy(obj, name, parent_item)
            return
        elif isinstance(obj, float):
            obj_name = 'float '+name+' = ' + str(obj)
        elif isinstance(obj, complex):
            obj_name = 'complex '+name+' = ' + str(obj)
        else:
            obj_name = 'class '+obj.__class__.__name__+' '+name
            is_object = True
        
        if None == parent_item:
            parent_item = self.tree_obj.AddRoot(obj_name)
            itm = parent_item
        else:
            itm = self.tree_obj.AppendItem(parent_item, obj_name)
        self.tree_obj.SetItemPyData(itm, obj)
        try:
            if is_object:
                if obj in self.objstack:
                    return
                self.objstack.append(obj)
                items = dir(obj)
                for n in ( x for x in dir(obj) if not x.startswith('__') ):
                    try:
                        self.objtraverse(obj.__dict__[n], n, itm)
                    except KeyError:
                        pass
                    except:
                        print traceback.format_exc()
                self.objstack = self.objstack[0:-1]
        except:
            print traceback.format_exc()
        self.tree_obj.Expand(itm)
        
    def tree_obj_on_activate(self, event):
        try:
            itm = event.GetItem()
            self.tree_obj.Expand(itm)
            obj = self.tree_obj.GetItemPyData(itm)
            self.txt_obj_data.Clear()
            self.txt_obj_data.AppendText(pprint.pformat(obj))
        except:
            print traceback.format_exc()
        
    def on_unroll_clk(self, event):
        pass

    def get_user_load_path(self):
        user_save_path = os.path.expanduser('~/')
        try:
            user_save_path = localdb.db.read_value('/db/persistent/common/default_save_path')
        except:
            pass
        return user_save_path

    def select_file(self, msg):
        filename = None
        wildcard = u"Текстовые файлы (*.txt)|*.txt|Все файлы  (*.*)|*.*"
        dialog = wx.FileDialog(None, msg, self.get_user_load_path(),"", wildcard, wx.SAVE)
        if dialog.ShowModal() == wx.ID_OK:
            filename = dialog.GetPath()
            user_save_path = os.path.dirname(os.path.realpath(filename))
            localdb.db.write_persistent('/db/persistent/common/default_save_path', user_save_path)
        dialog.Destroy()
        return filename
    
    def leaf_to_string(self, itm, offset=0):
        res = ' '*4*offset + self.tree_obj.GetItemText(itm) + "\r\n"
        item, cookie = self.tree_obj.GetFirstChild(itm)
        while item.IsOk():
            res += self.leaf_to_string(item, offset+1)
            item, cookie = self.tree_obj.GetNextChild(itm, cookie)
        return res
    
    def btnSaveView_on_click(self, event):
        try:
            path = self.select_file(u"Сохранить представление объекта в файле...")
            if None==path:
                return
            itm = self.tree_obj.GetSelection()
            with  open(path, 'w') as f:
                f.write(self.leaf_to_string(itm).encode('utf8'))
        except:
            print traceback.format_exc()
        

    def btnSaveObject_on_click(self, event):
        try:
            path = self.select_file(u"Сохранить объект...")
            if None==path:
                return
            itm = self.tree_obj.GetSelection()
            obj = self.tree_obj.GetItemPyData(itm)
            with  open(path, 'w') as f:
                pickle.dump(obj, f)
        except:
            print traceback.format_exc()

    def btnSaveValue_on_click(self, event):
        try:
            path = self.select_file(u"Сохранить тектовое представление значения объекта...")
            if None==path:
                return
            itm = self.tree_obj.GetSelection()
            obj = self.tree_obj.GetItemPyData(itm)
            if isinstance(obj, numpy.ndarray):
                numpy.savetxt(path, obj)
            else:
                with  open(path, 'w') as f:
                    f.write(pprint.pformat(obj))
        except:
            print traceback.format_exc()

    def On_btnsave_clk(self, event):
        self.expand_all = bool(self.unroll_all.GetValue())
        self.max_unroll_list = int(self.max_list.GetValue())
        self.max_unroll_dict = int(self.max_dict.GetValue())
        self.max_unroll_matrix = int(self.max_matr.GetValue())
        try:
            localdb.db.write_persistent("/db/persistent/objview/unroll_all", self.expand_all, u"Разворачивать все списки независимо от их размера")
            localdb.db.write_persistent("/db/persistent/objview/max_unroll_list", self.max_unroll_list, u"Максимальный размер разворачиваемого списка")
            localdb.db.write_persistent("/db/persistent/objview/max_unroll_dict", self.max_unroll_dict, u"Максимальный размер разворачиваемого словаря")
            localdb.db.write_persistent("/db/persistent/objview/max_unroll_matrix", self.max_unroll_matrix, u"Максимальный размер разворачиваемой матрицы (по числу элементов)")
        except:
            print traceback.format_exc()
     
class C:
    def __init__(self, n):
        self.n1 = n
        self.n2 = n+1
        self.n3 = n+2
        
class B:
    def __init__(self):
        self.x="hello"
        self.y="cruel"
        self.z="world"
        self.l = ["q", "a", "z", "w", "s"]
        self.ll = range(1,100)
        self.mtx = numpy.array([3,4,5,6,7,8,9,10,11])
        self.mtx2 = numpy.array([[3,4,5,6,7,8,9,10,11,12,13,14], [3,4,5,6,7,8,9,10,11,12,13,14], [3,4,5,6,7,8,9,10,11,12,13,14]])
  
class A:
    def __init__(self):
        self.cmplx = 12+2j
        self.a=1.0
        self.b=2
        self.c=3
        self.bb=B()
        self.c_l = [C(1), C(10), C(100)]
        self.c_d = {}
        self.n_d = {}
        for i in range(1,5):
            self.c_d[i] = C(i*20)
            self.n_d["itm " + str(i)] = "value " + str(i*10)

        
class ViewerObjects:
    def __init__(self):
        pass
    def generate(self, ticket, plotter):
        obj = ticket.get_data()
        plotter.add_object(obj)
        
def init_db(db):
    pass


def init_module(manager, gui):
    localdb.db.write_temporary("/db/temporary/plotters/objviewplot/class", ObjViewInst)
    localdb.db.write_temporary("/db/temporary/plotters/objviewplot/name", "objviewplot")
    localdb.db.write_temporary("/db/temporary/plotters/objviewplot/caption", u"Отображение структуры объектов")
    
    localdb.db.write_temporary("/db/temporary/viewers/objview/class", ViewerObjects)
    localdb.db.write_temporary("/db/temporary/viewers/objview/id", "viewer-obj")
    localdb.db.write_temporary("/db/temporary/viewers/objview/caption", u"Отображение неклассифицированных объектов")
    localdb.db.write_temporary("/db/temporary/viewers/objview/tags", ["undefined",".*"])
    localdb.db.write_temporary("/db/temporary/viewers/objview/data_names", [])
    localdb.db.write_temporary("/db/temporary/viewers/objview/plotter/name", "objviewplot")
    localdb.db.write_temporary("/db/temporary/viewers/objview/plotter/multiplexable", True)
    return []

if __name__ == "__main__":
    localdb.init_localdb("./config.pickle", init_db)
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = ObjViewInst()
    aa = A()
    frame_1.set_object(aa)
    frame_1.view_object()
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()