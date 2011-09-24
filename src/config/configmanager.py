'''
Created on Sep 17, 2011

@author: nEVSTER
'''

import os
from xml.etree import cElementTree
from config.metaclasses import codecMetaObject
    
class metaRepository:
    def __init__(self, filepath):
        self.filepath = filepath
        self.collection = {}
        self.createRepository()
        
    def allMetaObjects(self):
        for root, dirs, files in os.walk(self.filepath):
            for file in files:
                pathname = os.path.join(root, file)
                if 'xml' in pathname:
                    tree = cElementTree.ElementTree()
                    tree.parse(pathname)
                    for each in tree.findall('.//packet'):
                        yield codecMetaObject(each)
                        
    def createRepository(self):
        dupes = set()
        for cmo in self.allMetaObjects():
            t = cmo.getPacketName(), cmo.getPacketLength(), cmo.getPacketPattern()
            if t in dupes:
                raise IndexError('Duplicate metadata!!')
            dupes.add(t)
            self.collection[cmo.getPacketPattern()] = cmo
                        
    def getMetaObject(self, key):
        return self.collection.get(key)