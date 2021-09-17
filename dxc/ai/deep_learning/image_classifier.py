# import tensorflow as tf
# import numpy as np
# import os
# import cv2
# import matplotlib.pyplot as plt
# import random
# from sklearn.model_selection import train_test_split

# training_data =[]

# #This function separates both features & labels from training data
# def seggregate_data(training_data):
#     X = []
#     Y = []
#     for features, lables in training_data:
#         X.append(features)
#         Y.append(lables)
#     X = np.array(X)
#     Y = np.array(Y)
#     return X,Y

# #This function reads each folder and each image and converts into array
# #This function internally calls seggregate_data to separate features & labels
# def create_training_data(CATEGORIES,DATADIR, IMG_SIZE = 100):
#     for category in CATEGORIES:
#         class_num = CATEGORIES.index(category)
#         path = os.path.join(DATADIR,category)
#         for img in os.listdir(path):
#             try:
#                 img_array = cv2.imread(os.path.join(path,img), cv2.IMREAD_GRAYSCALE) 
#                 new_array = cv2.resize(img_array,(IMG_SIZE,IMG_SIZE))
#                 training_data.append([new_array,class_num])
#             except Exception as e:
#                 pass
#     random.shuffle(training_data)
#     features,labels = seggregate_data(training_data)
#     return features,labels

# #This function splits the data into test and train
# #This function normalizes the features values in both train and test
# #This function converts label values to binary matrix
# def split_normalize_data(X, Y, category_count, TEST_SIZE = 0.20,IMG_SIZE=100 ):
#     x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size = TEST_SIZE)
#     x_train = x_train.reshape(x_train.shape[0], IMG_SIZE, IMG_SIZE, 1)
#     x_test = x_test.reshape(x_test.shape[0], IMG_SIZE, IMG_SIZE, 1)

#     x_train = x_train.astype('float32')
#     x_test = x_test.astype('float32')

#     x_train/=255
#     x_test/=255

#     y_train = tf.keras.utils.to_categorical(y_train, category_count)
#     y_test = tf.keras.utils.to_categorical(y_test, category_count)
    
#     return x_train, x_test, y_train, y_test

# #This function creates a model compiling input, Hidden and output layers
# def image_classifier(category_count, IMG_SIZE = 100):
    
#     model = tf.keras.models.Sequential()

#     model.add(tf.keras.layers.Conv2D(32,(3,3),input_shape=(IMG_SIZE,IMG_SIZE,1)))
#     model.add(tf.keras.layers.Dense(32,activation=tf.nn.relu))
#     model.add(tf.keras.layers.MaxPooling2D(pool_size=(2,2)))

#     model.add(tf.keras.layers.Conv2D(64, (3,3)))
#     model.add(tf.keras.layers.Dense(64,activation=tf.nn.relu))
#     model.add(tf.keras.layers.MaxPooling2D(pool_size=(2,2)))

#     model.add(tf.keras.layers.Flatten())

#     model.add(tf.keras.layers.Dropout(0.2))

#     model.add(tf.keras.layers.Dense(category_count,activation=tf.nn.softmax))

#     model.compile(optimizer='adam',
#                      loss='categorical_crossentropy',
#                      metrics=['accuracy'])
#     return model
