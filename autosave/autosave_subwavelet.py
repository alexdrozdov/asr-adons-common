#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
import localdb
import time
import numpy
import tmpfolder

class AutosaveSubwavelet(object):
    def __init__(self, manager, data_id):
        self.data_id = data_id
        self.man = manager
        self.folder_name = None
        self.capture_cnt = 0
        self.man.register_handler(data_id, self.ticket_handler)
    def get_folder_name(self):
        if None==self.folder_name:
            self.folder_name = tmpfolder.create_temporary_folder('./temporary/autosave')
        return self.folder_name
    def ticket_handler(self, ticket):
        subwavelet = ticket.get_data()
        data = subwavelet.get_wavelet()
        mean_width = ticket.find_ticket_by_sticky('mean-width').get_sticky('mean-width')
        base_file_name = ticket.get_description()+'_'+ticket.get_data_name()+'-'+str(self.capture_cnt)
        numpy_file_name = base_file_name+'.numpy'
        json_file_name = base_file_name+'.json'

        path = self.get_folder_name()+numpy_file_name
        numpy.savetxt(path, data)
        
        numpy_file_name = numpy_file_name.encode('utf8')
        description = ticket.get_description().encode('utf8')
        data_name = ticket.get_data_name().encode('utf8')
        path = self.get_folder_name()+json_file_name
        with open(path, 'w') as f:
            f.write('{"description": "'+description+'", "data_name": "'+data_name+'", "format": "numpy", "data_file": "'+numpy_file_name+'", "mean-width": '+str(mean_width)+'}\r\n')

        self.capture_cnt += 1

def init_module(manager, gui):
    r = AutosaveSubwavelet(manager, 'subwavelet')
    return [r,]


