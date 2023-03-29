'''
Author: Dong Jiajun 2070928523@qq.com
Date: 2023-03-29 01:35:35
LastEditors: Dong Jiajun 2070928523@qq.com
LastEditTime: 2023-03-29 15:22:32
FilePath: \ColorTool\main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
'''
Author: Dong Jiajun 2070928523@qq.com
Date: 2023-03-28 18:57:58
LastEditors: Dong Jiajun 2070928523@qq.com
LastEditTime: 2023-03-29 15:02:37
FilePath: \ColorTool\main.py
'''
# This Python file uses the following encoding: utf-8
import sys

from PySide2.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsPixmapItem, QGraphicsItem
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QFileDialog
from PySide2.QtGui import QPixmap, QImage
from PySide2.QtGui import QPainter, QColor

from utils import ColorTool

import cv2
import numpy as np


class Window(QMainWindow):
    BLOCKS_X = 400
    BLOCKS_Y = 30
    BLOCK_H = 32
    BLOCK_W = 100
    BLOCK_D = 45 # 色块间距
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Color Tool')  
        self.setFixedSize(800, 600)
        qfile = QFile("newform.ui")
        qfile.open(QFile.ReadOnly)
        qfile.close()
        
        self.widget = QUiLoader().load(qfile)
        self.widget.setParent(self)
        self.scene = QGraphicsScene()
        self.widget.imgShow.setScene(self.scene)
        self.init_connect()
        
        self.path = None # 打开图片路径
        self.colortool = ColorTool()
        
        self.imgs = []
        
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
        # self.colortool.kmeanscore()
        self.refresh()
        self.list2imgs(self.colortool.color_list)
        
        # 保存测试
        # self.saveimgs()
        
        self.widget.update()
    
    # 更新绘制 文字
    def refresh(self):
        for i in range(self.colortool.color_list.shape[0]):
            # 填充一列色卡
            if self.colortool.color_type == 'RGB':
                pass
            elif self.colortool.color_type == '#hex':
                pass
            elif self.colortool.color_type == 'HSV':
                pass
          
    def paintEvent(self, event):
        qp = QPainter(self)
        for i in range(len(self.imgs)):
            block = QImage(self.imgs[i], self.BLOCK_W, self.BLOCK_H, self.BLOCK_W*3, QImage.Format_RGB888)
            qp.drawImage(self.BLOCKS_X, self.BLOCKS_Y+i*self.BLOCK_D, block)
            
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
        for i in range(len(self.imgs)):
            img = cv2.cvtColor(self.imgs[i], cv2.COLOR_RGB2BGR)
            cv2.imwrite("./imgs/"+str(i)+".png", img) # 只能写BGR格式
        pass


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication([])
    window = Window()
    window.show()
    
    sys.exit(app.exec_())
