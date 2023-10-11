import asyncio
import numpy as np
import tensorflow as tf
from generator.model import restore_model

from aiohttp import web

import socketio

# create a Socket.IO server
sio = socketio.AsyncServer(cors_allowed_origins='*')

# wrap with ASGI application
# app = socketio.ASGIApp(sio)
app = web.Application()

# attach application to server
sio.attach(app)

# get tokenizer functions
# path_to_file = 'data/usable_data_nekfeu.txt'
# ids_from_chars, chars_from_ids = tokenizer(path_to_file)

# get generator functions
path_to_model = 'model/'
model = restore_model(path_to_model)
print(model.tensorflow_version)
inputs = tf.constant(['Hi', '', '', '', ''])
model.generate_one_step(
    inputs=inputs, states=None)

# create a generator
# generator = OneStep(model, chars_from_ids, ids_from_chars)


# event handler for new connections


@sio.event
async def connect(sid, environ):
    print("connect ", sid)
    # sio.emit('config', config.as_dict())

threshold = 0.995
min_threshold = 0.935
end_punctuations = ['.', '?', '!']


async def genarate(model, seed: str, length: int) -> str:
    result = [seed, '', '', '', '']
    await sio.emit('responding', {"status": True})
    print("responding: ", True)
    await asyncio.sleep(0.25)

    states = None
    next_char = tf.constant(result)

    for n in range(length):
        next_char, states = model.generate_one_step(
            inputs=next_char, states=states)

        # next_char = 'a'
        await asyncio.sleep(0.075)

        letter = tf.strings.join([next_char])[0].numpy().decode("utf-8")
        await sio.emit('next_char', {"next_char": letter})

        result.append(next_char)

        if len(result) > 2:

            next_word = np.argmax(states[0])
            # print("threshold: ", states[0][next_word])
            # print("state: ", states[0][next_word] < threshold)

            # print(type(states))
            # print(bool(states[0][next_word] < threshold))

            # if states > min_certitude or letter in end_punctuations and n > length/2:
            if bool(states[0][next_word] < threshold) and (letter in end_punctuations):
                break
            if bool(states[0][next_word] < min_threshold):
                break

    await sio.emit('responding', {"status": False})
    print("responding: ", False)

    return ''.join(tf.strings.join(result)[0].numpy().decode("utf-8"))


@sio.on('message')
async def message(sid, data):
    print("message ", data)
    if 'message' in data:
        await genarate(model, data['message'], data.get('size', 750))


if __name__ == '__main__':
    web.run_app(app)
