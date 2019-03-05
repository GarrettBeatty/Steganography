from distutils.core import setup

setup(name='steganography',
      version='1.0',
      description='Encode and Decode Messages',
      url='https://github.com/GarrettBeatty/Steganography',
      author='Garrett Beatty',
      author_email='garrett@gbt.codes',
      license='MIT',
      packages=['steganography'],
      install_requires=[
          'Werkzeug>=0.14.1',
          'numpy>=1.16.1',
          'Pillow>=5.4.1'
      ])