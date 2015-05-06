# -*- coding: utf-8 -*-
'''
Created on 2015年2月11日

@author: kay
'''
import psutil
from mysocket import Mysocket
from PyQt4 import QtGui, QtCore
import sprint
import sys
from telnetlib import theNULL
QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName("utf8"))
class MyUi(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MyUi,self).__init__(parent)
        self.num=0
        self.connect(sprint.qtob,QtCore.SIGNAL("sprintf"),self.showMsg)
        self.mysocket=Mysocket()
        self.mysocket.start()
        
        #t=self.mysocket.res()
        #print t.getName()
        self.setWindowTitle(self.tr('服务端程序..'))
        self.resize(300,200)
        self.text=QtGui.QTextEdit(self)
        self.text.resize(300,200)
        self.text.setReadOnly(True)
        #self.connect(self.mysocket.qtobj,QtCore.SIGNAL("NewData()"),self.shownum)
        self.connect(self.mysocket.qtobj,QtCore.SIGNAL("NewData"),self.Newconn)
        
    def Newconn(self,t):
        #self.text.setText(data)
        self.t=t
        self.connect(self.t.qtobj,QtCore.SIGNAL("NewData1"),self.showMsg)
        self.connect(self.t.qtobj,QtCore.SIGNAL("sprintmesg"),self.showMsg)

    def showMsg(self,data):
        #QtGui.QMessageBox.information(self, u"信息", u"ok")
        
        if self.num>=100:
            self.num=0
            self.text.setText('')
        self.text.append(data)
        self.num=self.num+1
    def closeEvent(self, event):
        self.reply = QtGui.QMessageBox.question(self, 'Message',
        "Are you sure to quit?", QtGui.QMessageBox.Yes,
        QtGui.QMessageBox.No)
        if self.reply == QtGui.QMessageBox.Yes:
            
            event.accept()
        else:
            event.ignore()
