# -*- coding: utf-8 -*-
'''
Created on 2015年2月19日

@author: kay
'''
import MySQLdb,threading,time
import sprint
from PyQt4 import QtCore
class ConMysql(QtCore.QThread):
    def __init__(self, parent = None):
        QtCore.QThread.__init__(self)
        self.tip=False
        self.con=False
    def run(self):
        while True:
            if self.con:
                time.sleep(1) 
                try:
                    self.conn.select_db('information_sys')
                except :
                    self.tip=False
                    self.con=False
                    #print( u'连接出错')
                    #sprint.sprint('连接出错')
                    self.conn.close()
                else:
                    self.tip=True
                    #print ( u'连接成功')
                    #sprint.sprint ('连接成功')
            else:
                self.open()
            if self.tip:
                pass
    def setting(self,host,user,passwd,port,charset):
        self.Host=host
        self.User=user
        self.Passwd=passwd
        self.Port=port
        self.Charset=charset
    def open(self):
        while True:
            try:
                self.conn=MySQLdb.connect(host=self.Host,user=self.User,passwd=self.Passwd,port=self.Port,charset=self.Charset)
                self.cur=self.conn.cursor()
                
            except MySQLdb.Error,e:
                print "MySQL Error %d: %s" % (e.args[0], e.args[1])
                if e.args[0]==2003:
                    sprint.sprint( '数据库连接错误')
                    #print( u'数据库连接错误')
                self.con=False
                
            else:
                self.con=True
            break
    def fetchall(self):
        return self.cur.fetchall()
    def select_db(self,dbname):
        self.conn.select_db(dbname)
    def execute(self,strs):
        self.cur.execute(strs)
    def commit(self):
        self.conn.commit()
    def close(self):
        self.conn.close()

