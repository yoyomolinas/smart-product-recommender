# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 20:10:16 2019

@author: burak
"""

from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense


#Initialising the CNN
classifier = Sequential()

#Convolutional Layer - Tensorflow
classifier.add(Convolution2D(32, 3, 3, input_shape = (64 , 64 , 3), activation = 'relu'))

#Pooling Step
classifier.add(MaxPooling2D(pool_size = (2, 2)))

#Second Convolutional Layer - Tensorflow
classifier.add(Convolution2D(64, 3, 3, activation = 'relu'))

#Second Pooling Step
classifier.add(MaxPooling2D(pool_size = (2, 2)))

#Flattening
classifier.add(Flatten())

#Full Connection -> for binary sigmoid, for more -> softmax
classifier.add(Dense(output_dim = 128, activation = 'relu'))

classifier.add(Dense(output_dim = 1, activation = 'sigmoid'))

classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

# Fitting the CNN to the images
from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1./255)

trainining_set = train_datagen.flow_from_directory(
        'dataset/training_set',
        target_size=(64, 64),
        batch_size=32,
        class_mode='binary')

test_set = test_datagen.flow_from_directory(
        'dataset/test_set',
        target_size=(64, 64),
        batch_size=32,
        class_mode='binary')

classifier.fit_generator(
        trainining_set,
        steps_per_epoch=8000,
        epochs=25,
        validation_data=test_set,
        validation_steps=2000)