import fixedint
import sys, getopt
from PIL import Image

from generatepattern import generate_pattern

'''
extract_bits

retrieves the data stored the the green and blue channel's LSBs and appends it to a list

'''

def extract_bits(g, b, image_pos, extracted_data, extracted_data_iter, extracted_data_bit_iter):
    green_channel_pixel = g.getpixel(image_pos) #
    blue_channel_pixel = b.getpixel(image_pos)  # get the g and b pixel bytes

    selected_byte = extracted_data[extracted_data_iter] # get the destination byte

    selected_byte |= (green_channel_pixel & 0x1) << extracted_data_bit_iter      # add the new bits to the destination byte
    selected_byte |= (blue_channel_pixel & 0x1) << (extracted_data_bit_iter + 1) #

    extracted_data[extracted_data_iter] = int(selected_byte) # save the alteration


'''
retrieve_hidden_data_loop

splits image into individual lists of bytes, one for each of the 4 channels in the image (red, green, blue, alpha)

uses generator function, supplied with the seed, to generate x, y pairs
The last call of this function opens the pygame window that displays the pattern visually

for each x,y pair 2 bits will be extracted via extract_bits and saved into the extracted_data list
the first 24 bytes extracted is number of pixels left to extract data from

'''

def retrieve_hidden_data_loop(img, extracted_data, seed):
    r, g, b, a = img.convert('RGBA').split() # split the color/alpha channels into individual lists

    extracted_data_iter = 0
    extracted_data_bit_iter = 0

    size = 0
    countdown = -1 # counter isn't used until the data size is decoded from the first 4 bytes

    for x, y in generate_pattern(seed, img.width, img.height, img.width * img.height): # generate image x,y coordinates where bits are encoded in the green and blue pixel data
        if countdown == 0:
            return
        countdown -= 1
        if extracted_data_bit_iter == 0: # for each new byte of decoded data append a byte with value 0 to list
            extracted_data.append(0)
        extract_bits(g, b, (x, y), extracted_data, extracted_data_iter, extracted_data_bit_iter) # data is encoded in green and blue color channels. extract bits at the generated x,y pixel
        extracted_data_bit_iter += 2
        if extracted_data_bit_iter > 6: # move forward to the next byte
            if extracted_data_iter == 3: # magic number for the 4 bytes of memory where the data size is stored
                size = fixedint.UInt32.from_bytes(bytearray(extracted_data[:-(len(extracted_data) - extracted_data_iter)]), byteorder='little') # convert data size from bytes to int
                print("size of encoded data: ", size)
                countdown = size # this size becomes a counter for how many bytes are left to decode
            extracted_data_iter += 1
            extracted_data_bit_iter = 0

'''
decoder_wrapper

opens input_image and converts to 4 x 8bit RGBA

calls retrieve_hidden_data_loop

writed decoded data to output_file and STDOUT
'''

def decoder_wrapper(input_image, output_file, seed):

    img = Image.open(input_image) # open source image as PIL/Pillow object
    extracted_data = []

    retrieve_hidden_data_loop(img, extracted_data, seed)
    #data_as_string = extracted_data

    f = open(output_file, 'wb')
    f.write(bytearray(extracted_data[4:])) # needs to splice out leading bytes containing length
    img.close()
    f.close()
    #print(data_as_string)


'''
main

gets arguments using getopt

'''

def main(argv):

    input_image = ''
    output_file = ''
    seed = 0

    try:
        opts, args = getopt.getopt(argv,"hi:o:s:",["ifile=","ofile=", "seed="])
    except getopt.GetoptError:
        print('decode.py -i <inputfile> -o <outputfile> -s <seed(integer)>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('decode.py -i <inputfile> -o <outputfile> -s <seed(integer)>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_image = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg
        elif opt in ("-s", "--seed"):
            seed = int(arg)
    if input_image == '' or output_file == '' or seed <= 0:
        print('decode.py -i <inputfile> -o <outputfile> -s <seed(integer)>')
        sys.exit(2)

    decoder_wrapper(input_image, output_file, seed)

if __name__ == "__main__":
   main(sys.argv[1:])
