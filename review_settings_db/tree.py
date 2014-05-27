#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, localdb
import os.path

file_list = []
tree_dict = {}
stage_name = 'name'
folder_name = 't'
ts_elements = {}    #{pos number:element ts}
tree_pos = {}   #{addr: pos number(global_addr)}
root_dir = ''

def buildTree(self, rootdir):
    global file_list, tree_dict, root_dir
    root_dir = rootdir
    file_list = []
    tree_dict = {}
    '''Add a new root element and then its children'''
    self.rootID = self.tree_db.AddRoot(rootdir.split('/')[-1])
    self.tree_db.SetPyData(self.rootID, (rootdir,1))
    self.tree_db.SetItemBold(self.rootID)

    extendTree(self, self.rootID, self.tree_db.GetPyData(self.rootID)[0])
    return file_list, tree_dict 

def list_create(path):
    def myKeyFunc(aString):
        aString = aString.split('_')[-1]
        try:
            result = int(filter(str.isdigit, aString))    #sort by number in name
        except: result = sys.maxint
        return result
    dirs_list = []      #list of directories "*/"
    #print 'path: ', path    #append file in list 
    dirs_list.extend(localdb.db.list_subnodes(path))
    dirs_list.sort(key = myKeyFunc)
    return dirs_list

def extendTree(self, parentID, parentDir):
    global files_list, dirs_list, tree_dict, file_list
    '''extendTree is a semi-lazy directory tree builder. It takes
    the ID of a tree entry and fills in the tree with its child
    subdirectories and their children - updating 2 layers of the
    tree. This function is called by buildTree and onExpand methods'''

    # retrieve the associated absolute path of the parent
    dirs_list = list_create(parentDir)

    for child in dirs_list:
        child_path = parentDir + '/' + child
        #print 'CHILD', child_path, child
        if localdb.db.list_subnodes(child_path):   #if path is dir 
            childID = self.tree_db.AppendItem(parentID, child_path)
            self.tree_db.SetItemBold(childID)
            self.tree_db.SetPyData(childID, (child_path, False))
            if localdb.db.read_persistance(child_path) == 0:
                self.tree_db.SetItemTextColour(childID, 'red')
            elif localdb.db.read_persistance(child_path) == 1:
                self.tree_db.SetItemTextColour(childID, 'green')
            elif localdb.db.read_persistance(child_path) == 2:
                self.tree_db.SetItemTextColour(childID, 'blue')
            extendTree(self, childID, child_path)
        else:
            # add the child to the parent
            childID = self.tree_db.AppendItem(parentID, child_path) 
            tree_dict[child_path] = parentID
            file_list.append(child_path)
            self.tree_db.SetItemBold(childID)
            #self.tree_db.SetItemTextColour(childID, 'green')
            self.tree_db.SetPyData(childID, (child_path, False))
