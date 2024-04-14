import sys
import os
import re
import random
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QTimer

class TransparentImageWidget(QtWidgets.QLabel):
    def __init__(self, image_paths, randomize, scale_factor, parent=None):
        super(TransparentImageWidget, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.image_paths = image_paths
        self.randomize = randomize
        self.scale_factor = scale_factor
        self.current_index = 0
        self.setPixmap(self.scaled_pixmap(self.image_paths[self.current_index]))
        self.setFixedSize(self.pixmap().size())
        self.timer = QTimer()
        self.timer.timeout.connect(self.change_image)
        self.timer.start(60000)  # Change image every 60 seconds (60000 milliseconds)
        self.update_position()

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.close()
        elif event.button() == Qt.LeftButton:
            self.timer.stop()  # Stop the timer
            self.change_image()  # Change the image immediately
            self.timer.start(60000)  # Restart the timer

    def enterEvent(self, event):
        self.setWindowOpacity(0.5)  # Set the opacity to 50% when hovered

    def leaveEvent(self, event):
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

def get_user_choice(prompt):
    while True:
        choice = input(prompt).lower()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no', '']:
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def main():
    app = QtWidgets.QApplication(sys.argv)

    # Prompt the user for sprite type preference
    sprite_type = get_user_choice("Do you want to use swimsuit sprites? (y/n): ")
    sprite_folder = "sprites_swimsuit" if sprite_type else "sprites"

    # Get the list of image files in the specified directory
    image_files = [os.path.join(sprite_folder, file) for file in os.listdir(sprite_folder) if re.match(r'maki\d+\.png', file)]

    # Sort the image files numerically
    image_files.sort(key=lambda x: int(re.findall(r'\d+', x)[0]))

    if not image_files:
        print("No image files found.")
        sys.exit(1)

    # Prompt the user for randomization preference
    randomize = get_user_choice("Do you want to randomize the sprites? (y/n): ")

    # Prompt the user for image size preference
    while True:
        size_input = input("Enter the size of the images (0.1 to 1.0, default is 0.75): ")
        if not size_input:
            scale_factor = 0.75
            break
        try:
            scale_factor = float(size_input)
            if 0.1 <= scale_factor <= 1.0:
                break
            else:
                print("Invalid size. Please enter a value between 0.1 and 1.0.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    widget = TransparentImageWidget(image_files, randomize, scale_factor)
    widget.show()
    sys.exit(app.exec_())