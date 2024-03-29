#!/usr/bin/env python
# coding: utf-8

# In[1]:


####### import libraries and modules ########
from seq_reader import load_data        # parsing data file
from one_hot_rep import get_rep_mats, conv_labels   # converting to correct format

from sklearn.model_selection import StratifiedKFold     # cross validation

import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils
from keras.datasets import mnist
from keras.layers.normalization import BatchNormalization

#############################################


# In[2]:


seed = 123          # for reproducibility
np.random.seed(seed)


# In[3]:


# 1. Load data into train and test sets
X, y = load_data("../data/splice.data.txt")   # sequences, labels
X = get_rep_mats(X)     # convert to array of representation matrices
for i in X:             # CUSTOM reshape
    for idx, j in enumerate(i):
        i[idx] = j[0]
y = conv_labels(y)      # convert to integer labels
X = np.asarray(X)       # work with np arrays
Y = np.asarray(y)


# In[ ]:


# define 10-fold cross validation test harness
kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed)
scores = []

for train, test in kfold.split(X, Y):
    print ("====> FOLD [" + str(len(scores) + 1) + "]")
    
        # 2. Preprocess input data
    X_train = X[train].reshape(X[train].shape[0], 1,58, 64)
    X_test = X[test].reshape(X[test].shape[0], 1,58, 64)
    X_train = X_train.astype('float32')
    X_test = X_test.astype('float32')
    
    # 3. Preprocess class labels; i.e. convert 1-dimensional class arrays to 3-dimensional class matrices
    Y_train = np_utils.to_categorical(Y[train], 3)   # goes from (2872,) to (2872, 3)
    Y_test = np_utils.to_categorical(Y[test], 3)

    # 4. Define model architecture
    model = Sequential()
    

    #1st Convolution Layer
    model.add(Convolution2D(96, (3, 3), activation='relu', input_shape=(1, 58, 64), data_format='channels_first'))
    print (model.output_shape)
    model.add(MaxPooling2D(pool_size=(2,2)))
    #2nd Convolution Layer
    model.add(Convolution2D(256, (3, 3), activation='relu',data_format='channels_first'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    
    #3rd Convolution Layer
    model.add(Convolution2D(384, (3, 3), activation='relu', data_format='channels_first' ))
    
    #4th Convultion Layer
    model.add(Convolution2D(384, (3, 3), activation='relu', data_format='channels_first' ))
    #5th Convolution Layer
    model.add(Convolution2D(256, (3, 3), activation='relu', data_format='channels_first' ))
    model.add(MaxPooling2D(pool_size=(2,2)))

    #model.add(Dropout(0.25))

    model.add(Flatten())
    #1st Dense layer
    model.add(Dense(4096, activation='relu'))
    model.add(Dropout(0.4))
    
    #2nd dense Layer
    model.add(Dense(4096, activation='relu'))
    model.add(Dropout(0.4))
    #3rd dense Layer
    model.add(Dense(1000, activation='relu'))
    model.add(Dropout(0.4))
              
    #output layer    
    model.add(Dense(3, activation='softmax'))
    # 5. Compile model
    model.compile(loss='categorical_crossentropy',
                    optimizer='adam',
                    metrics=['accuracy'])

    # 6. Fit model on training data
    model.fit(X_train, Y_train,validation_data=(X_test,Y_test),
                  batch_size=32, epochs=1, verbose=1)

    # 7. Evaluate model on test data
    score = model.evaluate(X_test, Y_test, verbose=1)
    scores.append(score[1]*100)     # accuracies only
    print ("\nscore = " + str(score))
    
# output aggregate results
print("min: %.2f%%, average: %.2f%% (+/- %.2f%%), max: %.2f%%" % (np.min(scores), np.mean(scores), np.std(scores), np.max(scores)))


# In[ ]:




