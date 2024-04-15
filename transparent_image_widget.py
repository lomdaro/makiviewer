import sys
import os
import random
import configparser
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QTimer

class TransparentImageWidget(QtWidgets.QLabel):
    def __init__(self, image_paths, randomize, scale_factor, interval, enable_hover_transparency, parent=None):
        super(TransparentImageWidget, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.image_paths = image_paths
        self.randomize = randomize
        self.scale_factor = scale_factor
        self.enable_hover_transparency = enable_hover_transparency
        self.current_index = 0
        self.setPixmap(self.scaled_pixmap(self.image_paths[self.current_index]))
        self.setFixedSize(self.pixmap().size())
        self.timer = QTimer()
        self.timer.timeout.connect(self.change_image)
        self.timer.start(interval)
        self.update_position()

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.close()
        elif event.button() == Qt.LeftButton:
            self.timer.stop()  # Stop the timer
            self.change_image()  # Change the image immediately
            self.timer.start()  # Restart the timer

    def enterEvent(self, event):
        if self.enable_hover_transparency:
            self.setWindowOpacity(0.5)  # Set the opacity to 50% when hovered

    def leaveEvent(self, event):
        if self.enable_hover_transparency:
            self.setWindowOpacity(1.0)  # Return the opacity to 100% when not hovered

    def change_image(self):
        if self.randomize:
            self.current_index = random.randint(0, len(self.image_paths) - 1)
        else:
            self.current_index = (self.current_index + 1) % len(self.image_paths)
        current_image = self.image_paths[self.current_index]
        print(f"Displaying: {current_image}")
        self.setPixmap(self.scaled_pixmap(current_image))
        self.setFixedSize(self.pixmap().size())
        self.update_position()

    def update_position(self):
        screen_geometry = QtWidgets.QApplication.desktop().availableGeometry()
        screen_size = screen_geometry.size()
        self.move(screen_size.width() - self.width(), screen_size.height() - self.height())

    def scaled_pixmap(self, image_path):
        pixmap = QtGui.QPixmap(image_path)
        return pixmap.scaled(pixmap.size() * self.scale_factor, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

def main():
    app = QtWidgets.QApplication(sys.argv)

    config = configparser.ConfigParser()
    config.read('config.ini')

    sprite_folder = config.get('Settings', 'folder', fallback='sprites')
    randomize = config.getboolean('Settings', 'randomize', fallback=True)
    scale_factor = config.getfloat('Settings', 'scale', fallback=0.75)
    interval = config.getint('Settings', 'interval', fallback=60) * 1000  # Convert seconds to milliseconds
    enable_hover_transparency = config.getboolean('Settings', 'enable_hover_transparency', fallback=True)

    # Get the list of image files in the specified directory
    image_files = [os.path.join(sprite_folder, file) for file in os.listdir(sprite_folder) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    if not image_files:
        print("No image files found.")
        sys.exit(1)

    widget = TransparentImageWidget(image_files, randomize, scale_factor, interval, enable_hover_transparency)
    widget.show()
    sys.exit(app.exec_())