import sys
import os
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog, QLineEdit, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class ImageCropper(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Cropper")
        self.setGeometry(100, 100, 800, 600)

        # Variables to store coordinates
        self.template_crop_image_path = ""
        self.starting_x = self.starting_y = self.ending_x = self.ending_y = -1
        self.mouse_pressed = False

        # Labels
        self.image_label = QLabel(self)
        self.image_label.setGeometry(10, 10, 500, 500)

        # Buttons
        self.select_image_button = QPushButton("Select Sample Crop Image", self)
        self.select_image_button.setGeometry(550, 10, 200, 30)
        self.select_image_button.clicked.connect(self.select_image)

        self.output_path_label = QLabel("Output Folder:", self)
        self.output_path_label.setGeometry(10, 530, 100, 20)

        self.output_path_text = QLineEdit(self)
        self.output_path_text.setGeometry(120, 530, 400, 20)

        self.browse_output_button = QPushButton("Browse", self)
        self.browse_output_button.setGeometry(530, 525, 100, 30)
        self.browse_output_button.clicked.connect(self.browse_output_folder)

        self.input_path_label = QLabel("Input Folder:", self)
        self.input_path_label.setGeometry(10, 560, 100, 20)

        self.input_path_text = QLineEdit(self)
        self.input_path_text.setGeometry(120, 560, 400, 20)

        self.browse_input_button = QPushButton("Browse", self)
        self.browse_input_button.setGeometry(530, 555, 100, 30)
        self.browse_input_button.clicked.connect(self.browse_input_folder)

        self.crop_button = QPushButton("Crop and Save", self)
        self.crop_button.setGeometry(650, 525, 120, 50)
        self.crop_button.clicked.connect(self.crop_and_save)

        self.template_crop_image_path = ""

    def select_image(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.tiff)")
        if file_dialog.exec_():
            self.template_crop_image_path = file_dialog.selectedFiles()[0]
            self.run_opencv_code()

    def browse_output_folder(self):
        folder_dialog = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        self.output_path_text.setText(folder_dialog)

    def browse_input_folder(self):
        folder_dialog = QFileDialog.getExistingDirectory(self, "Select Input Folder")
        self.input_path_text.setText(folder_dialog)

    def run_opencv_code(self):
        img = cv2.imread(self.template_crop_image_path)
        img_dup = np.copy(img)
        mouse_pressed = False
        starting_x = starting_y = ending_x = ending_y = -1

        def mousebutton(event, x, y, flags, param):
            nonlocal img_dup, starting_x, starting_y, ending_x, ending_y, mouse_pressed

            if event == cv2.EVENT_LBUTTONDOWN:
                mouse_pressed = True
                starting_x, starting_y = x, y
                img_dup = np.copy(img)

            elif event == cv2.EVENT_MOUSEMOVE:
                if mouse_pressed:
                    img_dup = np.copy(img)
                    cv2.rectangle(img_dup, (starting_x, starting_y), (x, y), (0, 255, 0), 1)

            elif event == cv2.EVENT_LBUTTONUP:
                mouse_pressed = False
                ending_x, ending_y = x, y

        cv2.namedWindow('image')
        cv2.setMouseCallback('image', mousebutton)

        while True:
            cv2.imshow('image', img_dup)
            k = cv2.waitKey(1)
            if k == ord('c'):
                if starting_y > ending_y:
                    starting_y, ending_y = ending_y, starting_y
                if starting_x > ending_x:
                    starting_x, ending_x = ending_x, starting_x
                if ending_y - starting_y > 1 and ending_x - starting_x > 0:
                    message_box = QMessageBox(self)
                    message_box.setIcon(QMessageBox.Question)
                    message_box.setText("Is this the area you want to select?")
                    message_box.setWindowTitle("Confirm Selection")
                    message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                    message_box.setDefaultButton(QMessageBox.Yes)
                    if message_box.exec_() == QMessageBox.Yes:
                        self.starting_x = starting_x
                        self.starting_y = starting_y
                        self.ending_x = ending_x
                        self.ending_y = ending_y
                        cv2.destroyAllWindows()
                        break
            elif k == 27:
                cv2.destroyAllWindows()
                break

    def crop_and_save(self):
        if self.template_crop_image_path == "":
            QMessageBox.warning(self, "Warning", "Please select a sample crop image.")
            return
        if self.output_path_text.text() == "":
            QMessageBox.warning(self, "Warning", "Please select an output folder.")
            return
        if self.input_path_text.text() == "":
            QMessageBox.warning(self, "Warning", "Please select an input folder.")
            return

        starting_x = min(self.starting_x, self.ending_x)
        starting_y = min(self.starting_y, self.ending_y)
        ending_x = max(self.starting_x, self.ending_x)
        ending_y = max(self.starting_y, self.ending_y)

        input_folder = self.input_path_text.text()
        output_folder = self.output_path_text.text()

        for file_name in os.listdir(input_folder):
            if file_name.endswith(('.png', '.jpg', '.jpeg', '.tiff')):
                input_path = os.path.join(input_folder, file_name)
                img = cv2.imread(input_path)
                cropped_image = img[starting_y:ending_y, starting_x:ending_x]
                output_path = os.path.join(output_folder, file_name.split('.')[0] + '_cropped.bmp')
                cv2.imwrite(output_path, cropped_image)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageCropper()
    window.show()
    sys.exit(app.exec_())
