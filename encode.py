import sys, getopt

from PIL import Image
from pathlib import Path

from generatepattern import generate_pattern

'''
encode_bits

encodes two bits from the source text into the LSBs of the source image's green and blue channels

'''

def encode_bits(g, b, image_pos, input_data, input_data_iter, input_data_bit_iter):

    green_channel_pixel = g.getpixel(image_pos)
    blue_channel_pixel = b.getpixel(image_pos)

    hdatabyte = ord(input_data[input_data_iter])
    
    green_pixel_bitmask = (hdatabyte & (0x1 << input_data_bit_iter)) >> input_data_bit_iter
    blue_pixel_bitmask = (hdatabyte & (0x1 << (input_data_bit_iter + 1))) >> (input_data_bit_iter + 1)

    if green_channel_pixel & 0x1 and green_pixel_bitmask == 0:
        green_channel_pixel -= 1
    else:
        green_channel_pixel |= green_pixel_bitmask

    if blue_channel_pixel & 0x1 and blue_pixel_bitmask == 0:
        blue_channel_pixel -= 1
    else:
        blue_channel_pixel |= blue_pixel_bitmask

    g.putpixel(image_pos, green_channel_pixel)
    b.putpixel(image_pos, blue_channel_pixel)

'''
encoder

opens image and converts to 4 x 8bit RGBA

uses generator function, supplied with the seed, to generate x, y pairs
The last call of this function opens the pygame window that displays the pattern visually

for each x,y pair 2 bits will be encoded via encode_bits and saved into the g, b lists

the 4 channels are merged into a new image object and saved to the filesystem

'''

def encoder(inputfile, outputfile, hiddendatafile, seed):

    img = Image.open(inputfile)
    hdatareader = open(hiddendatafile)
    input_data = hdatareader.read()
    input_data += "\00"

    r, g, b, a = img.convert('RGBA').split()

    input_data_len = len(input_data) * 4
    input_data_iter = 0
    input_data_bit_iter = 0

    print("image mode before conversion: ", img.mode)
    if input_data_len > img.width * img.height:
        print("input data too large")
        return
    print("input data will affect ", input_data_len, " of ", img.width * img.height, "pixels in the image")

    for x, y in generate_pattern(seed, img.width, img.height, input_data_len):
        encode_bits(g, b, (x, y), input_data, input_data_iter, input_data_bit_iter)
        input_data_bit_iter += 2
        if input_data_bit_iter > 6:
            input_data_iter += 1
            input_data_bit_iter = 0

    #print (hdata)
 
    newimage = Image.merge('RGBA', (r, g, b, a))
    newimage.save(outputfile, 'PNG')

    img.close()
    newimage.close()
    hdatareader.close()

'''
main

gets arguments using getopt,
checks for errors using getopts format checking and the getopterror exception,
then calls the 'encoder' function
'''

def main(argv):

    inputfile = ''
    outputfile = ''
    hiddendatafile = ''
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
            hiddendatafile = arg
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-s", "--seed"):
            seed = int(arg)

    if inputfile == '' or outputfile == '' or hiddendatafile == '' or seed <= 0:
        print('encode.py -d <data to encode> -i <input image file> -o <output image file> -s <seed(integer)>')
        sys.exit(2)
    
    print ('Seed is - ', seed)
    print ('Input image file is - ', inputfile)
    print ('Output image file is - ', outputfile)
    print ('File with data to encode is - ', hiddendatafile)
    encoder(inputfile, outputfile, hiddendatafile, seed)

if __name__ == "__main__":
   main(sys.argv[1:])
