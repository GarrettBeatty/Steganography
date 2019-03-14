import numpy as np
from PIL import Image


class Source:

    @staticmethod
    def from_image(filename):
        source = np.array(Image.open(filename), dtype=np.uint8)
        return Source.from_array(source)

    @staticmethod
    def from_array(array):
        source = np.array(array, dtype=np.uint8)
        original_shape = source.shape
        source = np.unpackbits(source)
        source = source.reshape((-1, 8))
        return source, original_shape
