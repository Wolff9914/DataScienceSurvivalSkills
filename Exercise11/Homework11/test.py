from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QLineEdit, QPushButton
import tensorflow as tf
import numpy as np
import cv2
import sys

class FashionMNISTApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fashion MNIST Classifier")
        self.setGeometry(500, 300, 800, 600)

        # Load TFLite model
        print("Loading TFLite model...")  # Debugging message
        self.model = self.load_tflite_model("fashion_mnist_model.tflite")
        if self.model:
            print("Model loaded successfully.")  # Debugging message
        else:
            print("Failed to load the model.")  # Debugging message

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

        # Textbox for image path
        self.image_path_input = QLineEdit(self)
        self.image_path_input.setPlaceholderText("Enter image file path here...")
        layout.addWidget(self.image_path_input)

        # Button to load image
        self.load_button = QPushButton("Load Image", self)
        self.load_button.clicked.connect(self.load_image_from_path)
        layout.addWidget(self.load_button)

        # Image label to display the image
        self.image_label = QLabel("No image loaded", self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("background-color: #f0f0f0; border: 2px dashed #aaa;")
        self.image_label.setFixedSize(400, 300)
        layout.addWidget(self.image_label)

        # Prediction label
        self.prediction_label = QLabel("", self)
        self.prediction_label.setAlignment(Qt.AlignCenter)
        self.prediction_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.prediction_label)

    def load_image_from_path(self):
        image_path = self.image_path_input.text()  # Get path from text input
        print(f"Image path entered: {image_path}")  # Debugging message
        
        if image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            pixmap = QPixmap(image_path)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.classify_image(image_path)
        else:
            self.prediction_label.setText("Unsupported file format. Please enter a valid image file path.")

    def load_tflite_model(self, model_path):
        try:
            interpreter = tf.lite.Interpreter(model_path=model_path)
            interpreter.allocate_tensors()
            return interpreter
        except Exception as e:
            print(f"Error loading model: {e}")  # Debugging message
            return None

    def classify_image(self, image_path):
        print(f"Classifying image: {image_path}")  # Debugging message

        # Preprocess image for model input
        input_details = self.model.get_input_details()
        output_details = self.model.get_output_details()

        # Load and preprocess the image
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            print("Error: Image could not be read.")  # Debugging message
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
        print(f"Predicted class index: {predicted_class}")  # Debugging message
        self.prediction_label.setText(f"Predicted Class: {self.classes[predicted_class]}")

def main():
    app = QApplication(sys.argv)
    main_window = FashionMNISTApp()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
