# mystery-meme
experimental steganography encoder/decoder

Input data is split into two bit chunks and encoded in the least significant bits of the green and blue channels' pixel data. Pixels are chosen based on a pattern generated from a provided seed value

# usage

It should work with any image format Pillow/PIL supports.

python encode.py -d data-to-hide.txt -i source-image.png -o exported-image.png -s 1234(seed) 

python decode.py -i exported-image.png -o plaintext.txt -s 1234(seed) 



python imageviewer.py image.png

Image viewer controls:

Quit - q / escape
Zoom - + / -


# dependencies

tested using python 3.8.6

python -m pip install pillow pygame==2.0.0.dev12
