import cv2
import sys
import numpy as np
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi
from Tools.scripts.dutree import display

from utilitis.img_processing import *
from utilitis.io import *
from utilitis.img_resizer import *
from utilitis.expression_detect import *

class ShowImage(QMainWindow):
    def __init__(self):
        super(ShowImage, self).__init__()
        loadUi('GUI.ui', self)
        self.centerWindow()
        self.Image1 = None
        self.Image2 = None
        self.Image3 = None
        self.Image4 = None
        self.Image5 = None
        self.Image6 = None
        self.Image7 = None

        # BASE FUNCTION MENU
        self.button_loadimg.clicked.connect(self.loadimg)
        self.button_resetimg.clicked.connect(self.resetimg)
        self.button_saveimg.clicked.connect(self.saveimg)
        self.button_processimg.clicked.connect(self.processimg)

    def centerWindow(self):
        frameGm = self.frameGeometry()
        screen = QtWidgets.QApplication.primaryScreen().availableGeometry().center()
        frameGm.moveCenter(screen)
        self.move(frameGm.topLeft())

    def loadimg(self):
        image = loadimg(self)
        if image is not None:
            self.Image1 = resize_with_aspect_ratio(image, 512)
            # self.Image1 = image
            self.displayImage(1)

    def resetimg(self):
        for i in range(7):
            self.displayImage(i + 1, True)
            setattr(self, f'Image{i}', None)

    def saveimg(self):
        saveimg(self, self.Image7)

    # MWEHEHEHEHE!!!!
    def processimg(self):
        image = self.Image1 # Entering image input from Image1 to variable image

        # Grayscaling image
        self.Image2 = grayscaling(image)
        image = self.Image2 # Re-entering the previous output
        self.displayImage(2)

        # Image Smoothing with Gaussian Kernel
        self.Image3 = gaussian(image)
        image = self.Image3  # Re-entering the previous output
        self.displayImage(3)

        # Edge Detection with Canny Edge Detection
        self.Image4 = canny(image, 30, 80)
        image = self.Image4  # Re-entering the previous output
        self.displayImage(4)

        # Morphing image with Closing Method (Dilation => Erosion)
        self.Image5 = closing(image, 7)
        image = self.Image5  # Re-entering the previous output
        self.displayImage(5)

        # Marking and giving contours for each detected object
        self.Image6 = makecontours(image)
        image = self.Image6  # Re-entering the previous output
        self.displayImage(6)

        self.Image7 = analyze_quality(self.Image5, self.Image2)
        image = self.Image7  # Re-entering the previous output
        self.displayImage(7)

    def displayImage(self, windows=1, clear=False):
        qformat = QImage.Format_Indexed8

        if clear:
            if windows == 1:
                self.label_win_1.clear()
            elif windows == 2:
                self.label_win_2.clear()
            elif windows == 3:
                self.label_win_3.clear()
            elif windows == 4:
                self.label_win_2.clear()
            elif windows == 5:
                self.label_win_3.clear()
            elif windows == 6:
                self.label_win_2.clear()
            elif windows == 7:
                self.label_win_3.clear()
            return

        # Pilih image sesuai window
        if windows == 1:
            img_data = self.Image1
        elif windows == 2:
            img_data = self.Image2
        elif windows == 3:
            img_data = self.Image3
        elif windows == 4:
            img_data = self.Image4
        elif windows == 5:
            img_data = self.Image5
        elif windows == 6:
            img_data = self.Image6
        elif windows == 7:
            img_data = self.Image7
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
        scaled_pixmap1 = pixmap.scaled(self.label_win_1.size(), QtCore.Qt.KeepAspectRatio,
                                       QtCore.Qt.SmoothTransformation)
        scaled_pixmap2 = pixmap.scaled(self.label_win_2.size(), QtCore.Qt.KeepAspectRatio,
                                       QtCore.Qt.SmoothTransformation)
        scaled_pixmap3 = pixmap.scaled(self.label_win_3.size(), QtCore.Qt.KeepAspectRatio,
                                       QtCore.Qt.SmoothTransformation)
        scaled_pixmap4 = pixmap.scaled(self.label_win_4.size(), QtCore.Qt.KeepAspectRatio,
                                       QtCore.Qt.SmoothTransformation)
        scaled_pixmap5 = pixmap.scaled(self.label_win_5.size(), QtCore.Qt.KeepAspectRatio,
                                       QtCore.Qt.SmoothTransformation)
        scaled_pixmap6 = pixmap.scaled(self.label_win_6.size(), QtCore.Qt.KeepAspectRatio,
                                       QtCore.Qt.SmoothTransformation)
        scaled_pixmap7 = pixmap.scaled(self.label_win_7.size(), QtCore.Qt.KeepAspectRatio,
                                       QtCore.Qt.SmoothTransformation)

        if windows == 1:
            self.label_win_1.setPixmap(scaled_pixmap1)
            self.label_win_1.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        elif windows == 2:
            self.label_win_2.setPixmap(scaled_pixmap2)
            self.label_win_2.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        elif windows == 3:
            self.label_win_3.setPixmap(scaled_pixmap3)
            self.label_win_3.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        elif windows == 4:
            self.label_win_4.setPixmap(scaled_pixmap4)
            self.label_win_4.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        elif windows == 5:
            self.label_win_5.setPixmap(scaled_pixmap5)
            self.label_win_5.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        elif windows == 6:
            self.label_win_6.setPixmap(scaled_pixmap6)
            self.label_win_6.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        elif windows == 7:
            self.label_win_7.setPixmap(scaled_pixmap7)
            self.label_win_7.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

app = QtWidgets.QApplication(sys.argv)
window = ShowImage()
window.setWindowTitle('DIGITAL IMAGE PROCESSING')
window.show()
sys.exit(app.exec())