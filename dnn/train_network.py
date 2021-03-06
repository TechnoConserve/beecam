# Set the matplotlib backend so figures can be saved in the background
import matplotlib

matplotlib.use("Agg")

from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import img_to_array
from keras.utils import to_categorical
from beecam_network.lenet import LeNet

from imutils import paths
import matplotlib.pyplot as plt
import numpy as np
import argparse
import random
import cv2
import os

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
                help="path to input dataset")
ap.add_argument("-m", "--model", required=True,
                help="path to output model")
ap.add_argument("-p", "--plot", type=str, default="plot.png",
                help="path to output accuracy/loss plot")
args = vars(ap.parse_args())

# initialize the number of epochs to train for, initial learning rate,
# and batch size
EPOCHS = 70
INIT_LR = 1e-3
BS = 128

# initialize the data and labels
print("[INFO] loading images...")
data = []
labels = []

# grab the image paths and randomly shuffle them
image_paths = sorted(list(paths.list_images(args["dataset"])))
random.seed(42)
random.shuffle(image_paths)

# Loop over the input images
for img_path in image_paths:
    # Load the image, pre-process it, and store it in the data list
    image = cv2.imread(img_path)
    try:
        image = cv2.resize(image, (128, 128))
        image = img_to_array(image)
        data.append(image)
    except:
        print(img_path)
        print(image)

    # Extract the class label from the image path and update the
    # labels list
    label = img_path.split(os.path.sep)[-2]
    label = 1 if label == "Apis_mellifera" else 0
    labels.append(label)

data = np.array(data, dtype="float")
labels = np.array(labels)

print("data", data.shape)
print("labels", labels.shape)

# Partition the data into training and testing splits using 75% of
# the data for training and the remaining 25% for testing
(train_x, test_x, train_y, test_y) = train_test_split(data, labels, test_size=0.25,
                                                      random_state=42)
# Convert the labels from integers to vectors
train_y = to_categorical(train_y, num_classes=2)
test_y = to_categorical(test_y, num_classes=2)

# Construct the image generator for data augmentation
aug = ImageDataGenerator(rotation_range=30, width_shift_range=0.1,
                         height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
                         horizontal_flip=True, fill_mode="nearest")

# Initialize the model
print("[INFO] Compiling model...")
model = LeNet.build(width=128, height=128, depth=3, classes=2)
opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
model.compile(loss="binary_crossentropy", optimizer=opt, metrics=["accuracy"])

# Train the network
print("[INFO] Training network...")
H = model.fit_generator(aug.flow(train_x, train_y, batch_size=BS),
                        validation_data=(test_x, test_y), steps_per_epoch=len(train_x) // BS,
                        epochs=EPOCHS, verbose=1)

# Save the model to disk
print("[INFO] Serializing network...")
model.save(args["model"])

# Plot the training loss and accuracy
plt.style.use("ggplot")
plt.figure()
N = EPOCHS
plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
plt.plot(np.arange(0, N), H.history["acc"], label="train_acc")
plt.plot(np.arange(0, N), H.history["val_acc"], label="val_acc")
plt.title("Training Loss and Accuracy on Santa/Not Santa")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend(loc="lower left")
plt.savefig(args["plot"])
