#!/usr/bin/env python
# -*- coding: utf-8 -*-

import localdb
import numpy
# from matplotlib import pyplot
import Gnuplot, Gnuplot.funcutils
from os import system, chdir, mkdir, path
import time
#from mpl_toolkits.mplot3d import Axes3D 



class Plotter:
	is_plot = 0
	is_image = 1
	def __init__(self):
		self.plots = []

	def add_plot(self, y, x=None, caption=None):
		if None == x:
			x = numpy.array(range(0, len(y)))
		if None == caption:
			caption = u"График №" + str(len(self.plots)+1)
		self.plots.append([Plotter.is_plot, caption, x, y])

	def add_image(self, img, caption=None):
		if None == caption:
			caption = u"Изображение №" + str(len(self.plots)+1)
		self.plots.append([Plotter.is_image, img, caption])
	
	def plot(self):
		struct_time = time.localtime()
		sec = struct_time.tm_sec
		minute = struct_time.tm_min
		hour = struct_time.tm_hour
		day = struct_time.tm_mday
		mon = struct_time.tm_mon
		year = struct_time.tm_year
		path_tmp = 'temporary/'
		if path.isdir(path_tmp):
			pass
		else:
			mkdir(path_tmp)
		dir_name = 'dump' + '_' + str(year) + '_' + str(mon) + '_' + str(day) + '_' + str(hour) + ':' + str(minute) + ':' + str(sec) + '/'
		full_path = path_tmp + dir_name
		mkdir(full_path)

		fd = open(full_path + "result.gp", 'w')
		fd.write("#!/usr/bin/gnuplot -persist" + '\n')
		fd.write("reset" + '\n')
		fd.write("set size 1.0, 1.0" + '\n')
		fd.write("set origin 0.0, 0.0" + '\n')
		fd.write("set multiplot" + '\n')
		plot_cnt = 1
		for plt in self.plots:
			name = 'tmp' + str(plot_cnt)
			fd_r = open(full_path + name + '_re.txt', 'w')
			fd_i = open(full_path + name + '_im.txt', 'w')
			data = plt[3]
			for i in range(len(data)):
				fd_r.write(str(data[i].real) + '\n')
				fd_i.write(str(data[i].imag) + '\n')
			fd_r.close()
			fd_i.close()
			com = "set size 1," + str(1.0/len(self.plots))
			fd.write(com + '\n')
			com = "set origin 0.0," + str(1.0/len(self.plots) * (plot_cnt-1))
			fd.write(com + '\n')
			fd.write("set grid" + '\n')
			fd.write("set title 'Data'" + '\n')
			fd.write("set ylabel 'Amplitude'" + '\n')
			fd.write("set xlabel 'Sample'" + '\n')
			com = "plot '" + full_path + name + "_re.txt' with lines, '" + full_path + name + "_im.txt' with lines" + '\n'
			fd.write(com)
			plot_cnt += 1
		fd.write("set nomultiplot")
		fd.close()
		com = 'gnuplot ' + full_path + 'result.gp -persist'
		system(com)

def init_module(manager, gui):
	localdb.db.write_temporary("/db/temporary/plotters/gnuplot/class", Plotter)
	localdb.db.write_temporary("/db/temporary/plotters/gnuplot/name", "gnuplot")
	localdb.db.write_temporary("/db/temporary/plotters/gnuplot/caption", u"Gnuplot")
	return []
