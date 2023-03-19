import qimage2ndarray
import sys
import numpy as np
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QFileDialog, QAction, QPlainTextEdit, QLabel, QPushButton, QScrollArea
from PySide6.QtUiTools import QUiLoader
from numpy import uint16

loader = QUiLoader()


class UserInterface(QtWidgets.QMainWindow):
    def __init__(self):
        super(UserInterface, self).__init__()
        self.imgarr = np.zeros(0)
        uic.loadUi('basic.ui', self)

        self.open_action = self.findChild(QAction, 'open_action')
        self.open_action.triggered.connect(self.open_action_fun)

        self.save_action = self.findChild(QAction, 'save_action')
        self.save_action.triggered.connect(self.save_action_fun)

        self.path_bar = self.findChild(QPlainTextEdit, 'path_bar')

        self.scroll_area = self.findChild(QScrollArea, 'scrollArea')
        self.picture_label = self.findChild(QLabel, 'picture')
        self.current_picture = QImage()
        self.current_picture_changed = QImage()

        self.reload_image_button = self.findChild(QPushButton, 'reload_image_button')
        self.reload_image_button.clicked.connect(self.reload_image_button_fun)

        self.inverse_button = self.findChild(QPushButton, 'inverse_button')
        self.inverse_button.clicked.connect(self.inverse_button_fun)

        self.brightness_correction_button = self.findChild(QPushButton, 'brightness_correction_button')
        self.brightness_correction_button.clicked.connect(self.brightness_correction_button_fun)

        self.contrast_enhancement_button = self.findChild(QPushButton, 'contrast_enhancement_button')
        self.contrast_enhancement_button.clicked.connect(self.contrast_enhancement_button_fun)

        self.gamma_correction_button = self.findChild(QPushButton, 'gamma_correction_button')
        self.gamma_correction_button.clicked.connect(self.gamma_correction_button_fun)

        self.gaussian_blur_button = self.findChild(QPushButton, 'gaussian_blur_button')
        self.gaussian_blur_button.clicked.connect(self.gaussian_blur_button_fun)

        self.sharpen_button = self.findChild(QPushButton, 'sharpen_button')
        self.sharpen_button.clicked.connect(self.sharpen_button_fun)

        self.edge_detection_button = self.findChild(QPushButton, 'edge_detection_button')
        self.edge_detection_button.clicked.connect(self.edge_detection_button_fun)

        self.emboss_button = self.findChild(QPushButton, 'emboss_button')
        self.emboss_button.clicked.connect(self.emboss_button_fun)

    def enable_all_buttons(self):
        self.inverse_button.setEnabled(True)
        self.brightness_correction_button.setEnabled(True)
        self.contrast_enhancement_button.setEnabled(True)
        self.gamma_correction_button.setEnabled(True)
        self.gaussian_blur_button.setEnabled(True)
        self.sharpen_button.setEnabled(True)
        self.edge_detection_button.setEnabled(True)
        self.emboss_button.setEnabled(True)

    def open_action_fun(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file',
                                            'A:\Desktop\studia\sem 6\grafika\lab1', "Image files (*.jpg *.png)")
        if fname:
            fname = fname.replace('/', '\\')
            self.path_bar.setPlainText(fname)
            self.current_picture = QImage()
            self.current_picture.load(fname)
            self.current_picture_changed = self.current_picture.copy()
            self.picture_label.resize(self.scroll_area.width(), self.scroll_area.height())
            self.picture_label.setPixmap(
                QPixmap.fromImage(self.current_picture_changed.scaledToHeight(self.scroll_area.height())))
            self.imgarr = qimage2ndarray.rgb_view(self.current_picture_changed)
            self.enable_all_buttons()

    def save_action_fun(self):
        fname, type = QFileDialog.getSaveFileName(self, "Save file", "A:\Desktop\studia\sem 6\grafika\lab1",
                                                  ".jpg;;.png")
        if fname:
            fname = fname.replace('/', '\\')
            if type == '.png':
                fname += '.png'
                self.current_picture_changed.save(fname, format='png')
            if type == '.jpg':
                fname += '.jpg'
                self.current_picture_changed.save(fname, format='jpg')

    def resizeEvent(self, event):
        self.picture_label.resize(self.scroll_area.width(), self.scroll_area.height())
        self.picture_label.setPixmap(
            QPixmap.fromImage(self.current_picture_changed.scaledToHeight(self.scroll_area.height())))

    def reload_image_button_fun(self):
        self.current_picture_changed = self.current_picture.copy()
        self.imgarr = qimage2ndarray.rgb_view(self.current_picture_changed)
        self.picture_label.setPixmap(
            QPixmap.fromImage(self.current_picture_changed.scaledToHeight(self.scroll_area.height())))
        self.enable_all_buttons()
        self.reload_image_button.setEnabled(False)

    def inverse_button_fun(self):
        self.imgarr[:, :, list(range(0, 3))] = 255 - self.imgarr[:, :, list(range(0, 3))]
        self.current_picture_changed = qimage2ndarray.array2qimage(self.imgarr[:, :, list(range(0, 3))])
        self.picture_label.setPixmap(
            QPixmap.fromImage(self.current_picture_changed.scaledToHeight(self.scroll_area.height())))
        self.reload_image_button.setEnabled(True)
        self.inverse_button.setEnabled(False)

    def adjust_picture_arr(self, arr):
        self.imgarr = arr.copy()
        self.current_picture_changed = qimage2ndarray.array2qimage(self.imgarr[:, :, list(range(0, 3))]).copy()
        self.picture_label.setPixmap(
            QPixmap.fromImage(self.current_picture_changed.scaledToHeight(self.scroll_area.height())))
        self.reload_image_button.setEnabled(True)

    def brightness_correction_button_fun(self):
        arr = np.zeros(shape=self.imgarr.shape, dtype=uint16)
        arr = arr + self.imgarr
        arr = arr + 10
        arr = np.clip(a=arr, a_min=0, a_max=255)
        self.adjust_picture_arr(arr.copy())

    def contrast_enhancement_button_fun(self):
        arr = np.zeros(shape=self.imgarr.shape, dtype=float)
        arr += self.imgarr
        arr = np.floor(self.imgarr[:, :, list(range(0, 3))] + (128 - self.imgarr[:, :, list(range(0, 3))]) * 0.1)
        self.adjust_picture_arr(arr.copy())
        self.contrast_enhancement_button.setEnabled(False)

    def gamma_correction_button_fun(self):
        gamma = 1.1
        gamma_correction = 1 / gamma
        arr = np.zeros(shape=self.imgarr.shape, dtype=float)
        arr += self.imgarr
        arr = np.power(arr, gamma_correction)
        self.adjust_picture_arr(arr.copy())
        self.gamma_correction_button.setEnabled(False)

    def convolution(self, filter_arr):
        red_arr = self.imgarr[:, :, 0]
        green_arr = self.imgarr[:, :, 1]
        blue_arr = self.imgarr[:, :, 2]
        red_arr = np.pad(red_arr, ((1, 1), (1, 1)), 'constant')
        green_arr = np.pad(green_arr, ((1, 1), (1, 1)), 'constant')
        blue_arr = np.pad(blue_arr, ((1, 1), (1, 1)), 'constant')

        width = red_arr.shape[1]
        width_filter = filter_arr.shape[1]
        height = red_arr.shape[0]
        height_filter = filter_arr.shape[0]

        r0 = np.arange(width - width_filter + 1)
        r0 = np.repeat(r0, height - height_filter + 1)
        r0 = r0.reshape(-1, 1)
        r1 = np.arange(width_filter).reshape(1, width_filter)
        r = np.repeat(r0 + r1, height_filter, axis=1)

        c0 = np.arange(height_filter)
        c0 = np.tile(c0, width_filter).reshape(1, -1)
        c1 = np.arange(height - height_filter + 1).reshape(-1, 1)
        c = c0 + c1
        c = np.tile(c, [width - width_filter + 1, 1])

        red_arr = np.reshape(a=np.floor(red_arr[c, r] @ filter_arr.reshape(-1)),
                             newshape=(height - height_filter + 1, width - width_filter + 1), order='F')
        green_arr = np.reshape(a=np.floor(green_arr[c, r] @ filter_arr.reshape(-1)),
                               newshape=(height - height_filter + 1, width - width_filter + 1), order='F')
        blue_arr = np.reshape(a=np.floor(blue_arr[c, r] @ filter_arr.reshape(-1)),
                              newshape=(height - height_filter + 1, width - width_filter + 1), order='F')
        red_arr = np.clip(a=red_arr, a_min=0, a_max=255)
        green_arr = np.clip(a=green_arr, a_min=0, a_max=255)
        blue_arr = np.clip(a=blue_arr, a_min=0, a_max=255)
        red_arr = red_arr.astype('uint8')
        green_arr = green_arr.astype('uint8')
        blue_arr = blue_arr.astype('uint8')
        self.imgarr[:, :, 0] = red_arr.copy()
        self.imgarr[:, :, 1] = green_arr.copy()
        self.imgarr[:, :, 2] = blue_arr.copy()
        # https://lucasdavid.github.io/blog/computer-vision/vectorization/

    def adjust_picture(self):
        self.current_picture_changed = qimage2ndarray.array2qimage(self.imgarr[:, :, list(range(0, 3))]).copy()
        self.picture_label.setPixmap(
            QPixmap.fromImage(self.current_picture_changed.scaledToHeight(self.scroll_area.height())))
        self.reload_image_button.setEnabled(True)

    def gaussian_blur_button_fun(self):
        filter_arr = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]])
        filter_arr = filter_arr / np.sum(filter_arr)
        self.convolution(filter_arr)
        self.adjust_picture()
        self.gaussian_blur_button.setEnabled(False)

    def sharpen_button_fun(self):
        filter_arr = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        filter_arr = filter_arr / np.sum(filter_arr)
        self.convolution(filter_arr)
        self.adjust_picture()
        self.sharpen_button.setEnabled(False)

    def edge_detection_button_fun(self):
        filter_arr = np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 0]])
        self.convolution(filter_arr)
        self.adjust_picture()
        self.edge_detection_button.setEnabled(False)

    def emboss_button_fun(self):
        filter_arr = np.array([[-1, -1, 0], [-1, 1, 1], [0, 1, 1]])
        filter_arr = filter_arr / np.sum(filter_arr)
        self.convolution(filter_arr)
        self.adjust_picture()
        self.emboss_button.setEnabled(False)


app = QtWidgets.QApplication(sys.argv)
window = UserInterface()
window.show()
app.exec_()
