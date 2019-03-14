import numpy as np
from PIL import Image


class Message:

    @staticmethod
    def from_image(filename, bit_split):
        message = Image.open(filename)
        message = np.array(message, dtype=np.uint8)
        return Message.from_array(message, bit_split)

    @staticmethod
    def from_array(array, bit_split):
        message = np.array(array, dtype=np.uint8)
        return Message.pad_and_reshape_message(np.unpackbits(message), bit_split), message.shape

    @staticmethod
    def from_text(text, bit_split):
        message = [ord(x) for x in text]
        message = np.array(message, dtype=np.uint8)
        return Message.from_array(message, bit_split)

    @staticmethod
    def from_text_file(filename, bit_split):
        with open(filename, 'r') as f:
            m = []
            for line in f:
                for char in line:
                    m.append(ord(char))
        message = np.array(m, dtype=np.uint8)
        return Message.from_array(message, bit_split)

    @staticmethod
    def from_text_stream(stream, bit_split):
        stream.seek(0)
        m = stream.read()
        m = m.decode('ascii')
        message = [ord(x) for x in m]
        message = np.array(message, dtype=np.uint8)
        return Message.from_array(message, bit_split)

    @staticmethod
    def pad_and_reshape_message(message, bit_split):


        padding = bit_split - message.shape[0] % bit_split
        message = np.pad(message, (0, padding), mode='constant')
        message = message.reshape(-1, bit_split)
        return message, padding
