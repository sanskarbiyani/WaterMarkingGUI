from msilib.schema import SelfReg
from multiprocessing import Manager
from turtle import pencolor
from PySide6.QtWidgets import QMainWindow, QApplication, QGridLayout, QPushButton, QFileDialog, QLabel, QWidget, QColorDialog
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QPixmap, QImage
import sys
from PIL import Image, ImageFont, ImageDraw
import os


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setMinimumSize(QSize(800, 600))
        self.setWindowTitle("Watermark Image")
        self.layout = QGridLayout()

        self.get_image_btn = QPushButton("Select Image", self)
        self.get_image_btn.clicked.connect(self.get_img_btn_clicked)
        self.layout.addWidget(self.get_image_btn, 0, 0)

        self.watermark_image_btn = QPushButton("Add Watermark", self)
        self.watermark_image_btn.clicked.connect(self.watermark_image)
        self.watermark_image_btn.setEnabled(False)
        self.layout.addWidget(self.watermark_image_btn, 0, 1)

        self.discard_image_btn = QPushButton("Discard Image", self)
        self.discard_image_btn.clicked.connect(self.discard_image)
        self.discard_image_btn.setEnabled(False)
        self.layout.addWidget(self.discard_image_btn, 0, 2)

        self.save_image_btn = QPushButton("Save Image", self)
        self.save_image_btn.clicked.connect(self.save_image)
        self.save_image_btn.setEnabled(False)
        self.layout.addWidget(self.save_image_btn, 0, 3)

        self.change_color_btn = QPushButton("Change Pen Color", self)
        self.change_color_btn.clicked.connect(self.change_pen_color)
        self.layout.addWidget(self.change_color_btn, 1, 1, 1, 2)

        self.clear_watermark_btn = QPushButton("Clear Watermark", self)
        self.clear_watermark_btn.clicked.connect(self.clear_watermark)
        self.clear_watermark_btn.setEnabled(False)
        self.layout.addWidget(self.clear_watermark_btn, 1, 0)

        self.label = QLabel("Please Select an Image", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label, 2, 0, 2, 4)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def get_img_btn_clicked(self):
        self.filename = QFileDialog.getOpenFileName(
            self, "Select Image", "\\Users\\sansk\\OneDrive\\Pictures\\Screenshots", "Image files (*.png)")[0]

        if len(self.filename) == 0:
            return
        self.discard_image_btn.setEnabled(True)
        self.watermark_image_btn.setEnabled(True)
        self.label.clear()
        self.label.setPixmap(QPixmap(self.filename).scaledToWidth(750))
        self.get_image_btn.setEnabled(False)

    def watermark_image(self):
        image = Image.open(self.filename)
        copy_image = image.copy()

        draw = ImageDraw.Draw(copy_image)
        font = ImageFont.truetype("arial.ttf", 150)

        if hasattr(self, "pen_color"):
            draw.text((400, 200), "Sanskar's Image", self.pen_color, font=font)
        else:
            draw.text((400, 200), "Sanskar's Image", (0, 0, 0, 100), font=font)
        image_name = self.filename.split("/")[-1].split(".")[0]

        self.dir_loc = f"C:\\dev\\python\\imageWatermark\\img\\{image_name}.png"
        copy_image.save(self.dir_loc)
        self.label.clear()
        self.label.setPixmap(QPixmap(self.dir_loc).scaledToWidth(750))
        self.clear_watermark_btn.setEnabled(True)
        self.save_image_btn.setEnabled(True)

    def discard_image(self):
        if hasattr(self, "dir_loc") and os.path.exists(self.dir_loc):
            os.remove(self.dir_loc)
        self.label.clear()
        self.label.setText("Please Select a Image")
        self.discard_image_btn.setEnabled(False)
        self.watermark_image_btn.setEnabled(False)
        self.save_image_btn.setEnabled(False)
        self.get_image_btn.setEnabled(True)
        self.clear_watermark_btn.setEnabled(False)

    def save_image(self):
        self.label.setText("Image Saved.\nPlease Select a Image")
        delattr(self, "dir_loc")
        self.discard_image_btn.setEnabled(False)
        self.watermark_image_btn.setEnabled(False)
        self.save_image_btn.setEnabled(False)
        self.clear_watermark_btn.setEnabled(False)
        self.get_image_btn.setEnabled(True)

    def change_pen_color(self):
        selected_color = QColorDialog(self).getColor()
        selected_color.setAlpha(130)
        self.pen_color = selected_color.getRgb()

    def clear_watermark(self):
        self.discard_image()
        self.label.clear()
        self.discard_image_btn.setEnabled(True)
        self.watermark_image_btn.setEnabled(True)
        self.label.setPixmap(QPixmap(self.filename).scaledToWidth(750))
        self.clear_watermark_btn.setEnabled(False)
        self.get_image_btn.setEnabled(False)


app = QApplication([])
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
