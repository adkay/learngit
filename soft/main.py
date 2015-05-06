# -*- coding: utf-8 -*-
'''
Created on 2015年2月2日

@author: kay
'''
from mysocket import Mysocket
from PyQt4 import QtGui, QtCore
from myui import MyUi
import sys



if __name__=="__main__":
    app=QtGui.QApplication(sys.argv)
    myui=MyUi()
    myui.show()
    sys.exit(app.exec_())