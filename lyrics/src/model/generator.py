# %% [markdown]
# 

# %% [markdown]
# Imports

# %%
from numpy import array, asarray
from pickle import dump
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Embedding
import tensorflow as tf

# %% [markdown]
# load doc into memory

# %%
def load_doc(filename):
	# open the file as read only
	file = open(filename, 'r', encoding="utf-8")
	# read all text
	text = file.read()
	# close the file
	file.close()
	return text

# %%
# load
# !dir
in_filename = './usable_data.txt'
doc = load_doc(in_filename)
lines = doc.split('\n')

# %% [markdown]
# tokenization

# %%
# integer encode sequences of words
tokenizer = Tokenizer()
tokenizer.fit_on_texts(lines)
sequences = tokenizer.texts_to_sequences(lines)
print(type(sequences), type(sequences[0]), type(sequences[0][0]))

# %%
# vocabulary size
vocab_size = len(tokenizer.word_index) + 1
print('Vocabulary Size: %d' % vocab_size)

# %% [markdown]
# Sequences

# %%
# separate into input and output
# sequences = array(sequences)
X, y = sequences[:][:-1], sequences[:][-1]
# X = sequences[:][:-1]
# y = sequences[:][-1]
# X = [ l[:-1] if len(l) != 0 else 0 for l in sequences]
# y = [ l[-1] if len(l) != 0 else 0 for l in sequences]

# X = array(X, dtype=object)
# y = array(y)
# print(X)
# print(y)
y = to_categorical(y, num_classes=vocab_size)
seq_length = 50 # X.shape[1]
# print(seq_length)

# %% [markdown]
# Define model

# %%
model = Sequential()
model.add(Embedding(vocab_size, 50, input_length=seq_length))
model.add(LSTM(100, return_sequences=True))
model.add(LSTM(100))
model.add(Dense(100, activation='relu'))
model.add(Dense(vocab_size, activation='softmax'))
print(model.summary())

# %% [markdown]
# compile model

# %%
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# %%
[print(i.shape, i.dtype) for i in model.inputs]
[print(o.shape, o.dtype) for o in model.outputs]
[print(l.name, l.input_shape, l.dtype) for l in model.layers]

# %% [markdown]
# Fit model

# %%
# print(X.shape)
# re_x = array(X)
model.fit(X, tf.convert_to_tensor(y, dtype=tf.float64), batch_size=128, epochs=100, verbose=0)

# %% [markdown]
# save the model to file

# %%
model.save('model.h5')

# %% [markdown]
# save the tokenizer

# %%
dump(tokenizer, open('tokenizer.pkl', 'wb'))


