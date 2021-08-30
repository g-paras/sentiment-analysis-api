import numpy as np
from keras.models import load_model
from keras.callbacks import LambdaCallback
from keras.datasets import imdb
from keras.layers import Dense, Embedding, GlobalAveragePooling1D
from keras.models import Sequential
from keras.preprocessing.sequence import pad_sequences
import matplotlib.pyplot as plt

# This model was used in early stage of this project and used as a reference, learned from coursesa project

(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=10000)

print(x_train[0])

print(y_train[0])

class_names = ['Negative', 'Positive']

word_index = imdb.get_word_index()
print(word_index['hello'])


reverse_word_index = dict((value, key) for key, value in word_index.items())


def decode(review):
    text = ''
    for i in review:
        text += reverse_word_index[i]
        text += ' '
    return text


decode(x_train[0])


def show_lengths():
    print('Length of 1st training example: ', len(x_train[0]))
    print('Length of 2nd training example: ',  len(x_train[1]))
    print('Length of 1st test example: ', len(x_test[0]))
    print('Length of 2nd test example: ',  len(x_test[1]))


word_index['the']


x_train = pad_sequences(
    x_train, value=word_index['the'], padding='post', maxlen=256)
x_test = pad_sequences(
    x_test, value=word_index['the'], padding='post', maxlen=256)

show_lengths()

decode(x_train[0])


model = Sequential([
    Embedding(10000, 16),
    GlobalAveragePooling1D(),
    Dense(16, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['acc']
)

model.summary()


simple_logging = LambdaCallback(on_epoch_end=lambda e, l: print(e, end='.'))

E = 20

h = model.fit(
    x_train, y_train,
    validation_split=0.2,
    epochs=E,
    callbacks=[simple_logging],
    verbose=False
)


plt.plot(range(E), h.history['acc'], label='Training')
plt.plot(range(E), h.history['val_acc'], label='Validation')
plt.legend()
plt.show()

loss, acc = model.evaluate(x_test, y_test)
print('Test set accuracy: ', acc * 100)


prediction = model.predict(np.expand_dims(x_test[0], axis=0))
class_names = ['Negative', 'Positive']
print(class_names[np.argmax(prediction[0])])

print(decode(x_test[0]))

model.save("model.h5")
md = load_model("model.h5")

md.summary()

prediction = md.predict(np.expand_dims(x_test[1], axis=0))
class_names = ['Negative', 'Positive']
print(class_names[np.argmax(prediction[0])])

decode(x_test[1])

# these are samples for manually testing examples
text = "i was working on that project and i find it quiet amazing and funny overall the experience was good and satisfying"
text1 = "working on this was a worst experience for me i hate this very much and wish no one should get though this"
text2 = "you are a waste"
t_list = []

for i in text.split():
    t_list.append(word_index[i])

print(t_list)

prediction = md.predict(np.expand_dims(t_list, axis=0))
class_names = ['Negative', 'Positive']
print(class_names[np.argmax(prediction[0])])
print(prediction)
