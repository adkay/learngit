# -*- coding: utf-8 -*-
'''
Created on 2015年2月24日

@author: kay
'''
from PyQt4.QtCore import QObject, SIGNAL
#global qtob


#def printf_init():
qtob=QObject()

def sprint(data):
    qtob.emit(SIGNAL("sprintf"), qtob.tr(data))