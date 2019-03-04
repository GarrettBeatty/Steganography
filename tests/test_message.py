import unittest
import tempfile

from werkzeug.datastructures import FileStorage

from steganography.message import Message


class TestMessage(unittest.TestCase):

    def test_text_stream(self):
        f = tempfile.NamedTemporaryFile(delete=False)
        f.write(b'testing')
        fs = FileStorage(f)
        _ = Message(fs, message_type='text_stream')
        f.close()
