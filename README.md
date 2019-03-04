# Steganography

See it in action at [encode.gbt.codes](http://encode.gbt.codes).

Original:

![alt text](images/city.jpg "original")

Original with Encoded Hidden Message:

![alt text](images/encoded.png "encoded")

Decoded Hidden Message:

![alt text](images/message.jpeg "decoded")

## How It Works

### Supported Source Images
* Images (8 bit per channel) (must be PNG)

### Supported Message Types
* RGB Images (assumes 8 bits per channel) (must be PNG)
* Text

### Encoding

This is best explained through an example:

Suppose the source image's bytes were 11110011 01111110
and we wanted to encode the bits  0110 into our image.

We first choose the number of least significant bits to use to encode our message. For this example, we will use 2.

The encoding process looks like this:

11110011 01111110

will transform to 

111100**01** 011111**10**

Notice how we only had to change the 2 least significant bits of the first byte. In the second byte we can keep least significant bits the same because they are the same as the source message.

#### Padding

In order to ensure that the message is divisible by the bit split, the message may need to be padded.
To do this the padding is calculated with `padding = bit_split - (number of bits in hidden message) % bit_split`. Once the value is calculated, that number of 0's is appended to the end of the message.

#### Header

In order to embed the message attributes and encoding info into the image, a header is used.
The header is in the 46 + (32 optional) least significant bits of every byte.

The header is encoded as:
* Bit Split (4 bits)
* Padding (4 bits)
* Message Length (32 bits)
* Message Type (2 bits)
* Number of extras (4 bits)
* Height (optional extra) (16 bits)
* Width (optional extra) (16 bits)


### Decoding

Decoding is simple if the header format is known. The header tells the program what parameters to use to decode the message.

## Installation

Manually Install

```
git clone https://github.com/GarrettBeatty/Steganography.git
cd Steganography
pip3 install -r requirements.txt
pip3 install -e .
```

## Using the Library

Here is an example of hiding an image within another image.

```
from steganography.message import Message
from steganography.source import Source
from steganography.steganography import Steganography

source_image = 'path/to/my/image.jpg
source = Source(source_image, source_type='image')

message_image = 'path/to/my/message.jpg'
message = Message(message_image, message_type='image')

bit_split = 2

encoded = Steganography.encode(source, message, bit_split)

#encoded is a numpy array, need to convert back to an image
image = Image.fromarray(encoded)


```


## How to Run From Command Line

### Command Line Parameters

Parameters:
* --source: Source Image
* --source-type: Source type: 'image'
* --message: Image file, Text File, or String
* --message-type: Message type: 'text', 'text_file, 'text_stream', 'image', or 'image_array'
* --encode: Will encode if flag is set
* --decode: Will decode if flag is set
* --bit-split: (Optional, default is 2) Number of least significant bits to use to encode message.
* --output: Output file

### To Encode Using Command Line

```
python3 cli.py --source <source> --encode --message <message> --bit-split <bitsplit> --output <output> --source-type <source_type> --message-type <message_type>
```

Example:
```
python3 cli.py --source images/city.jpg --encode --message images/message.jpeg --bit-split 8 --output ~/Desktop/output.png --source-type image --message-type image
```

### To Decode using Command Line

```
python3 cli.py --source <source> --decode --output <output> --source-type <source_type>
```

Example:

```
python3 cli.py --source ~/Desktop/source.png --decode --output ~/Desktop/output.png --source-type image
```

## Run the Tests

```
python3 -m unittest discover tests
```

