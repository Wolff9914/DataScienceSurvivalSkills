import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.datasets import fashion_mnist
import cv2

# Lade das Fashion MNIST Dataset
(x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()

# Klassenlabels
class_names = [
    "T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
    "Sandal", "Shirt", "Sneaker", "Bag", "Ankle Boot"
]

# Wähle zufällige Indizes aus den Testdaten aus
random_indices = np.random.choice(range(len(x_test)), 5, replace=False)

# Speichere die Bilder mit den zugehörigen Klassenlabels
for i in random_indices:
    image = x_test[i]  # Bilddaten
    label = y_test[i]  # Klassenlabel
    class_name = class_names[label]

    # Speicherpfad erstellen
    filename = f"fashion_mnist_example_{class_name}.jpg"

    # Speichere das Bild als PNG (skaliere für graue Bilder auf 0–255)
    cv2.imwrite(filename, image)
    print(f"Bild gespeichert: {filename}")
