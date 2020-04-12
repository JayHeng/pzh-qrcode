#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import os
import time
from PyQt5.Qt import *
from qrcodeWin import *
from MyQR import myqr
from zxing import *

kGeneratorType_MyQR = 'MyQR'
kGeneratorType_pzh  = 'pzh'

kDetectorType_zxing = 'zxing'
kDetectorType_pzh   = 'pzh'

kImageSource_Camera  = 'Camera'
kImageSource_Picture = 'Picture'

class qrcodeMain(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(qrcodeMain, self).__init__(parent)
        self.setupUi(self)
        self._show_image(u"../img/default_bg.png")
        self._register_callbacks()
        self.destPicture = None
        self.srcPicture = None

    def _register_callbacks(self):
        self.pushButton_selectDestPicturePath.clicked.connect(self.callbackDoSelectDestPicturePath)
        self.pushButton_generate.clicked.connect(self.callbackDoGenerate)
        self.pushButton_selectSrcPicture.clicked.connect(self.callbackDoSelectSrcPicture)
        self.pushButton_detect.clicked.connect(self.callbackDoDetect)

    def _show_image(self, picFile):
        picObj = QtGui.QPixmap(picFile).scaled(self.label_showImage.width(), self.label_showImage.height())
        self.label_showImage.setPixmap(picObj)

    def _get_generation_info(self):
        self.generatorType = self.comboBox_generatorType.currentText()
        # Set version to 0 for Auto mode
        if self.comboBox_symbolVersion.currentText() == 'Auto':
            self.symbolVersion = 0
        else:
            self.symbolVersion = int(self.comboBox_symbolVersion.currentText())
        eccLevel = self.comboBox_eccLevel.currentText()
        self.eccLevel = eccLevel[0]
        picName = self.lineEdit_destPictureName.text()
        if self.destPicture != None and picName != '':
            # If self.destPicture is file, we should set it back to path
            if os.path.isfile(self.destPicture):
                self.destPicture, dummyName = os.path.split(self.destPicture)
            # Attach new file name and type to self.destPicture
            picType = self.comboBox_destPictureType.currentText()
            self.destPicture = os.path.join(self.destPicture, picName + picType)
        else:
            # Use same default file as MyQR
            self.destPicture = os.path.join(os.getcwd(), 'qrcode.png')
        self.encodeWords = self.lineEdit_encodeWords.text()
        # If there is no words, return false
        return (self.encodeWords != '')

    def callbackDoSelectDestPicturePath(self):
        self.destPicture = QtWidgets.QFileDialog.getExistingDirectory(self, u"Browse Folder", os.getcwd())
        self.lineEdit_destPicturePath.setText(self.destPicture)

    def callbackDoGenerate(self):
        if not self._get_generation_info():
            QMessageBox.about(self, u"Info", u"Please input encode words first! " )
            return
        if self.generatorType == kGeneratorType_MyQR:
            picPath, picName = os.path.split(self.destPicture)
            # Just set symbolVersion to 1 for Auto mode, MyQR will adjust version automatically
            symbolVersion = self.symbolVersion
            if self.symbolVersion == 0:
                symbolVersion = 1
            # Run MyQR
            version, level, qr_name = myqr.run(self.encodeWords,
                                               version=symbolVersion,
                                               level=self.eccLevel,
                                               picture=None,
                                               colorized=False,
                                               contrast=1.0,
                                               brightness=1.0,
                                               save_name=picName,
                                               save_dir=picPath
                                               )
            self._show_image(qr_name)
        elif self.generatorType == kGeneratorType_pzh:
            pass
        else:
            pass

    def _get_detection_info(self):
        self.detectorType = self.comboBox_detectorType.currentText()
        self.imageSource = self.comboBox_imageSource.currentText()
        if self.imageSource == kImageSource_Picture:
            if self.srcPicture == None:
                self.srcPicture = self.destPicture
            return os.path.isfile(self.srcPicture)
        elif self.imageSource == kImageSource_Camera:
            return False
        else:
            pass

    def callbackDoSelectSrcPicture(self):
        self.srcPicture, dummyType = QtWidgets.QFileDialog.getOpenFileName(self, u"Browse File", os.getcwd(), "All Files(*);;Source Files(*.png)")
        self.lineEdit_srcPicture.setText(self.srcPicture)

    def callbackDoDetect(self):
        if not self._get_detection_info():
            return
        if self.detectorType == kDetectorType_zxing:
            # Have to add prefix 'file:/' to the real pictrue path, this is requirement from zxing'
            srcPicture = 'file:/' + self.srcPicture
            srcPicture = srcPicture.replace("\\", '/')
            zx = BarCodeReader()
            barcode = zx.decode(srcPicture)
            self.lineEdit_decodedWords.setText(barcode.data)
        elif self.detectorType == kDetectorType_pzh:
            pass
        else:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = qrcodeMain()
    main_win.setWindowTitle(u"pzh-qrcode v1.0")
    main_win.show()
    sys.exit(app.exec_())


