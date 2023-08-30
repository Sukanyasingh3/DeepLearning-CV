# -*- coding: utf-8 -*-
"""Plant disease diagnosis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lql9FsZNwHKoCCqPYCSDu2Ns8kgaxJ-k
"""

!mkdir ~/.kaggle
!mv ./kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

#Downloading dataset
!kaggle datasets download -d emmarex/plantdisease

#Importing Libraries
import tensorflow as tf
from tensorflow import keras
from keras import Sequential
from keras import layers
from keras.layers import Dense,Conv2D,MaxPooling2D,Flatten,BatchNormalization,Dropout,AveragePooling2D
from keras.layers import Activation, Dropout, Flatten, Dense, GaussianNoise, GlobalMaxPooling2D
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import cv2
from sklearn.model_selection import train_test_split

#Unzipping the file
import zipfile
zip_ref = zipfile.ZipFile('/content/plantdisease.zip', 'r')
zip_ref.extractall('/content')
zip_ref.close()

#Loading the images
x_data= keras.utils.image_dataset_from_directory(
    directory = '/content/PlantVillage',
    labels='inferred',
    label_mode = 'int',
    batch_size=100,
    image_size=(256,256)

)

# Spliting data into train and test
train_ds =x_data
test_ds = tf.keras.preprocessing.image_dataset_from_directory(
    directory='/content/PlantVillage',
    labels='inferred',
    label_mode='int',
    batch_size=32,
    image_size=(256, 256),
    validation_split=0.2,
    subset='validation',
    seed=42
)

class_names = x_data.class_names
len(class_names)

class_names

# Displaying a few sample images
plt.figure(figsize=(20, 20))
for images, labels in train_ds.take(1):
    for i in range(6):
        ax = plt.subplot(3, 3, i + 1)
        plt.imshow(images[i].numpy().astype("uint8"))
        plt.title(class_names[labels[i]])
        plt.axis("off")
plt.show()

input_shape = (256, 256, 3)

# Createing the base model
base_model = tf.keras.applications.ResNet50(
    include_top=False,
    weights='imagenet',
    input_shape=input_shape
)
base_model.trainable = False

model = tf.keras.Sequential([
    base_model,
    layers.Flatten(),
    layers.Dense(15, activation='softmax')
])

model.summary()

# Compiling the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

#Training
history = model.fit(train_ds,epochs=5, batch_size=200, validation_data=test_ds)

model.evaluate(test_ds)

#Plotting  Graphs - Accuracy
plt.plot(history.history['accuracy'],color='red',label='train')
plt.plot(history.history['val_accuracy'],color='blue',label='validation')
plt.title('Model accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()

#Loss
plt.plot(history.history['loss'],color='red',label='train')
plt.plot(history.history['val_loss'],color='blue',label='validation')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()