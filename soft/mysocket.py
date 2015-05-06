# -*- coding: utf-8 -*-
'''
Created on 2015年2月2日

@author: kay
'''
import socket, threading,time,re
from PyQt4.QtCore import QObject, SIGNAL
from PyQt4 import QtCore
from conmysql import ConMysql
import sprint
class Mysocket(QtCore.QThread):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        QtCore.QThread.__init__(self)
        self.qtobj=QObject()
        self.mysql=ConMysql()
        self.mysql.setting('localhost', 'root', '443622796', 3306, 'utf8')
        self.mysql.open()
        self.mysql.start()
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.s.bind(('192.168.1.107', 8899))
        self.s.bind(('192.168.0.199', 8899))
        #self.s.bind((socket.gethostbyname(socket.gethostname()), 8899))
        self.s.listen(5)
        
    def run(self):
        sprint.sprint('程序开始运行，等待连接...')
        while True:
            
            #print "current has %d threads" % (threading.activeCount())
            #for item in threading.enumerate():
            #    print item
            
            self.sock, self.addr =self.s.accept()   
            
            self.t =tcplink(self.sock,self.addr,self.mysql)
            
            self.t.start()
            self.qtobj.emit(SIGNAL("NewData"), self.t)
    
class tcplink(QtCore.QThread):
    def __init__(self,sock,addr,mysql):
        QtCore.QThread.__init__(self)
        self.qtobj=QObject()
        self.name="tcplink"
        self.sock=sock
        self.addr=addr
        self.mysql=mysql
    def run(self):
        sprint.sprint('Accept new connection from %s:%s...'% self.addr)
        
        while True:
            self.data = self.sock.recv(1024)
            if not self.data:
                break
            elif self.data[0]=='~':
                if self.data[2]=='1':
                    if self.data[4]=='1':     #   ~0101
                        self.Read_Time()      
                    elif self.data[4]=='2':   #   ~0102
                        self.read_tongji(self.data)
                        pass
                elif self.data[2]=='2':
                    if self.data[4]=='1':
                        self.Read_WMTechnology() #读取全部打包工艺条目 ~0201
                    elif self.data[4]=='2':
                        self.Read_WMId(self.data) #按ID号读取打包工艺条目 ~0202
                elif self.data[2]=='3':
                    if self.data[4]=='1':
                        self.write_sql(self.data)   #   ~0301
                    elif self.data[4]=='2':   #   ~0302
                        self.sock.send('~0302')
                        self.sock.send(str(self.read_maxnum()))
                        self.sock.send('#')
                    elif self.data[4]=='3':    #    ~0303
                        self.read_thelast()
                        
                    elif self.data[4]=='4':    #    ~0304
                        if self.data[9]=='#':
                            self.delete_(self.data)     
                            pass
            sprint.sprint(self.data)
            #self.qtobj.emit(SIGNAL("NewData1"), self.data)
        self.sock.close()
    def delete_(self,data):
        try:
            self.mysql.select_db('information_wms')
            self.mysql.execute("select max(序号) from all_data")
            rows = self.mysql.fetchall()
            self.mysql.execute("delete from all_data where 序号="+str(rows[0][0]))
            self.mysql.commit()
            self.mysql.select_db('information_technology')
            self.mysql.execute("update wm set 当日包数=当日包数-1 where ID="+data[5]+data[6]+data[7]+data[8])
            self.mysql.commit()
            self.mysql.execute("update wm set 总包数=总包数-1 where ID="+data[5]+data[6]+data[7]+data[8])
            self.mysql.commit()
            self.mysql.select_db('information_sys')
            self.mysql.execute("update sys set 当日总包数=当日总包数-1")
            self.mysql.commit()
            self.mysql.execute("update sys set 历史总包数=历史总包数-1")
            self.mysql.commit()
            
        except self.mysql.MySQLdb.Error,e:
            print "My Error %d: %s" % (e.args[0], e.args[1])    
        
    def read_thelast(self):
        try:
            self.mysql.select_db('information_wms')
            self.mysql.execute("select max(序号) from all_data")
            rows = self.mysql.fetchall()
            #print rows
            self.mysql.execute("select * from all_data where 序号="+str(rows[0][0]))
            rows = self.mysql.fetchall()
            print rows
            data='~0303ID:    '+str(rows[0][0])+' '+str(rows[0][1])+' '+str(rows[0][3])+'\r\nNUM:   '+str(rows[0][4])+'\r\nTIME:  '+str(rows[0][5])+'#'
            self.sock.send(data)
            #print data
        except :
            pass
    def read_tongji(self,data): #~03051022#
        try:
            self.mysql.select_db('information_technology')
            self.mysql.execute("select 当日包数 from wm where ID="+data[5]+data[6]+data[7]+data[8])
            rows1 = self.mysql.fetchall()
            self.mysql.select_db('information_sys')
            self.mysql.execute("select 当日总包数 from sys")
            rows2 = self.mysql.fetchall()
            self.sock.send("~0102*"+str(rows1[0][0])+'*'+str(rows2[0][0])+'#')
            
        except :
            pass
    def read_maxnum(self):
        try:
            self.mysql.select_db('information_wms')
            self.mysql.execute("select max(序号) from all_data")
            rows =self.mysql.fetchall()
            return rows[0][0]+1
        except :
            pass
    def write_sql(self,data):
        exp=re.compile('(?isu)\*([^\*]+)')
        res=exp.findall(data)
        sprint.sprint('接收到数据 ：%s'%res)
        sprint.sprint('等待下一个数据')
        a=res[0]
        b=res[1]
        c=res[2]
        d=str(res[3])
        e=str(time.strftime("%Y%m%d%H%M%S",time.localtime(time.time())))
    
        try:
            self.mysql.select_db('information_wms')
            self.mysql.execute("select max(序号) from all_data")
            rows = self.mysql.fetchall()
            self.mysql.execute(("INSERT INTO all_data(序号,批号ID,毛重,净重,条码号,生产时间)VALUES("+str(rows[0][0]+1)+","+a+","+b+","+c+","+"\'"+d+"\'"+","+e+")"))
            self.mysql.commit()
            self.mysql.select_db('information_technology')
            self.mysql.execute("update wm set 当日包数=当日包数+1 where ID="+a)
            self.mysql.commit()
            self.mysql.execute("update wm set 总包数=总包数+1 where ID="+a)
            self.mysql.commit()
            self.mysql.select_db('information_sys')
            self.mysql.execute("update sys set 当日总包数=当日总包数+1")
            self.mysql.commit()
            self.mysql.execute("update sys set 历史总包数=历史总包数+1")
            self.mysql.commit()
        except :
            pass
    def Read_Time(self):
        self.sock.send('~0101*')
        self.sock.send(str(time.strftime("%y%m%d%H%M%S",time.localtime(time.time()))))
        self.sock.send('#')
        self.sprint(time.strftime("%y%m%d%H%M%S",time.localtime(time.time())))
    def Read_WMId(self,ID):
        exp=re.compile('(?isu)\*([^\*]+)')
        res=exp.findall(ID)
        try:
            self.mysql.select_db('information_technology')
            self.mysql.execute("select ID,批号,规格,纱色,管色,品名,等级 from wm where ID="+str(res[0]))
            rows = self.mysql.fetchall()
            self.sock.send('~0202*')
            self.sock.send(str(rows[0][0]))
            self.sock.send('*')
            self.sock.send(rows[0][1].encode('gb2312'))
            self.sock.send('*')
            self.sock.send(rows[0][2].encode('gb2312'))
            self.sock.send('*')
            self.sock.send(rows[0][3].encode('gb2312'))
            self.sock.send('*')
            self.sock.send(rows[0][4].encode('gb2312'))
            self.sock.send('*')
            self.sock.send(rows[0][5].encode('gb2312'))
            self.sock.send('*')
            self.sock.send(rows[0][6].encode('gb2312'))
            self.sock.send('*')
            self.sock.send('#')
            self.mysql.commit()
        except:
            pass
    def Read_WMTechnology(self):
        try:
            self.mysql.select_db('information_technology')
            self.mysql.execute('select * from wm')
            results=self.mysql.fetchall()
            self.sock.send('~0201')
            for row in results:
                self.sock.send('*')
                for row1 in range(0,7):
                    xy=row[row1]
                    if row1==0:
                        self.sock.send(str(xy))
                        self.sock.send(' ')
                    else:
                        self.sock.send(xy.encode('gb2312'))
                        self.sock.send(' ')
                self.sock.send('\r\n')
            self.sock.send('#')
        except:
            pass
    def send(self,data):
        print 'good'
        self.data=data
        
        self.sock.send(self.data)