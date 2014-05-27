 #!/usr/bin/env python
# -*- coding: utf-8 -*-


import numpy as np
import wx, matrix_interface, os
import wx.grid
import functools
import localdb

class MatrixFrame(matrix_interface.MatrixFrame):

    def __init__(self):
        matrix_interface.MatrixFrame.__init__(self, None, -1, "")
                
    def set_matrix(self, matrix):
        self.matrix = matrix
                
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
    
    def plot(self):
        self.dimension.Enable(False)
        self.dimension.SetValue(str(len(self.matrix.shape)))
        left = 0
        dictionary = {}
        str_slice_rows = 'self.matrix'
        form_obj = []
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
        self.matr.AppendRows(len(eval(str_slice_rows)))
        self.matr.AppendCols(len(eval(str_slice_cols)))
        for i in range(self.matr.GetNumberCols()):
            self.matr.SetColLabelValue(i, str(i+1))
        for i in range(len(eval(str_slice_rows))):
            for j in range(len(eval(str_slice_rows)[i])):
                self.matr.SetCellValue(i, j, str(eval(str_slice_rows)[i][j]))
        
        self.Show()

class ViewerMatrix:
    def __init__(self):
    	pass
    def generate(self, ticket, plotter):
        matrix = ticket.get_data()
        plotter.set_matrix(matrix)

def init_module(manager, gui):
	localdb.db.write_temporary("/db/temporary/plotters/matrixplot/class", MatrixFrame)
	localdb.db.write_temporary("/db/temporary/plotters/matrixplot/name", "matrixplot")
	localdb.db.write_temporary("/db/temporary/plotters/matrixplot/caption", u"Отображение матриц")
	
	localdb.db.write_temporary("/db/temporary/viewers/matrix/class", ViewerMatrix)
	localdb.db.write_temporary("/db/temporary/viewers/matrix/id", "viewer-matrix")
	localdb.db.write_temporary("/db/temporary/viewers/matrix/caption", u"Отображение матриц")
	localdb.db.write_temporary("/db/temporary/viewers/matrix/tags", ["matrix",])
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


