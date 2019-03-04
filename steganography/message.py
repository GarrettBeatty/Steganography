import numpy as np
from PIL import Image

class Message:

    @staticmethod
    def convert_to_type(encoded, message_type, extras):
        if message_type == 'image':
            try:
                message = encoded.reshape((extras[0], extras[1], 3))
            except:
                message = encoded.reshape((extras[0], extras[1], 4))
            m = Image.fromarray(message)
        elif message_type == 'text':
            m = ''.join(chr(x) for x in encoded)
        return m

    def __init__(self, message, message_type):
        """
        
        :param message: 
        :type message: 
        :param message_type:
        :type message_type:
        """
        self.extras = []
        self.orig_message = message
        if message_type == 'image':
            self.message_type = 'image'
            message = Image.open(message)
            self.extras.append(message.size[1])
            self.extras.append(message.size[0])
        elif message_type == 'image_array':
            self.message_type = 'image'
            self.extras.append(message.size[1])
            self.extras.append(message.size[0])
        elif message_type == 'text':
            self.message_type = 'text'
            message = [ord(x) for x in message]
        elif message_type == 'text_file':
            self.message_type = 'text'
            with open(message, 'r') as f:
                m = []
                for line in f:
                    for char in line:
                        m.append(ord(char))
            self.message = m
        elif message_type == 'text_stream':
            self.message_type = 'text'
            message.seek(0)
            m = message.read()
            m = m.decode('ascii')
            message = m
        else:
            raise Exception('Message Type not supported', message_type)

        message = np.array(message, dtype=np.uint8)
        self.message = np.unpackbits(message)
        self.padding = 0

    def pad_and_reshape_message(self, bit_split):
        self.padding = bit_split - self.message.shape[0] % bit_split
        self.message = np.pad(self.message, (0, self.padding), mode='constant')
        self.message = self.message.reshape(-1, bit_split)