import numpy as np
from PIL import Image


class Message:
    @staticmethod
    def convert_to_type(encoded, message_type, extras):
        """
        Converts the numpy array message back to original type

        :param encoded: Encoded message
        :type encoded: numpy array
        :param message_type: Message type: 'image' or 'text'
        :type message_type: str
        :param extras: List of parameters used to help format message
        :type extras: list
        :return:
        :rtype:
        """
        if message_type == "image":
            try:
                message = encoded.reshape((extras[0], extras[1], 3))
            except:
                message = encoded.reshape((extras[0], extras[1], 4))
            m = Image.fromarray(message)
        elif message_type == "text":
            m = "".join(chr(x) for x in encoded)
        return m

    def __init__(self, message, message_type):
        """
        
        :param message: Message to encode
        :type message: Path to image, Path to text file, numpy array, str, or Stream of text
        :param message_type: Message Type: 'image', 'image_array', 'text', 'text_file', or 'text_stream'
        :type message_type: str
        """
        self.extras = []
        self.orig_message = message
        if message_type == "image":
            self.message_type = "image"
            message = Image.open(message)
            self.extras.append(message.size[1])
            self.extras.append(message.size[0])
        elif message_type == "image_array":
            self.message_type = "image"
            self.extras.append(message.shape[1])
            self.extras.append(message.shape[0])
        elif message_type == "text":
            self.message_type = "text"
            message = [ord(x) for x in message]
        elif message_type == "text_file":
            self.message_type = "text"
            with open(message, "r") as f:
                m = []
                for line in f:
                    for char in line:
                        m.append(ord(char))
            self.message = m
        elif message_type == "text_stream":
            self.message_type = "text"
            message.seek(0)
            m = message.read()
            m = m.decode("ascii")
            message = [ord(x) for x in m]
        else:
            raise Exception("Message Type not supported", message_type)

        message = np.array(message, dtype=np.uint8)
        self.message = np.unpackbits(message)
        self.padding = 0

    def pad_and_reshape_message(self, bit_split):
        """
        Pads and reshapes the message

        :param bit_split: Bit split
        :type bit_split: int
        """
        self.padding = bit_split - self.message.shape[0] % bit_split
        self.message = np.pad(self.message, (0, self.padding), mode="constant")
        self.message = self.message.reshape(-1, bit_split)
