'''
Author: Dong Jiajun 2070928523@qq.com
Date: 2023-03-29 09:13:26
LastEditors: Dong Jiajun 2070928523@qq.com
LastEditTime: 2023-03-29 14:15:21
FilePath: \ColorTool\paint.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from PySide2.QtWidgets import QMainWindow, QApplication
from PySide2.QtGui import QPainter, QColor, QImage
import sys
import cv2
import numpy as np

class Example(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Drawing Rectangles')        
        self.show()
    
    def paintEvent(self, event):
        img = np.zeros((50, 100, 3), np.uint8)
        y,x = img.shape[:-1]
        colorlist = np.array([[255, 0, 0],[0, 0, 255]])
        color = (colorlist[0, 0], colorlist[0, 1], colorlist[0, 2]) # RGB
        color = tuple([int(x) for x in color])
        cv2.rectangle(img, (0, 0), (100,50), color, -1)
        block = QImage(img, x, y, x*3, QImage.Format_RGB888)
        block.save("color1.png")
        qp = QPainter(self)
        qp.drawImage(0,0,block)
        qp.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())