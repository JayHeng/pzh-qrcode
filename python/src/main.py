#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import os
import time
from PyQt5.Qt import *
from qrcodeWin import *

class qrcodeMain(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(qrcodeMain, self).__init__(parent)
        self.setupUi(self)
        self._show_default_picture()
        self._register_callbacks()

    def _register_callbacks(self):
        pass

    def _show_default_picture(self):
        imgName = u"../img/default_bg.png"
        picObj = QtGui.QPixmap(imgName).scaled(self.label_showImage.width(), self.label_showImage.height())
        self.label_showImage.setPixmap(picObj)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = qrcodeMain()
    main_win.setWindowTitle(u"pzh-qrcode v1.0")
    main_win.show()
    sys.exit(app.exec_())


