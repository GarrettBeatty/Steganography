import numpy as np
from PIL import Image

class Source:

    def __init__(self, source, source_type):
        if source_type == 'image':
            source = Image.open(source)
        else:
            raise Exception('Source Type not supported')

        source = np.array(source, dtype=np.uint8)
        self.orig_source_shape = source.shape
        self.source = np.unpackbits(source)
        self.source = self.source.reshape((-1, 8))
        self.source_type = source_type

