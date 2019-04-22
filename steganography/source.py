import numpy as np
from PIL import Image


class Source:
    @staticmethod
    def from_image(filename):
        """
        Reads an image file and converts it to the right source format.

        :param filename: Image file
        :type filename: str, File
        :return: Properly reshaped source, original_shape
        :rtype: numpy.array, tuple
        """
        source = np.array(Image.open(filename), dtype=np.uint8)
        return Source.from_array(source)

    @staticmethod
    def from_array(array):
        """
        Reads an array and converts it to the right source format.

        :param array: Array
        :type array: numpy.array
        :return: Properly reshaped source, original_shape
        :rtype: numpy.array, tuple
        """
        source = np.array(array, dtype=np.uint8)
        original_shape = source.shape
        source = np.unpackbits(source)
        source = source.reshape((-1, 8))
        return source, original_shape
