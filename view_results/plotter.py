#!/usr/bin/env python
# -*- coding: utf-8 -*-

import localdb
import numpy
from matplotlib import pyplot
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
		pyplot.ion()
		pyplot.figure()
		plot_cnt = 1
		for plt in self.plots:
			pyplot.subplot(len(self.plots), 1, plot_cnt)
			plot_cnt += 1
			if Plotter.is_plot==plt[0]:
				pyplot.plot(plt[2], plt[3])
			if Plotter.is_image==plt[0]:
				pyplot.imshow(plt[1])
		pyplot.show()


def init_module(manager, gui):
	localdb.db.write_temporary("/db/temporary/plotters/plot/class", Plotter)
	localdb.db.write_temporary("/db/temporary/plotters/plot/name", "plot")
	localdb.db.write_temporary("/db/temporary/plotters/plot/caption", u"Компонент Matplotlib")
	return []

