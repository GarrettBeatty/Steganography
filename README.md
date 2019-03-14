# Steganography

[![Build Status](https://travis-ci.org/GarrettBeatty/Steganography.svg?branch=master)](https://travis-ci.org/GarrettBeatty/Steganography)
[![Coverage Status](https://coveralls.io/repos/github/GarrettBeatty/Steganography/badge.svg?branch=master)](https://coveralls.io/github/GarrettBeatty/Steganography?branch=master)


See it in action at [encode.gbt.codes](http://encode.gbt.codes).

Original:

![alt text](images/city.jpg "original")

Original with Encoded Hidden Message:

![alt text](images/encoded.png "encoded")

Decoded Hidden Message:

![alt text](images/message.jpeg "decoded")

## How It Works

### Supported Source Images
* Image File
* Array

### Supported Message Types
* Image File
* Text File
* Text Stream
* Text
* Array

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

The header is encoded as:

* bit split (4 bits)
* padding (4 bits)
* message length (32 bits)
* message type (2 bits)
* num extras (4 bits)
* extras (16 bits each)

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

## Using the Library in Python

Look at `tests/test_steganography.py` for examples.

## How to Run From Command Line

### Command Line Parameters

Parameters:
* --source Path to source file
* --source-type: Source type: 'image'
* --message: Image file, Text File, or String
* --message-type: Message type: 'text', 'text_file,, 'image'
* --encode: Will encode if flag is set
* --decode: Will decode if flag is set
* --bit-split: (Optional, default is 2) Number of least significant bits to use to encode message.
* --output: Output file

### To Encode Using Command Line

```
python3 cli.py --source <source> --encode --message <message> --bit-split <bitsplit> --output <output> --source-type <source-type> --message-type <message-type>
```
Example:

``` 
python3 cli.py --source images/city.jpg --encode --message images/message.jpeg --bit-split 2 --output images/encoded.png --source-type image --message-type image
```

### To Decode using Command Line

```
python3 cli.py --source <source> --decode --output <output> --source-type <source-type>
```
Example:
``` 
python3 cli.py --source images/encoded.png --decode --output ~/Desktop/garrett.png --source-type image
```

## Run the Tests

```
nosetests --with-coverage --cover-package=steganography
```

