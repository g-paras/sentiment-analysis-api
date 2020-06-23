from keras.datasets import imdb
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.models import load_model
import re
from nltk.tokenize import word_tokenize
import nltk
import numpy as np
import numpy

numpy.random.seed(7)

top_words = 5000
(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words = top_words)

word2id = imdb.get_word_index()
id2word = {i:word for word, i in word2id.items()}
print('---review with words---')
print([id2word.get(i,"") for i in x_train[6]])
print('---label---')
print(y_train[6])

print('Maximum review length: {}'.format(len(max((x_train + x_test), key = len))))

print('Minimum review length: {}'.format(len(min((x_train+ x_test), key = len))))

max_review_length = 500
x_train = sequence.pad_sequences(x_train,maxlen = max_review_length)
x_test = sequence.pad_sequences(x_test, maxlen = max_review_length)

#creating model
embedding_vector_length = 32
model = Sequential()
model.add(Embedding(top_words, embedding_vector_length, input_length = max_review_length))
model.add(Dropout(0.2))
model.add(LSTM(100))
model.add(Dropout(0.2))
model.add(Dense(1, activation = 'sigmoid'))

model.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics = ['accuracy'])
print(model.summary)
model.fit(x_train, y_train, validation_data = (x_test, y_test), epochs = 10, batch_size = 64)

scores = model.evaluate(x_test, y_test, verbose = 0)
print('Accuracy: %2f%%' % (scores[1]*100))

!pip install -U -q PyDrive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

model.save('model.h5')
model_file = drive.CreateFile({'title':'model.h5'})
model_file.SetContentFile('model.h5')
model_file.Upload()

model = load_model('model.h5')

text = input().split()
x_test = [[word2id[word] for word in text]]
vector = np.array([x_test]).flatten()
prob = model.predict(np.array([vector][0]))[0][0]
print(prob)
