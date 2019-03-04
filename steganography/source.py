import numpy as np
from PIL import Image

class Source:


    def __init__(self, source, source_type):
        """

        :param source: Source Image
        :type source: Path to image, File, etc
        :param source_type: Source Type: 'image'
        :type source_type: str
        """

        if source_type == 'image':
            source = Image.open(source)
        else:
            raise Exception('Source Type not supported')

        source = np.array(source, dtype=np.uint8)
        self.orig_source_shape = source.shape
        self.source = np.unpackbits(source)
        self.source = self.source.reshape((-1, 8))
        self.source_type = source_type

