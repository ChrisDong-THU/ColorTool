'''
Author: Dong Jiajun 2070928523@qq.com
Date: 2023-03-29 01:35:35
LastEditors: Dong Jiajun 2070928523@qq.com
LastEditTime: 2023-03-30 02:54:49
FilePath: \ColorTool\main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
# This Python file uses the following encoding: utf-8
import sys

from PySide2.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsPixmapItem, QGraphicsItem
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QFileDialog
from PySide2.QtGui import QPixmap, QImage, QIcon
from PySide2.QtGui import QPainter

from utils import ColorTool

import cv2
import numpy as np
import os

class Window(QMainWindow):
    BLOCKS_X = 520
    BLOCKS_Y = 30
    BLOCK_H = 36
    BLOCK_W = 100
    BLOCK_VD = 152 # 色块水平方向间距
    BLOCK_HD = BLOCK_H+10 # 色块竖直方向间距
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Color Tool for XiaoW')  
        self.setFixedSize(804, 520)
        self.setWindowIcon(QIcon("./icons/logo.png"))
        qfile = QFile("newform.ui")
        qfile.open(QFile.ReadOnly)
        qfile.close()
        
        self.widget = QUiLoader().load(qfile)
        self.widget.setParent(self)
        self.dialog = QUiLoader(self).load("./dialog.ui")
        self.dialog.setFixedSize(280, 250)
        self.scene = QGraphicsScene()
        self.widget.imgShow.setScene(self.scene)
        
        self.path = None # 打开图片路径
        self.colortool = ColorTool()
        
        self.imgs = []
        self.blockspos = [] # 色块位置序列
        self.editreal = [36, 100, 1] # 自定义输出参数(真实)h, w, span
        self.edittmp = [36, 100, 1] # 自定义更改暂存区h, w, span
        
        self.inituipos()
        self.init_connect()
        
    def inituipos(self):
        for i in range(20):
            if i<10:
                self.blockspos.append((self.BLOCKS_X, self.BLOCKS_Y+i*self.BLOCK_HD))
            else:
                self.blockspos.append((self.BLOCKS_X+self.BLOCK_VD, self.BLOCKS_Y+(i-10)*self.BLOCK_HD))
                
        
    def init_connect(self):
        # 信号与槽函数连接
        self.widget.loadBtn.clicked.connect(self.loadimg) # 传入一个self
        self.widget.startBtn.clicked.connect(self.start)
        self.widget.saveBtn.clicked.connect(self.saveimgs)
        self.widget.editBtn.clicked.connect(self.edit)
        self.widget.colorNum.valueChanged.connect(self.colornumset)
        self.widget.colorType.currentTextChanged.connect(self.sorttypeset)
        
        self.dialog.buttonBox.accepted.connect(self.editset)
        self.dialog.buttonBox.rejected.connect(self.reeditset)
        self.dialog.hBox.valueChanged.connect(self.outputh)
        self.dialog.wBox.valueChanged.connect(self.outputw)
        self.dialog.spanBox.valueChanged.connect(self.outputspan)
    
    # 需传入的数据类型， k值和颜色类型  
    def colornumset(self,  num):
        self.colortool.color_num = num
        
    def sorttypeset(self, type):
        if type == '亮度':
            t = 1
        elif type == '权重':
            t = 2
        elif type == '平均':
            t = 3

        self.colortool.sort_type = t

    def loadimg(self):
        self.path, _ = QFileDialog.getOpenFileName(self.widget,'选择图片','.','图像文件(*.jpg *.png)')
        # self.colortool.ori_pic = cv2.imread(self.path)
        img = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), -1) # 兼容中文路径
        cvimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # 将opencv默认BGR转为RGB
        self.colortool.ori_pic = cvimg
        
        y, x = cvimg.shape[:-1] # 图片尺寸
        frame = QImage(cvimg, x, y, x*3, QImage.Format_RGB888) # x*3防止倾斜
        self.scene.clear() # 清除scene残留
        pix = QPixmap.fromImage(frame)
        item = QGraphicsPixmapItem(QPixmap(pix))
        # item.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)
        self.scene.addItem(item)
        # 让image填充显示窗口
        self.widget.imgShow.fitInView(item, Qt.KeepAspectRatio)
        
    def start(self):
        self.colortool.kmeanscore()
        self.list2imgs(self.colortool.color_list)
        
        self.widget.update()
          
    def paintEvent(self, event):
        for i in range(len(self.imgs)):
            qp = QPainter(self)
            block = QImage(self.imgs[i], self.BLOCK_W, self.BLOCK_H, self.BLOCK_W*3, QImage.Format_RGB888)
            qp.drawImage(self.blockspos[i][0], self.blockspos[i][1], block)
            qp.end()

    def list2imgs(self, colorlist):
        '''色彩列表转图像对象

        Args:
            colorlist (ndarray): rgb color list
        '''
        self.imgs.clear()
        for i in range(colorlist.shape[0]):
             img = np.zeros((self.BLOCK_H, self.BLOCK_W, 3), np.uint8)
             color = colorlist[i]
             color = tuple([int(x) for x in color]) # 转int元组防报错
             cv2.rectangle(img, (0,0), (self.BLOCK_W, self.BLOCK_H), color, -1) # RGB格式
            # block此处不合适，改到paintEvent中
             self.imgs.append(img)
             
    def saveimgs(self):
        path = "./imgs"
        ls = os.listdir(path)
        for k in ls:
            cpath = os.path.join(path, k)
            os.remove(cpath)
        
        # TODO: 将图片连成一排打印出来，格式可自定义
        colorlist = self.colortool.color_list
        [h, w, span] = self.editreal
        singleimg = np.zeros((h, w, 3), np.uint8)
        spanimg = np.full((h, span, 3), fill_value=255,dtype=np.uint8)
        
        for i in range(colorlist.shape[0]):
            color = colorlist[i]
            color = tuple([int(x) for x in color]) # 转int元组防报错
            cv2.rectangle(singleimg, (0,0), (w, h), color, -1)
            singleimg = cv2.cvtColor(singleimg, cv2.COLOR_RGB2BGR)
            name = 'rgb_'+str(self.colortool.color_list[i][0]) + '_'\
                + str(self.colortool.color_list[i][1]) + '_'\
                    + str(self.colortool.color_list[i][2])
            cv2.imwrite("./imgs/"+name+".png", singleimg) # 只能写BGR格式
            
            if i==0:
                totalimg = singleimg
                totalimg = np.hstack((totalimg, spanimg))
                continue
            totalimg = np.hstack((totalimg, singleimg))
            
            if i==colorlist.shape[0]-1:
                continue
            totalimg = np.hstack((totalimg, spanimg))

        cv2.imwrite("./imgs/atla.png", totalimg)
                
        
    
    def edit(self):
        self.dialog.exec_()
       
    def editset(self):
        for i in range(3):
            self.editreal[i] = self.edittmp[i]
    
    def reeditset(self):
        for i in range(3):
            self.edittmp[i] = self.editreal[i]
            
        self.dialog.hBox.setValue(self.edittmp[0])
        self.dialog.wBox.setValue(self.edittmp[1])
        self.dialog.spanBox.setValue(self.edittmp[2])
    
    def outputh(self, h):
        self.edittmp[0] = h
    
    def outputw(self, w):
        self.edittmp[1] = w
    
    def outputspan(self, span):
        self.edittmp[2] = span

if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication([])
    window = Window()
    window.show()
    
    sys.exit(app.exec_())
