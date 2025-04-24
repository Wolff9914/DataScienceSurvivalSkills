import sys
import tensorflow as tf
import numpy as np
import cv2
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget

class FashionMNISTApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fashion MNIST Classifier with Drag and Drop")
        self.setGeometry(500, 300, 800, 600)

        # Load TFLite model
        self.model = self.load_tflite_model("fashion_mnist_model.tflite")

        self.classes = [
            "T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
            "Sandal", "Shirt", "Sneaker", "Bag", "Ankle Boot"
        ]

        # Set up UI
        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Drop area for image
        self.image_label = QLabel("Drag and drop an image here", self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("background-color: #f0f0f0; border: 2px dashed #aaa;")
        self.image_label.setFixedSize(400, 300)
        layout.addWidget(self.image_label)

        # Prediction label
        self.prediction_label = QLabel("", self)
        self.prediction_label.setAlignment(Qt.AlignCenter)
        self.prediction_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.prediction_label)

        # Enable drag-and-drop for image_label
        #self.image_label.setAcceptDrops(True)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():  # Check if the dragged data contains URLs (files)
            event.accept()  # Accept the event if it's a valid file drop
        else:
            event.ignore()  # Otherwise ignore the event

    def dropEvent(self, event):
        if event.mimeData().hasUrls():  # Check if the dropped data contains URLs (files)
            file_url = event.mimeData().urls()[0].toLocalFile()  # Get file path
            if file_url.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):  # Check for valid image file types
                pixmap = QPixmap(file_url)
                self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Set image to label
                self.classify_image(file_url)  # Classify the image using parent method
            else:
                self.prediction_label.setText("Unsupported file format. Please drop an image file.")

    def load_tflite_model(self, model_path):
        try:
            interpreter = tf.lite.Interpreter(model_path=model_path)
            interpreter.allocate_tensors()
            return interpreter
        except Exception as e:
            print(f"Error loading model: {e}")
            return None

    def classify_image(self, image_path):
        # Preprocess image for model input
        input_details = self.model.get_input_details()
        output_details = self.model.get_output_details()

        # Load and preprocess the image
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            print("Error: Image could not be read.")
            return
        
        resized_image = cv2.resize(image, (28, 28))
        input_data = np.expand_dims(resized_image / 255.0, axis=(0, -1)).astype(np.float32)

        # Set input tensor
        self.model.set_tensor(input_details[0]['index'], input_data)
        self.model.invoke()

        # Get output tensor
        output_data = self.model.get_tensor(output_details[0]['index'])
        predicted_class = np.argmax(output_data)

        # Display results
        self.prediction_label.setText(f"Predicted Class: {self.classes[predicted_class]}")

def main():
    app = QApplication(sys.argv)
    main_window = FashionMNISTApp()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
