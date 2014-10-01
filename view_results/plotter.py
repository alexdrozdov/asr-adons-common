#!/usr/bin/env python
# -*- coding: utf-8 -*-

import localdb
import numpy
from pyplotter import PyplotPlotter

class Plotter(PyplotPlotter):
    def __init__(self):
        PyplotPlotter.__init__(self)
    def add_plot(self, y, x=None, caption=None):
        PyplotPlotter.pyplot_add_plot(self, y, x, caption)
    def add_image(self, img, caption=None):
        PyplotPlotter.pyplot_add_image(self, img, caption)
    def plot(self):
        PyplotPlotter.pyplot_plot(self)


def init_module(manager, gui):
    localdb.db.write_temporary("/db/temporary/plotters/plot/class", Plotter)
    localdb.db.write_temporary("/db/temporary/plotters/plot/name", "plot")
    localdb.db.write_temporary("/db/temporary/plotters/plot/caption", u"Компонент Matplotlib")
    return []
