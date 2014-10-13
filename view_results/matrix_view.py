 #!/usr/bin/env python
# -*- coding: utf-8 -*-


import numpy as np
import wx, matrix_interface, os
import wx.grid
import functools
import numpy
import localdb
import traceback

class MatrixFrame(matrix_interface.MatrixFrame):

    def __init__(self):
        matrix_interface.MatrixFrame.__init__(self, None, -1, "")
        self.matrixes = []
        self.matrix = None
                
    def set_matrix(self, matrix):
        self.matrix = matrix

    def add_matrix(self, matrix, caption):
        self.matrixes.append((caption, matrix))
                
    def chooses(self, msg, butt_type):
        """ Ф-ция открывает диалог проводника """
        
        wildcard = "Техт Files (*.txt)|*.dat;*.prn;*.txt|"\
        "All files (*.*)|*.*"
        dialog = wx.FileDialog(None, msg, os.getcwd(),"", wildcard, butt_type|wx.MULTIPLE)    #wx.OPEN
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
        dialog.Destroy()
        return path

    def On_spin_clk(self, event, slice_num, form_obj):
        
        self.matr.DeleteCols(0, self.matr.GetNumberCols())
        self.matr.DeleteRows(0, self.matr.GetNumberRows())
        str_slice_rows = 'self.matrix'
        for i in range(len(self.matrix.shape[:-2])):
            str_slice_rows = str_slice_rows + '[0]'
        str_slice_cols = str_slice_rows + '[0]'
        self.matr.AppendRows(len(eval(str_slice_rows)))
        self.matr.AppendCols(len(eval(str_slice_cols)))
        for i in range(self.matr.GetNumberCols()):
            self.matr.SetColLabelValue(i, str(i+1))
        slices = 'self.matrix'
        for i in range(len(self.matrix.shape[:-2])):      #int(self.dimension.GetValue())
            num_cur_slice = form_obj[i].GetValue()                  #self.slice_0.GetValue()
            slices = slices + '[' + str(num_cur_slice) + ']'
            for i in range(len(eval(slices))):                      #len(array[num])
                for j in range(len(eval(slices)[i])):               #len(array[num][i])
                    self.matr.SetCellValue(i, j, str(eval(slices)[i][j])) #array[num]
    
    def On_btn_trans(self, event):
        matrix = []
        for i in range(self.matr.GetNumberRows()):
            matr_str = []
            for j in range(self.matr.GetNumberCols()):
                matr_str.append(int(self.matr.GetCellValue(i, j)))
            matrix.append(matr_str)
        matrix = np.array(matrix)
        T_array = matrix.T
        rows = len(T_array)
        cols = len(T_array[0])
        self.matr.DeleteCols(0, self.matr.GetNumberCols())
        self.matr.DeleteRows(0, self.matr.GetNumberRows())
        self.matr.AppendRows(rows)
        self.matr.AppendCols(cols)
        for i in range(self.matr.GetNumberCols()):
            self.matr.SetColLabelValue(i, str(i+1))
        for i in range(len(T_array)):
            for j in range(len(T_array[i])):
                self.matr.SetCellValue(i, j, str(T_array[i][j]))

    def On_btn_save(self, event):
        num_rows = self.matr.GetNumberRows()
        num_cols = self.matr.GetNumberCols()
        #if self.matr.IsSelection():
        if self.matr.GetSelectedCols():
            file_path = self.chooses(u"Выберите текстовый файл", wx.OPEN)
            fd = open(file_path, 'w')
            for i in range(num_rows):
                fd.writelines(self.matr.GetCellValue(i, self.matr.GetSelectedCols()[0]) + '\n')
            fd.close()
        elif self.matr.GetSelectedRows():
            file_path = self.chooses(u"Выберите текстовый файл", wx.OPEN)
            fd = open(file_path, 'w')
            for i in range(num_cols):
                fd.writelines(self.matr.GetCellValue(self.matr.GetSelectedRows()[0], i) + '\n')
            fd.close()
        else:
            file_path = self.chooses(u"Выберите текстовый файл", wx.OPEN)
            fd = open(file_path, 'w')
            for i in range(num_rows):
                for j in range(num_cols):
                    fd.writelines(self.matr.GetCellValue(i, j) + '\n')
                fd.writelines('\n')
            fd.close()
    def show_matrix(self, matrix):
        self.matrix = matrix
        if None==self.matrix:
            return
        self.dimension.Enable(False)
        self.dimension.SetValue(str(len(self.matrix.shape)))
        left = 0
        dictionary = {}
        str_slice_rows = 'self.matrix'
        form_obj = []
        if len(self.matrix.shape)>1:
            for i in range(len(self.matrix.shape[:-2])):
                right = self.matrix.shape[i]
                dictionary['self.slice_' + str(i)] = wx.SpinCtrl(self, -1, "0", min=left, max=right-1)
                vars()['self.slice_' + str(i)] = dictionary['self.slice_' + str(i)]
                self.sizer_5.Add(vars()['self.slice_' + str(i)], 0, wx.LEFT, 10)
                form_obj.append(vars()['self.slice_' + str(i)])
                func = functools.partial(self.On_spin_clk, slice_num = i, form_obj = form_obj)
                self.Bind(wx.EVT_SPINCTRL, func)
                str_slice_rows = str_slice_rows + '[0]'
            str_slice_cols = str_slice_rows + '[0]'
        else:
            str_slice_cols = "[0]"
        try:
            self.matr.DeleteRows(0, self.matr.NumberRows)
            self.matr.DeleteCols(0, self.matr.NumberCols)
        except:
            pass
        self.matr.AppendRows(len(eval(str_slice_rows)))
        self.matr.AppendCols(len(eval(str_slice_cols)))
        for i in range(self.matr.GetNumberCols()):
            self.matr.SetColLabelValue(i, str(i+1))
        for i in range(len(eval(str_slice_rows))):
            for j in range(len(eval(str_slice_rows)[i])):
                self.matr.SetCellValue(i, j, str(eval(str_slice_rows)[i][j]))
    def plot(self): 
        matrix_list = [m[0] for m in self.matrixes]
    	self.lbMatrixes.SetItems(matrix_list)
        self.show_matrix(None)
        self.Show()
            
    def lbMatrixes_on_select(self, event):
        sel = self.lbMatrixes.GetSelection()
        if sel < 0:
        	return
        matrix = self.matrixes[sel][1]
        self.show_matrix(matrix)

class AppendableString(object):
    def __init__(self, s):
        self.s = s
    def clone(self):
        return AppendableString(self.s)
    def append(self,s):
        self.s = self.s+u"->"+s
    def get_str(self):
        return self.s

class ViewerMatrix:
    def __init__(self):
    	pass

    def list_has_objects(self, obj):
        """ Определяет наличие в списке объектов со сложной структурой """
        for v in obj:
            if not isinstance(v, int) and not isinstance(v, float) and \
                not isinstance(v, complex) and not isinstance(v, str):
                return True
        return False
    def traverse_list(self, obj, name="object", ap_str=None):
        if not self.list_has_objects(obj):
            return
        #Есть объекты и их необходмо отобразить
        obj_name = 'list '+name+' = [obj*'+str(len(obj))+']'
            
        obj_cnt = 0
        for v in obj:
            item_name = obj_name+"["+str(obj_cnt)+"]"
            ap_str_clone = ap_str.clone()
            ap_str_clone.append(item_name)
            self.objtraverse(v, name+"["+str(obj_cnt)+"]", ap_str_clone)
            obj_cnt += 1
        
    def traverse_tuple(self, obj, name="object", ap_str=None):
        if not self.list_has_objects(obj):
            return
        #Есть объекты и их необходмо отобразить
        obj_name = 'tuple '+name+' = (obj*'+str(len(obj))+')'
        unroll = True
        
        obj_cnt = 0
        for v in obj:
            item_name = obj_name+"("+str(obj_cnt)+")"
            ap_str_clone = ap_str.clone()
            ap_str_clone.append(item_name)
            self.objtraverse(v, name+"("+str(obj_cnt)+")", ap_str_clone)
            obj_cnt += 1

    def traverse_dict(self, obj, name="object", ap_str=None):
        if not self.list_has_objects(obj.values()):
            return
        #Есть объекты и их необходмо отобразить
        obj_name = 'dict '+name+' = {obj*'+str(len(obj))+'}'
        ap_str
        
        for k in obj.keys():
            item_name = obj_name+"["+str(k)+"]"
            ap_str_clone = ap_str.clone()
            ap_str_clone.append(item_name)
            self.objtraverse(obj[k], name+"["+str(k)+"]", ap_str_clone)

    def traverse_numpy(self, obj, name="object", ap_str = None):
        obj_name = 'numpy '+name+' = [...*'+str(obj.shape)+']'
        ap_str.append(obj_name)
        self.matrixes.append((ap_str.get_str(), obj))
    
    def objtraverse(self, obj, name="object", ap_str=None):
        is_object = False
        if isinstance(obj, dict):
            self.traverse_dict(obj, name, ap_str.clone())
            return
        elif isinstance(obj, list):
            self.traverse_list(obj, name, ap_str.clone())
            return
        elif isinstance(obj, tuple):
            self.traverse_tuple(obj, name, ap_str.clone())
            return
        elif isinstance(obj, str):
            return
        elif isinstance(obj, unicode):
            return
        elif isinstance(obj, int):
            return
        elif isinstance(obj, type):
            return
        elif None==obj:
            return
        elif isinstance(obj, long):
            return
        elif isinstance(obj, numpy.ndarray):
            self.traverse_numpy(obj, name, ap_str.clone())
            return
        elif isinstance(obj, float):
            return
        elif isinstance(obj, complex):
            return
        else:
            obj_name = 'class '+obj.__class__.__name__+' '+name
            is_object = True
        
        try:
            if is_object:
                if obj in self.objstack:
                    return
                self.objstack.append(obj)
                items = dir(obj)
                for n in ( x for x in dir(obj) if not x.startswith('__') ):
                    try:
                        self.objtraverse(obj.__dict__[n], n, ap_str.clone())
                    except KeyError:
                        pass
                    except:
                        print traceback.format_exc()
                self.objstack = self.objstack[0:-1]
        except:
            print traceback.format_exc()
    def generate(self, ticket, plotter):
        obj = ticket.get_data()
        self.matrixes = []
        self.objstack = []
        self.objtraverse(obj, ap_str=AppendableString(u"Matrix "))
        for m in self.matrixes:
            plotter.add_matrix(m[1], m[0])
        #plotter.add_matrix(numpy.zeros((10,20)), "matrix1")
        #plotter.add_matrix(numpy.zeros((20,30)), "matrix2")
        #plotter.set_matrix(matrix)

def init_module(manager, gui):
	localdb.db.write_temporary("/db/temporary/plotters/matrixplot/class", MatrixFrame)
	localdb.db.write_temporary("/db/temporary/plotters/matrixplot/name", "matrixplot")
	localdb.db.write_temporary("/db/temporary/plotters/matrixplot/caption", u"Отображение матриц")
	
	localdb.db.write_temporary("/db/temporary/viewers/matrix/class", ViewerMatrix)
	localdb.db.write_temporary("/db/temporary/viewers/matrix/id", "viewer-matrix")
	localdb.db.write_temporary("/db/temporary/viewers/matrix/caption", u"Отображение матриц")
	localdb.db.write_temporary("/db/temporary/viewers/matrix/tags", [".*",])
	localdb.db.write_temporary("/db/temporary/viewers/matrix/data_names", [])
	localdb.db.write_temporary("/db/temporary/viewers/matrix/plotter/name", "matrixplot")
	localdb.db.write_temporary("/db/temporary/viewers/matrix/plotter/multiplexable", False)
	return []

if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = MatrixFrame()
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()


