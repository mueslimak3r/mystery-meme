import sys, getopt

import fixedint
from PIL import Image
from pathlib import Path

from generatepattern import generate_pattern

'''
encode_bits

encodes two bits from the source text into the LSBs of the source image's green and blue channels

'''

def encode_bits(g, b, image_pos, input_data, input_data_iter, input_data_bit_iter):

    green_channel_pixel = g.getpixel(image_pos) #
    blue_channel_pixel = b.getpixel(image_pos)  # get g and b byte to modify

    selected_byte = input_data[input_data_iter] # get byte from input data to modify
    
    green_pixel_bitmask = (selected_byte & (0x1 << input_data_bit_iter)) >> input_data_bit_iter            #
    blue_pixel_bitmask = (selected_byte & (0x1 << (input_data_bit_iter + 1))) >> (input_data_bit_iter + 1) # bitshift the two bits from the input data to mask the least significant bits in the g and b pixel bytes

    if green_channel_pixel & 0x1 and green_pixel_bitmask == 0: # flip the bit on or off if needed
        green_channel_pixel -= 1
    else:
        green_channel_pixel |= green_pixel_bitmask

    if blue_channel_pixel & 0x1 and blue_pixel_bitmask == 0:
        blue_channel_pixel -= 1
    else:
        blue_channel_pixel |= blue_pixel_bitmask

    g.putpixel(image_pos, green_channel_pixel) # save the alteration into each color channel
    b.putpixel(image_pos, blue_channel_pixel)

'''
encoder

opens image and converts to 4 x 8bit RGBA

reads input data, gets length of input data and serializes the int value this length

the data to be encoded in now the length value joined to the input data, as a bitarray

uses generator function, supplied with the seed, to generate x, y pairs
The last call of this function opens the pygame window that displays the pattern visually

for each x,y pair 2 bits will be encoded via encode_bits and saved into the g, b lists

the 4 channels are merged into a new image object and saved to the filesystem

'''

def encoder(input_image, output_image, input_data_file, seed):

    img = Image.open(input_image) # open source image as PIL/Pillow object
    hdatareader = open(input_data_file, 'rb') # open input data file to be read as a bytearray
    input_data = hdatareader.read()

    r, g, b, a = img.convert('RGBA').split() # split the color/alpha channels into individual lists


    input_data_len = len(input_data) * 4 # get length of input data
    
    print("original size of input data (in pixels used): ", input_data_len)
    
    input_data_iter = 0
    input_data_bit_iter = 0

    data_len_serialized = fixedint.UInt32(input_data_len).to_bytes() # turn the length of the input data into a bytearray to it can be prepended to the input data during encoding
    input_data = data_len_serialized + input_data # prepend the length to the input data

    input_data_len = len(input_data) * 4 # update value to include total length of data that will be encoded

    print("image mode before conversion: ", img.mode)
    if input_data_len > img.width * img.height: # check if everything fits
        print("input data too large")
        return
    print("input data will affect ", input_data_len, " of ", img.width * img.height, "pixels in the image")

    for x, y in generate_pattern(seed, img.width, img.height, input_data_len): # generate image x,y coordinates where bits encoded in the green and blue pixel data
        encode_bits(g, b, (x, y), input_data, input_data_iter, input_data_bit_iter) # pass g and b color channel list, pixel coordinates, and the indexes of the byte and bits to encode
        input_data_bit_iter += 2
        if input_data_bit_iter > 6: # move forward to the next byte
            #print(input_data[input_data_iter], end=' ')
            input_data_iter += 1
            input_data_bit_iter = 0
 
    newimage = Image.merge('RGBA', (r, g, b, a)) # make new image to export by combining the channels
    newimage.save(output_image, 'PNG')

    img.close()
    newimage.close()
    hdatareader.close()

'''
main

gets arguments using getopt

'''

def main(argv):

    input_image = ''
    input_data_file = ''
    output_image = ''
    seed = 0

    try:
        opts, args = getopt.getopt(argv,"hd:i:o:s:",["hdata=", "ifile=","ofile=", "seed="])
    except getopt.GetoptError:
        print('encode.py -d <data to encode> -i <input image file> -o <output image file> -s <seed(integer)>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('encode.py -d <data to encode> -i <input image file> -o <output image file> -s <seed(integer)>')
            sys.exit()
        elif opt in ("-d", "--hdata"):
            input_data_file = arg
        elif opt in ("-i", "--ifile"):
            input_image = arg
        elif opt in ("-o", "--ofile"):
            output_image = arg
        elif opt in ("-s", "--seed"):
            seed = int(arg)

    if input_image == '' or output_image == '' or input_data_file == '' or seed <= 0:
        print('encode.py -d <data to encode> -i <input image file> -o <output image file> -s <seed(integer)>')
        sys.exit(2)
    
    print ('Seed is - ', seed)
    print ('File with data to encode is - ', input_data_file)
    print ('Input image file is - ', input_image)
    print ('Output image file is - ', output_image)
    encoder(input_image, output_image, input_data_file, seed)

if __name__ == "__main__":
   main(sys.argv[1:])
