# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_mainwindow(object):
    def setupUi(self, mainwindow):
        if not mainwindow.objectName():
            mainwindow.setObjectName(u"mainwindow")
        mainwindow.setEnabled(True)
        mainwindow.resize(726, 571)
        mainwindow.setMinimumSize(QSize(726, 0))
        mainwindow.setMaximumSize(QSize(726, 578))
        self.centralwidget = QWidget(mainwindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget_7 = QWidget(self.centralwidget)
        self.widget_7.setObjectName(u"widget_7")
        self.widget_7.setGeometry(QRect(11, 11, 321, 499))
        self.widget = QWidget(self.widget_7)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(10, 350, 300, 131))
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.widget_2)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.colorNum = QSpinBox(self.widget_2)
        self.colorNum.setObjectName(u"colorNum")
        self.colorNum.setMinimumSize(QSize(44, 0))
        self.colorNum.setMaximum(20)

        self.horizontalLayout.addWidget(self.colorNum)


        self.gridLayout.addWidget(self.widget_2, 0, 0, 1, 1)

        self.widget_3 = QWidget(self.widget)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.loadBtn = QPushButton(self.widget_3)
        self.loadBtn.setObjectName(u"loadBtn")

        self.horizontalLayout_3.addWidget(self.loadBtn)


        self.gridLayout.addWidget(self.widget_3, 0, 1, 1, 1)

        self.widget_5 = QWidget(self.widget)
        self.widget_5.setObjectName(u"widget_5")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.widget_5)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.colorType = QComboBox(self.widget_5)
        self.colorType.addItem("")
        self.colorType.addItem("")
        self.colorType.addItem("")
        self.colorType.setObjectName(u"colorType")

        self.horizontalLayout_2.addWidget(self.colorType)


        self.gridLayout.addWidget(self.widget_5, 1, 0, 1, 1)

        self.widget_4 = QWidget(self.widget)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.startBtn = QPushButton(self.widget_4)
        self.startBtn.setObjectName(u"startBtn")

        self.horizontalLayout_4.addWidget(self.startBtn)


        self.gridLayout.addWidget(self.widget_4, 1, 1, 1, 1)

        self.imgShow = QGraphicsView(self.widget_7)
        self.imgShow.setObjectName(u"imgShow")
        self.imgShow.setGeometry(QRect(10, 10, 301, 331))
        self.widget_8 = QWidget(self.centralwidget)
        self.widget_8.setObjectName(u"widget_8")
        self.widget_8.setGeometry(QRect(350, 10, 161, 501))
        mainwindow.setCentralWidget(self.centralwidget)
        self.widget_8.raise_()
        self.widget_7.raise_()
        self.menubar = QMenuBar(mainwindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 726, 26))
        mainwindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(mainwindow)
        self.statusbar.setObjectName(u"statusbar")
        mainwindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainwindow)

        QMetaObject.connectSlotsByName(mainwindow)
    # setupUi

    def retranslateUi(self, mainwindow):
        mainwindow.setWindowTitle(QCoreApplication.translate("mainwindow", u"ColorTool", None))
        self.label.setText(QCoreApplication.translate("mainwindow", u"\u989c\u8272\u6570\u91cf", None))
        self.loadBtn.setText(QCoreApplication.translate("mainwindow", u"\u6253\u5f00", None))
        self.label_2.setText(QCoreApplication.translate("mainwindow", u"\u989c\u8272\u6a21\u5f0f", None))
        self.colorType.setItemText(0, QCoreApplication.translate("mainwindow", u"RGB", None))
        self.colorType.setItemText(1, QCoreApplication.translate("mainwindow", u"#hex", None))
        self.colorType.setItemText(2, QCoreApplication.translate("mainwindow", u"HSV", None))

        self.startBtn.setText(QCoreApplication.translate("mainwindow", u"\u5f00\u59cb", None))
    # retranslateUi

