'''
Author: Dong Jiajun 2070928523@qq.com
Date: 2023-03-28 18:57:58
LastEditors: Dong Jiajun 2070928523@qq.com
LastEditTime: 2023-03-29 00:52:16
FilePath: \ColorTool\main.py
'''
# This Python file uses the following encoding: utf-8
import sys

from PySide2.QtWidgets import QApplication, QGraphicsScene, QGraphicsPixmapItem, QGraphicsItem
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QFileDialog
from PySide2.QtGui import QPixmap, QImage

from utils import ColorTool

import cv2
import numpy as np


class Window:
    def __init__(self):
        qfile = QFile("form.ui")
        qfile.open(QFile.ReadOnly)
        qfile.close()
        
        self.widget = QUiLoader().load(qfile)
        
        self.scene = QGraphicsScene()
        self.widget.imgShow.setScene(self.scene)
        self.init_connect()
        
        self.path = None # 打开图片路径
        self.colortool = ColorTool()
        
    def init_connect(self):
        # 信号与槽函数连接
        self.widget.loadBtn.clicked.connect(self.loadimg) # 传入一个self
        self.widget.startBtn.clicked.connect(self.start)
        self.widget.colorNum.valueChanged.connect(self.colornumset)
        self.widget.colorType.currentTextChanged.connect(self.colortypeset)
    
    # 需传入的数据类型， k值和颜色类型  
    def colornumset(self,  num):
        self.colortool.color_num = num
        
    def colortypeset(self, type):
        self.colortool.color_type = type

    def loadimg(self):
        self.path, _ = QFileDialog.getOpenFileName(self.widget,'选择图片','.','图像文件(*.jpg *.png)')
        # self.colortool.ori_pic = cv2.imread(self.path)
        img = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), -1) # 兼容中文路径
        cvimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # 将opencv默认BGR转为RGB
        self.colortool.ori_pic = cvimg
        self.colortool.updatedata()
        
        y, x = cvimg.shape[:-1] # 图片尺寸
        frame = QImage(cvimg, x, y, x*3, QImage.Format_RGB888) # x*3防止倾斜
        self.scene.clear() # 清除scene残留
        pix = QPixmap.fromImage(frame)
        item = QGraphicsPixmapItem(QPixmap(pix))
        item.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)
        self.scene.addItem(item)
        # 让image填充显示窗口
        self.widget.imgShow.fitInView(item, Qt.KeepAspectRatio)
        
        
    def start(self):
        print("开始！")
    
    # 更新绘制
    def refresh(self):
        for i in range(self.colortool.color_list.shape[0]):
            # 填充一列色卡
            
            if self.colortool.color_type == 'RGB':
                pass
            elif self.colortool.color_type == '#hex':
                pass
            elif self.colortool.color_type == 'HSV':
                pass
        
        
        

if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication([])
    widget = Window()
    widget.widget.show()
    
    sys.exit(app.exec_())
