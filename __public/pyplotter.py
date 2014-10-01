#!/usr/bin/env python
# -*- coding: utf-8 -*-

import localdb
import os
import tmpfolder
import numpy
from matplotlib import pyplot
from coresystem import tmpfolder

class PyplotPlotter(object):
    is_plot = 0
    is_image = 1
    def __init__(self):
        self.plots = []
        self.plot_folder = './temporary/plots/'
        try:
            self.plot_folder = localdb.db.read_value('/db/persistent/plotters/plot/def_plot_folder')
        except:
            localdb.db.write_persistent('/db/persistent/plotters/plot/def_plot_folder', self.plot_folder)
    def pyplot_add_plot(self, y, x=None, caption=None):
        if None == x:
            x = numpy.array(range(0, len(y)))
        if None == caption:
            caption = u"График №" + str(len(self.plots)+1)
        self.plots.append([PyplotPlotter.is_plot, caption, x, y])
    def pyplot_add_image(self, img, caption=None):
        if None == caption:
            caption = u"Изображение №" + str(len(self.plots)+1)
        self.plots.append([PyplotPlotter.is_image, img, caption])
    def generate_plotfile(self):
        folder_name = tmpfolder.create_temporary_folder(self.plot_folder)
        py_file_name = folder_name+'plot.py'
        with open(py_file_name, 'w') as f:
            f.write('#!/usr/bin/env python\r\n')
            f.write('# -*- coding: utf-8 -*-\r\n')
            f.write('import os\r\n')
            f.write('import numpy\r\n')
            f.write('from matplotlib import pyplot\r\n')
            f.write('dir_name = os.path.dirname(os.path.realpath(__file__))\r\n')
            f.write('pyplot.figure(num=u"{0}")\r\n'.format(folder_name.encode("utf8")))
            plot_cnt = 1
            plot_count = len(self.plots)
            for plt in self.plots:
                relative_data_file_name = 'datafile_'+str(plot_cnt)
                data_file_name = folder_name+relative_data_file_name
                f.write('pyplot.subplot({0},1,{1})\r\n'.format(plot_count, plot_cnt))
                if PyplotPlotter.is_plot==plt[0]:
                    f.write('data_x = numpy.loadtxt(dir_name+"/{0}_x.gz")\r\n'.format(relative_data_file_name))
                    f.write('data_y = numpy.loadtxt(dir_name+"/{0}_y.gz")\r\n'.format(relative_data_file_name))
                    f.write('pyplot.title(u"{0}")\r\n'.format(plt[1].encode('utf8')))
                    f.write('pyplot.plot(data_x, data_y)\r\n')
                    numpy.savetxt(data_file_name+'_x.gz', plt[2])
                    numpy.savetxt(data_file_name+'_y.gz', plt[3])
                    plot_cnt += 1
                if PyplotPlotter.is_image==plt[0]:
                    f.write('data = numpy.loadtxt(dir_name+"/{0}.gz")\r\n'.format(relative_data_file_name))
                    f.write('pyplot.title(u"{0}")\r\n'.format(plt[2].encode('utf8')))
                    f.write('pyplot.imshow(data)\r\n')
                    numpy.savetxt(data_file_name+'.gz', plt[1])
                    plot_cnt += 1
            f.write('pyplot.show()\r\n')
        return py_file_name

    def pyplot_plot(self):
        py_file_name = self.generate_plotfile()
        os.system('python {0} &'.format(py_file_name))
        return
