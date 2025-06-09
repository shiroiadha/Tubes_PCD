import cv2
import sys
import numpy as np
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi

from utilitis.io import loadimg, saveimg, array2qimage
from utilitis.img_resizer import resize_with_aspect_ratio
from utilitis.grayscale import grayscaling
from utilitis.expression_detect import *

class ShowImage(QMainWindow):
    def __init__(self):
        super(ShowImage, self).__init__()
        loadUi('GUI.ui', self)
        self.centerWindow()
        self.Image = None
        self.Image2 = None
        self.Image3 = None

        # BASE FUNCTION MENU
        self.button_loadimg1.clicked.connect(self.loadF1)
        self.button_loadimg2.clicked.connect(self.loadF2)
        self.button_saveimg.clicked.connect(self.saveF)
        self.button_grayscale.clicked.connect(self.gs)
        self.button_clnW1.clicked.connect(self.clnw1)
        self.button_clnW2.clicked.connect(self.clnw2)
        self.button_clnW3.clicked.connect(self.clnw3)

        # EXPRESSION DETECTION
        self.button_dtctexprssion.clicked.connect(self.expression)

    def centerWindow(self):
        frameGm = self.frameGeometry()
        screen = QtWidgets.QApplication.primaryScreen().availableGeometry().center()
        frameGm.moveCenter(screen)
        self.move(frameGm.topLeft())

    # BASE FUNCTION'S FUNCTION
    def loadF1(self):
        image = loadimg(self)
        if image is not None:
            self.Image = image
            self.Image = resize_with_aspect_ratio(image, 720)
            self.displayImage(1)

    def loadF2(self):
        image = loadimg(self)
        if image is not None:
            self.Image2 = resize_with_aspect_ratio(image, 720)
            self.displayImage(2)

    def saveF(self):
        saveimg(self, self.Image3)

    def gs(self):
        if self.Image is not None:
            try:
                self.Image = grayscaling(self.Image)
            except:
                pass
            self.displayImage(1)
        if self.Image2 is not None:
            try:
                self.Image2 = grayscaling(self.Image2)
            except:
                pass
            self.displayImage(2)

    def clnw1(self):
        self.displayImage(1, True)
        self.Image = None

    def clnw2(self):
        self.displayImage(2, True)
        self.Image2 = None

    def clnw3(self):
        self.displayImage(3, True)
        self.Image3 = None

    def expression(self):
        self.Image3 = detect_expression(1)
        self.displayImage(3)

    def displayImage(self, windows=1, clear=False):
        qformat = QImage.Format_Indexed8

        if clear:
            if windows == 1:
                self.label_window1.clear()
            elif windows == 2:
                self.label_window2.clear()
            elif windows == 3:
                self.label_window3.clear()
            return

        # Pilih image sesuai window
        if windows == 1:
            img_data = self.Image
        elif windows == 2:
            img_data = self.Image2
        elif windows == 3:
            img_data = self.Image3
        else:
            return

        if img_data is None:
            return

        # Pastikan img_data adalah numpy.ndarray sebelum memeriksa shape
        if isinstance(img_data, np.ndarray):
            if len(img_data.shape) == 3:
                if img_data.shape[2] == 4:
                    qformat = QImage.Format_RGBA8888
                else:
                    qformat = QImage.Format_RGB888
        elif isinstance(img_data, QImage):
            # Kalau img_data sudah QImage, langsung konversi formatnya
            qformat = QImage.Format_RGB888

        # Jika img_data adalah numpy.ndarray, konversi ke QImage
        if isinstance(img_data, np.ndarray):
            img = QImage(img_data.data, img_data.shape[1], img_data.shape[0], img_data.strides[0], qformat)
            img = img.rgbSwapped()
        else:
            img = img_data  # Jika sudah QImage, tidak perlu konversi lagi

        pixmap = QPixmap.fromImage(img)
        scaled_pixmap1 = pixmap.scaled(self.label_window1.size(), QtCore.Qt.KeepAspectRatio,
                                       QtCore.Qt.SmoothTransformation)
        scaled_pixmap2 = pixmap.scaled(self.label_window2.size(), QtCore.Qt.KeepAspectRatio,
                                       QtCore.Qt.SmoothTransformation)
        scaled_pixmap3 = pixmap.scaled(self.label_window3.size(), QtCore.Qt.KeepAspectRatio,
                                       QtCore.Qt.SmoothTransformation)

        if windows == 1:
            self.label_window1.setPixmap(scaled_pixmap1)
            self.label_window1.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        elif windows == 2:
            self.label_window2.setPixmap(scaled_pixmap2)
            self.label_window2.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        elif windows == 3:
            self.label_window3.setPixmap(scaled_pixmap3)
            self.label_window3.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

app = QtWidgets.QApplication(sys.argv)
window = ShowImage()
window.setWindowTitle('DIGITAL IMAGE PROCESSING')
window.show()
sys.exit(app.exec())