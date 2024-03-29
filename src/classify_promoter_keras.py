#!/usr/bin/env python
# coding: utf-8

# In[2]:


#!pip install --upgrade ipython

get_ipython().system('pip install --upgrade pip')


# In[3]:


####### import libraries and modules ########
from seq_reader import load_data        # parsing data file
from one_hot_rep import get_rep_mats, conv_labels   # converting to correct format
#from ipynb.fs.full.seq_reader import load_data
#from ipynb.fs.full.one_hot_rep import get_rep_mats, conv_labels


# In[4]:


import numpy as np
np.random.seed(123)  # for reproducibility


# In[5]:


from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils
from keras.datasets import mnist
#############################################


# In[6]:


# 1. Load data into train and test sets
X, y = load_data("../data/promoters.data.txt")   # sequences, labels
X = get_rep_mats(X)     # convert to array of representation matrices
############


# In[ ]:


for i in X:
    for idx, j in enumerate(i):
        i[idx] = j[0]
############


# In[ ]:


y = conv_labels(y, "promoter")      # convert to integer labels
X = np.asarray(X)       # work with np arrays
y = np.asarray(y)
X_train = X[0:90]
X_test = X[90:]
y_train = y[0:90]
y_test = y[90:]


# In[ ]:


# 2. Preprocess input data
X_train = X_train.reshape(X_train.shape[0], 1, 55, 64)  # (90, 55, 64) --> (90, 1, 55, 64)
X_test = X_test.reshape(X_test.shape[0], 1, 55, 64)
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')


# In[ ]:


# 3. Preprocess class labels; i.e. convert 1-dimensional class arrays to 3-dimensional class matrices
Y_train = np_utils.to_categorical(y_train, 2)
Y_test = np_utils.to_categorical(y_test, 2)


# In[ ]:


# 4. Define model architecture
model = Sequential()

model.add(Convolution2D(54, 3, 3, activation='relu', input_shape=(1, 55, 64)))
model.add(Convolution2D(54, 3, 3, activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(2, activation='softmax'))   # since 2 classes


# In[ ]:


# 5. Compile model
model.compile(loss='categorical_crossentropy',
                optimizer='adam',
                metrics=['accuracy'])


# In[ ]:


# 6. Fit model on training data
model.fit(X_train, Y_train,validation_data=(X_test,Y_test),
              batch_size=32, nb_epoch=10, verbose=1)



# 7. Evaluate model on test data
score = model.evaluate(X_test, Y_test, verbose=1)
print ("score = " + str(score))

