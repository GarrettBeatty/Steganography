import numpy as np

from .message import Message
from .source import Source

class Steganography:

    type_map = {
        'array': '00',
        'text': '01',
        'text_file': '01',
        'text_stream': '01',
        'image': '10',
    }

    inv_type_map = {
        '00': 'array',
        '01': 'text',
        '10': 'image'
    }

    @staticmethod
    def decode(source, source_type='array'):

        if source_type == 'array':
            source, source_original_shape = Source.from_array(source)
        elif source_type == 'image':
            source, source_original_shape = Source.from_image(source)
        else:
            raise Exception('Source type not valid', source_type)

        offset = 0
        bit_split = source[: offset + 4, -1:]
        bit_split = bit_split.squeeze()
        bit_split = "".join(str(num) for num in bit_split)
        bit_split = int(bit_split, 2)
        offset = offset + 4

        padding = source[offset: offset + 4, -1:]
        padding = padding.squeeze()
        padding = "".join([str(num) for num in padding])
        padding = int(padding, 2)
        offset = offset + 4

        message_length = source[offset: offset + 32, -1:]
        message_length = message_length.squeeze()
        message_length = "".join([str(num) for num in message_length])
        message_length = int(message_length, 2)
        offset = offset + 32

        message_type = source[offset: offset + 2, -1:]
        message_type = message_type.squeeze()
        message_type = "".join([str(num) for num in message_type])
        message_type = Steganography.inv_type_map[message_type]
        offset = offset + 2

        num_extras = source[offset: offset + 4, -1:]
        num_extras = num_extras.squeeze()
        num_extras = "".join([str(num) for num in num_extras])
        num_extras = int(num_extras, 2)
        offset = offset + 4

        extras = []
        for extra in range(num_extras):
            extra = source[offset: offset + 16, -1:]
            extra = extra.squeeze()
            extra = "".join([str(num) for num in extra])
            extras.append(int(extra, 2))
            offset = offset + 16

        message = source[offset: offset + message_length, -bit_split:]
        message = message.reshape((-1,))[:-padding]
        message = np.packbits(message)
        return message, message_type, extras

    @staticmethod
    def encode(source, message, bit_split, source_type='array', message_type='array'):

        if bit_split > 8:
            raise Exception("Bit Split must be >= 1 and <= 8")

        if source_type == 'array':
            source, source_original_shape = Source.from_array(source)
        elif source_type == 'image':
            source, source_original_shape = Source.from_image(source)
        else:
            raise Exception('Source type not valid', source_type)

        if message_type == 'array':
            (message, padding), message_extras = Message.from_array(message, bit_split)
        elif message_type == 'image':
            (message, padding), message_extras = Message.from_image(message, bit_split)
        elif message_type == 'text':
            (message, padding), message_extras = Message.from_text(message, bit_split)
        elif message_type == 'text_file':
            (message, padding), message_extras = Message.from_text_file(message, bit_split)
        elif message_type == 'text_stream':
            (message, padding), message_extras = Message.from_text_stream(message, bit_split)
        else:
            raise Exception('Message type not valid', message_type)

        bit_split_str = "{0:04b}".format(bit_split)
        padding = "{0:04b}".format(padding)
        message_length = "{0:032b}".format(message.shape[0])  # message height
        mt = Steganography.type_map[message_type]

        extras = []
        for extra in message_extras:
            e = "{0:016b}".format(extra)
            extras.append(e)

        num_extras = "{0:04b}".format(len(extras))

        header = [bit_split_str, padding, message_length, mt, num_extras]
        header.extend(extras)

        header = np.array(list("".join(header)))
        header = np.expand_dims(header, axis=1)

        if header.shape[0] + message.shape[0] > source.shape[0]:
            e = (
                "Message size too large!",
                str(header.shape[0] + message.shape[0]),
                ">",
                str(source.shape[0]),
            )
            raise Exception(e)

        # write header
        encoded = np.copy(source)
        encoded[: header.shape[0], -1:] = header

        # write message
        offset = header.shape[0]
        encoded[
        offset: offset + message.shape[0], -bit_split:
        ] = message

        # converts back to regular numbers and reshapes to original size
        encoded = np.packbits(encoded)
        encoded = encoded.reshape(source_original_shape)

        return encoded
