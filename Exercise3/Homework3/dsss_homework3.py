import glob
import random
import matplotlib.pyplot as plt
import imageio.v2 as io
import json 
import cv2
import numpy as np

BAGLS_PATH = "Mini_BAGLS_dataset"

''' 
Task 1: get four arbitrary images and their corresponding segmentation masks and metadata
'''
selected_files = []  # List to collect file paths

for i in range(4):
    fileNum = random.randint(10, 99)  # Pick a random image number between 10 and 99 
    files = glob.glob(BAGLS_PATH + "/*" + str(fileNum) + "*")  # Find the corresponding data files to the picked image number
    selected_files.append(files)  # Add image and mask files to the list

print(selected_files)

'''
Task 2: Create a plot to display all images and their corresponding segmentation masks 
'''
meta_info = []  # List to collect metadata info (subject disorder status)
fig, axes = plt.subplots(2, 2, figsize=(10, 5))  # Create a 2x2 grid for displaying the images

# Flatten axes for easy iteration
axes = axes.flatten()

for i, file in enumerate(selected_files):
    meta = file[0]
    # Read the .meta file
    with open(meta) as f:
        meta_data = json.load(f)
    disorder_status = meta_data.get('Subject disorder status', 'Unknown') # Extract the disorder status
    meta_info.append(disorder_status)  # Add the disorder status to the metadata list
    img = io.imread(file[1])  # Read the image (second file in the list)
    seg = io.imread(file[2])  # Read the segmentation mask (third file in the list)
    
    ax = axes[i]  # Get the current axis to plot on
    ax.axis("off")  # Turn off the axis
    # Display the image
    ax.imshow(img)
    # Overlay the segmentation mask with transparency
    ax.imshow(seg, alpha=0.5)  # Add transparency to the segmentation mask for overlay effect
    # Set the title to the "Subject disorder status"
    ax.set_title(f"Status: \n{meta_info[i]}")

# Adjust layout to avoid overlap
plt.tight_layout()
plt.show()

'''
Task 3: Implement the lightness, average and luminosity method on "leaves.jgb" 
'''
img_path = 'leaves.jpg' # Image Path
img_leaves = cv2.imread(img_path)
img_rgb = cv2.cvtColor(img_leaves, cv2.COLOR_BGR2RGB) #Convert image to RGB
fig2, axes = plt.subplots(1, 4, figsize=(15, 5))
fig2.suptitle("Task 3: Grayscale Conversion Methods", fontsize=16)
# Show original image
axes[0].imshow(img_rgb)  
axes[0].axis("off")  
axes[0].set_title("Original")  

# Lightness method
img_lightness = (np.max(img_rgb, axis=2) + np.min(img_rgb, axis=2)) / 2
axes[1].imshow(img_lightness, cmap="gray")
axes[1].axis("off")
axes[1].set_title("Lightness Method")

# Average method
img_average = np.mean(img_rgb, axis=2)
axes[2].imshow(img_average, cmap="gray")
axes[2].axis("off")
axes[2].set_title("Average Method")

# Luminosity method
img_luminosity = (img_rgb[:, :, 0] * 0.2989) + (img_rgb[:, :, 1] * 0.587) + (img_rgb[:, :, 2] * 0.1140) 
axes[3].imshow(img_luminosity, cmap="gray")
axes[3].axis("off")
axes[3].set_title("Luminosity Method")

plt.tight_layout()
plt.show()
