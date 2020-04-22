
import sys
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget, QMessageBox, QLabel, QDialog,
    QApplication, QPushButton, QDesktopWidget, QLineEdit, QTabWidget)
from PyQt5.QtGui import QIcon, QPixmap, QImage, QPalette, QBrush
from PyQt5.QtCore import Qt, QTimer
import numpy as np
import os
import pickle

class Setting(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.startButton = QPushButton('GENGGAI', self)
        self.startButton.move(400, 50)
        self.startButton = QPushButton('start', self)
        self.startButton.move(400, 100)
        self.startButton = QPushButton('start', self)
        self.startButton.move(400, 150)
        self.startButton = QPushButton('start', self)
        self.startButton.move(400, 200)