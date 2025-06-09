import cv2
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import numpy as np
from PyQt5.QtGui import QImage

def loadimg(self):
    filename, _ = QFileDialog.getOpenFileName(
        self,
        "Load Image",
        "",
        "Image Files (*.png *.jpg *.bmp *.jpeg);;All Files (*)"
    )
    if filename:
        image = cv2.imread(filename)
        if image is not None:
            return image
        else:
            QMessageBox.warning(self, "Error", "Failed to Load Image.")
    return None

def saveimg(self, image):
    if image is None:
        QMessageBox.warning(self, "Error", "Tidak ada gambar untuk disimpan.")
        return

    filename, _ = QFileDialog.getSaveFileName(
        self,
        "Save File",
        "",
        "JPEG Files (*.jpg);;PNG Files (*.png);;Bitmap Files (*.bmp);;All Files (*)"
    )

    if filename:
        success = cv2.imwrite(filename, image)
        if success:
            QMessageBox.information(self, "Success", "Gambar berhasil disimpan.")
        else:
            QMessageBox.warning(self, "Error", "Gagal menyimpan gambar.")

def array2qimage(img_data):
    img_data = img_data.astype(np.uint8)

    if img_data.ndim == 2:
        # Grayscale
        height, width = img_data.shape
        bytes_per_line = width
        qimg = QImage(img_data.tobytes(), width, height, bytes_per_line, QImage.Format_Grayscale8)
        return qimg

    elif img_data.ndim == 3:
        height, width, channels = img_data.shape
        if channels == 3:
            bytes_per_line = 3 * width
            qimg = QImage(img_data.data, width, height, bytes_per_line, QImage.Format_RGB888)
            if need_rgb_swap(img_data):
                qimg = qimg.rgbSwapped()
            return qimg
        elif channels == 4:
            bytes_per_line = 4 * width
            qimg = QImage(img_data.data, width, height, bytes_per_line, QImage.Format_RGBA8888)
            return qimg
        else:
            raise ValueError("Unsupported number of channels")
    else:
        raise ValueError("Unsupported image dimension")

def need_rgb_swap(img_data):
    """
    Deteksi otomatis apakah perlu rgbSwapped() atau tidak.
    Caranya: Cek dominasi warna kanal pertama (BGR atau RGB).
    """
    sample = img_data[0, 0]  # Ambil pixel pertama
    blue, green, red = sample if len(sample) == 3 else (0, 0, 0)

    return blue > red
