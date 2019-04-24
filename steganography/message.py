import numpy as np
from PIL import Image


class Message:
    @staticmethod
    def from_image(filename, bit_split):
        """
        Reads an image file and converts it to the right message format.

        :param filename: Image file
        :type filename: str, File
        :param bit_split: Bit split
        :type bit_split: int
        :return: Padded and reshaped message, padding, original shape
        :rtype: numpy.array, int, tuple
        """
        message = Image.open(filename)
        message = np.array(message, dtype=np.uint8)
        return Message.from_array(message, bit_split)

    @staticmethod
    def from_array(array, bit_split):
        """
        Reads an array and converts it to the right message format.

        :param array: Array
        :type array: numpy.array
        :param bit_split: Bit split
        :type bit_split: int
        :return: Padded and reshaped message, padding, original shape
        :rtype: numpy.array, int, tuple
        """
        message = np.array(array, dtype=np.uint8)
        return (
            Message.pad_and_reshape_message(np.unpackbits(message), bit_split),
            message.shape,
        )

    @staticmethod
    def from_text(text, bit_split):
        """
        Reads text and converts it to the right message format.

        :param text: Text
        :type text: str
        :param bit_split: Bit split
        :type bit_split: int
        :return: Padded and reshaped message, padding, original shape
        :rtype: numpy.array, int, tuple
        """
        message = [ord(x) for x in text]
        message = np.array(message, dtype=np.uint8)
        return Message.from_array(message, bit_split)

    @staticmethod
    def from_text_file(filename, bit_split):
        """
        Reads a text file and converts it to the right message format.

        :param filename: Text file
        :type filename: str, File
        :param bit_split: Bit split
        :type bit_split: int
        :return: Padded and reshaped message, padding, original shape
        :rtype: numpy.array, int, tuple
        """
        with open(filename, "r") as f:
            m = []
            for line in f:
                for char in line:
                    m.append(ord(char))
        message = np.array(m, dtype=np.uint8)
        return Message.from_array(message, bit_split)

    @staticmethod
    def from_text_stream(stream, bit_split):
        """
        Reads text stream converts it to the right message format.

        :param stream: Stream
        :type stream: stream
        :param bit_split: Bit split
        :type bit_split: int
        :return: Padded and reshaped message, padding, original shape
        :rtype: numpy.array, int, tuple
        """
        stream.seek(0)
        m = stream.read()
        m = m.decode("ascii")
        message = [ord(x) for x in m]
        message = np.array(message, dtype=np.uint8)
        return Message.from_array(message, bit_split)

    @staticmethod
    def pad_and_reshape_message(message, bit_split):
        """
        Pads and reshapes a message to the correct format.

        :param message: Message to pad and reshaped
        :type message: numpy.array
        :param bit_split: Bit split
        :type bit_split: int
        :return: Padded and reshaped message, padding, original shape
        :rtype: numpy.array, int, tuple
        """

        padding = bit_split - message.shape[0] % bit_split
        message = np.pad(message, (0, padding), mode="constant")
        message = message.reshape(-1, bit_split)
        return message, padding
