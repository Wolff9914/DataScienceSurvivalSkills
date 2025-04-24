import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QTextEdit, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import tensorflow as tf
import numpy as np
from PIL import Image


class TFLiteModelApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'TF Lite Model Predictions with PyQt5'
        self.left = 500
        self.top = 300
        self.width = 640
        self.height = 480
        self.initUI()

        self.model = None
        (_, _), (self.x_test, self.y_test) = tf.keras.datasets.cifar10.load_data()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Main layout
        layout = QVBoxLayout()

        # Load Model button
        self.loadButton = QPushButton('Load TensorFlow Lite Model', self)
        self.loadButton.clicked.connect(self.loadModel)
        layout.addWidget(self.loadButton)

        # Run Model button
        self.runButton = QPushButton('Run Model', self)
        self.runButton.clicked.connect(self.runModel)
        self.runButton.setEnabled(False)  # Disabled until a model is loaded
        layout.addWidget(self.runButton)

        # Text edit for results
        self.resultsText = QTextEdit(self)
        self.resultsText.setReadOnly(True)
        layout.addWidget(self.resultsText)

        # Image label for displaying the image
        self.imageLabel = QLabel(self)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.imageLabel)

        # Enable drag and drop
        self.setAcceptDrops(True)

        # Set the layout to a central widget
        centralWidget = QWidget(self)
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def loadModel(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "TensorFlow Lite Models (*.tflite)", options=options)
        if fileName:
            self.model = tf.lite.Interpreter(model_path=fileName)
            self.model.allocate_tensors()
            self.runButton.setEnabled(True)
            self.resultsText.append(f"Model loaded: {fileName}\n")

    def runModel(self):
        if self.model:
            input_details = self.model.get_input_details()
            output_details = self.model.get_output_details()

            dict_classes = self.load_text_to_dict("labelfile.txt")
            dict_out = {}
            dict_out['true_val'] = []
            dict_out['predicted_val'] = []

            for test_image, test_label in zip(self.x_test[0:5], self.y_test[0:5]):
                # Get prediction of TFLite model
                input_data = np.array(test_image[None, ...], dtype=np.float32)
                self.model.set_tensor(input_details[0]['index'], input_data)
                self.model.invoke()
                result_tflite = self.model.get_tensor(output_details[0]['index'])
                dict_out['true_val'].append(dict_classes[np.argmax(result_tflite)])
                dict_out['predicted_val'].append(dict_classes[int(test_label)])
            self.resultsText.append(f"True Label: {dict_out['true_val']} \n"
                                    f"Model output: {dict_out['predicted_val']}")

    def load_text_to_dict(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            # Create a dictionary with line numbers as keys and lines as values
            line_dict = {i: line.strip() for i, line in enumerate(lines)}
        return line_dict

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        file_path = event.mimeData().urls()[0].toLocalFile()
        if file_path:
            self.processImage(file_path)

    def processImage(self, file_path):
        # Display image in the GUI
        pixmap = QPixmap(file_path)
        self.imageLabel.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))

        # Preprocess image to match input format for the model
        img = Image.open(file_path).convert('L')  # Convert to grayscale (if needed)
        img = img.resize((28, 28))  # Resize to match the input size (28x28 for Fashion MNIST)
        img = np.array(img) / 255.0  # Normalize the image
        img = np.expand_dims(img, axis=-1)  # Add the channel dimension

        # Run the model on the image
        self.classifyImage(img)

    def classifyImage(self, img):
        if self.model:
            input_details = self.model.get_input_details()
            output_details = self.model.get_output_details()

            # Run inference
            input_data = np.array(img[None, ...], dtype=np.float32)
            self.model.set_tensor(input_details[0]['index'], input_data)
            self.model.invoke()

            # Get the output
            result_tflite = self.model.get_tensor(output_details[0]['index'])
            predicted_class = np.argmax(result_tflite)

            dict_classes = self.load_text_to_dict("labelfile.txt")
            predicted_label = dict_classes[predicted_class]

            self.resultsText.append(f"Predicted Class: {predicted_label}")


def main():
    app = QApplication(sys.argv)
    ex = TFLiteModelApp()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
