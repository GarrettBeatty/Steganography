import numpy as np

class Steganography:

    type_maps = {
        '00': 'image',
        '11': 'text'
    }

    inv_type_maps = {v: k for k, v in type_maps.items()}

    @staticmethod
    def decode(source):
        """
        Decodes source

        :param source: Source
        :type source: Source
        :return: message, message_type, extras
        :rtype: Message, str, list
        """

        offset = 0
        bit_split = source.source[:offset + 4, -1:]
        bit_split = bit_split.squeeze()
        bit_split = ''.join(str(num) for num in bit_split)
        bit_split = int(bit_split, 2)
        offset = offset + 4

        padding = source.source[offset:offset + 4, -1:]
        padding = padding.squeeze()
        padding = ''.join([str(num) for num in padding])
        padding = int(padding, 2)
        offset = offset + 4

        message_length = source.source[offset:offset + 32, -1:]
        message_length = message_length.squeeze()
        message_length = ''.join([str(num) for num in message_length])
        message_length = int(message_length, 2)
        offset = offset + 32

        message_type = source.source[offset:offset + 2, -1:]
        message_type = message_type.squeeze()
        message_type = ''.join([str(num) for num in message_type])
        message_type = Steganography.type_maps[message_type]
        offset = offset + 2

        num_extras = source.source[offset:offset + 4, -1:]
        num_extras = num_extras.squeeze()
        num_extras = ''.join([str(num) for num in num_extras])
        num_extras = int(num_extras, 2)
        offset = offset + 4

        extras = []
        for extra in range(num_extras):
            extra = source.source[offset:offset + 16, -1:]
            extra = extra.squeeze()
            extra = ''.join([str(num) for num in extra])
            extras.append(int(extra, 2))
            offset = offset + 16

        message = source.source[offset:offset + message_length, -bit_split:]
        message = message.reshape((-1,))[:-padding]
        message = np.packbits(message)
        return message, message_type, extras

    @staticmethod
    def encode(source, message, bit_split):
        """

        :param source: Source
        :type source: Source
        :param message: Message
        :type message: Message
        :param bit_split: Bit split
        :type bit_split: int
        :return: Encoded source
        :rtype: numpy array
        """

        if bit_split > 8:
            raise Exception('Bit Split must be >= 1 and <= 8')

        message.pad_and_reshape_message(bit_split)

        bit_split_str = '{0:04b}'.format(bit_split)
        padding = '{0:04b}'.format(message.padding)
        message_length = '{0:032b}'.format(message.message.shape[0])  # message height
        message_type = Steganography.inv_type_maps[message.message_type]

        extras = []
        for extra in message.extras:
            e = '{0:016b}'.format(extra)
            extras.append(e)

        num_extras = '{0:04b}'.format(len(extras))

        header = [
            bit_split_str,
            padding,
            message_length,
            message_type,
            num_extras
        ]

        header.extend(extras)

        header = np.array(list(''.join(header)))
        header = np.expand_dims(header, axis=1)

        if header.shape[0] + message.message.shape[0] > source.source.shape[0]:
            e = 'Message size too large!', str(header.shape[0] + message.message.shape[0]), '>', str(
                source.source.shape[0])
            raise Exception(e)

        # write header
        encoded = np.copy(source.source)
        encoded[:header.shape[0], -1:] = header

        # write message
        offset = header.shape[0]
        encoded[offset:offset + message.message.shape[0], -bit_split:] = message.message

        # converts back to regular numbers and reshapes to original size
        encoded = np.packbits(encoded)
        encoded = encoded.reshape(source.orig_source_shape)

        return encoded

