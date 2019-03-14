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

The header is encoded as:


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

## How to Run From Command Line

### Command Line Parameters

Parameters:

### To Encode Using Command Line


### To Decode using Command Line

## Run the Tests

```
nosetests --with-coverage --cover-package=steganography
```

