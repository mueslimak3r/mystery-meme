# mystery-meme
experimental steganography encoder/decoder

currently uses basic linear LSB encoding. Switching to pseudo-random data distribution is WIP

# usage

It should work with any (common) image format that pillow/PIL supports.

python3 encode.py -d data-to-hide.txt -i source-image.png -o exported-image.png

python3 decode.py -i exported-image.png -o plaintext.txt


# dependencies

pillow
