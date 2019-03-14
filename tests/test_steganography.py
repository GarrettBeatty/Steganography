import tempfile
import unittest

import numpy as np
from PIL import Image
from werkzeug.datastructures import FileStorage

from steganography.steganography import Steganography


class TestMessageTypes(unittest.TestCase):

    def test_message_text(self):
        message = 'hi'
        encoded = Steganography.encode('test_data/city.jpg', message, 2, 'image', 'text')
        decoded = Steganography.decode(encoded)[0]
        decoded_text = ''.join(chr(x) for x in decoded)
        assert decoded_text == message

    def test_message_image(self):
        message = 'test_data/message.jpeg'
        message_array = np.array(Image.open(message))
        encoded = Steganography.encode('test_data/city.jpg', message, 2, 'image', 'image')
        decoded_image, _, shape = Steganography.decode(encoded)
        decoded_image = decoded_image.reshape(shape)
        assert np.array_equal(decoded_image, message_array)

    def test_message_array(self):
        message = np.random.randint(0, 100, size=(100, 2))
        encoded = Steganography.encode('test_data/city.jpg', message, 2, 'image', 'array')
        decoded_array, _, shape = Steganography.decode(encoded)
        decoded_array = decoded_array.reshape(shape)
        assert np.array_equal(decoded_array, message)

    def test_message_text_stream(self):
        f = tempfile.NamedTemporaryFile(delete=False)
        f.write(b'testing')
        message = FileStorage(f)
        encoded = Steganography.encode('test_data/city.jpg', message, 2, 'image', 'text_stream')
        decoded = Steganography.decode(encoded)[0]
        decoded_text = ''.join(chr(x) for x in decoded)
        assert decoded_text == 'testing'
        f.close()


class TestSourceTypes(unittest.TestCase):
    def test_source_array(self):
        message = 'hi'
        source = np.random.randint(0, 100, size=(400, 300, 3))
        encoded = Steganography.encode(source, message, 2, 'array', 'text')
        decoded = Steganography.decode(encoded)[0]
        decoded_text = ''.join(chr(x) for x in decoded)
        assert decoded_text == message

    def test_source_image(self):
        message = 'hi'
        encoded = Steganography.encode('test_data/city.jpg', message, 2, 'image', 'text')
        decoded = Steganography.decode(encoded)[0]
        decoded_text = ''.join(chr(x) for x in decoded)
        assert decoded_text == message
