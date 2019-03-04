import argparse
import os

from PIL import Image

from steganography.message import Message
from steganography.source import Source
from steganography.steganography import Steganography

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=str, help="Source Image", required=True)
    parser.add_argument("--message", type=str, help="Message")
    parser.add_argument("--message-type", type=str, help="Message Type")
    parser.add_argument("--source-type", type=str, help="Source Type", required=True)
    parser.add_argument("--bit-split", type=int, help="Bit Split", default=2)
    parser.add_argument("--encode", action='store_true')
    parser.add_argument("--decode", action='store_true')
    parser.add_argument("--output", type=str, required=True)

    args = parser.parse_args()

    if args.encode:
        if not args.message or not args.source_type or not args.message_type:
            parser.error('Must include --message, --source-type, and --message-type')

        source = Source(args.source, args.source_type)
        message = Message(args.message, args.message_type)
        encoded = Steganography.encode(source, message, args.bit_split)
        image_encoded = Image.fromarray(encoded)

        fp = args.output
        os.makedirs(os.path.dirname(os.path.abspath(fp)), exist_ok=True)
        image_encoded.save(fp, format='png')
        print('File saved to', fp)

    elif args.decode:
        source = Source(args.source, args.source_type)
        message, message_type, extras = Steganography.decode(source)

        message = Message.convert_to_type(message, message_type, extras)
        fp = args.output

        os.makedirs(os.path.dirname(os.path.abspath(fp)), exist_ok=True)

        if message_type == 'image':
            message.save(fp, format='png')
        else:
            with open(fp, 'w') as f:
                f.write(message)

        print('File saved to', fp)

    else:
        parser.print_help()
