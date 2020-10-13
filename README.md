# mystery-meme
experimental steganography encoder/decoder

data is hidden in pixel data, in the least significant bits of the green and blue channels. Pixels are chosen based on a pattern generated from a provided seed value

# usage

It should work with any (common) image format that pillow/PIL supports.

python encode.py -d data-to-hide.txt -i source-image.png -o exported-image.png -s 1234(seed) 

python decode.py -i exported-image.png -o plaintext.txt -s 1234(seed) 



python imageviewer.py image.png


# dependencies

tested using python 3.8.6

python -m pip install pillow pygame==2.0.0.dev12
