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
		pass

def init_module(manager, gui):
	localdb.db.write_temporary("/db/temporary/plotters/plotter_3d/class", Plotter)
	localdb.db.write_temporary("/db/temporary/plotters/plotter_3d/name", "plotter_3d")
	localdb.db.write_temporary("/db/temporary/plotters/plotter_3d/caption", u"Компонент Matplotlib")
	return []
