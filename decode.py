import sys, getopt
from PIL import Image

from generatepattern import generate_pattern

'''
extract_bits

retrieves the data stored the the green and blue channel's LSBs and appends it to a list

'''

def extract_bits(g, b, image_pos, extracted_data, extracted_data_iter, extracted_data_bit_iter):
    green_channel_pixel = g.getpixel(image_pos)
    blue_channel_pixel = b.getpixel(image_pos)

    selected_byte = ord(extracted_data[extracted_data_iter])

    selected_byte |= (green_channel_pixel & 0x1) << extracted_data_bit_iter
    selected_byte |= (blue_channel_pixel & 0x1) << (extracted_data_bit_iter + 1)

    extracted_data[extracted_data_iter] = str(chr(selected_byte))


'''
retrieve_hidden_data_loop

splits image into individual lists of bytes, one for each of the 4 channels in the image (red, green, blue, alpha)

uses generator function, supplied with the seed, to generate x, y pairs
The last call of this function opens the pygame window that displays the pattern visually

for each x,y pair 2 bits will be extracted via extract_bits and saved into the extracted_data list

'''

def retrieve_hidden_data_loop(img, extracted_data, seed):
    r, g, b, a = img.convert('RGBA').split()

    extracted_data_iter = 0
    extracted_data_bit_iter = 0

    for x, y in generate_pattern(seed, img.width, img.height, img.width * img.height):
        if extracted_data_bit_iter == 0:
            extracted_data.append('\0')
        extract_bits(g, b, (x, y), extracted_data, extracted_data_iter, extracted_data_bit_iter)
        extracted_data_bit_iter += 2
        if extracted_data_bit_iter > 6:
            if ord(extracted_data[extracted_data_iter]) == 0:
                return
            extracted_data_iter += 1
            extracted_data_bit_iter = 0

'''
decoder_wrapper

opens input_image and converts to 4 x 8bit RGBA

calls retrieve_hidden_data_loop

writed decoded data to output_image and STDOUT
'''

def decoder_wrapper(input_image, output_image, seed):

    img = Image.open(input_image)
    extracted_data = []

    retrieve_hidden_data_loop(img, extracted_data, seed)
    data_as_string = "".join(extracted_data)[:-1]

    f = open(output_image, "w", encoding="utf-8")
    f.write(data_as_string)
    img.close()
    f.close()
    print(data_as_string)


'''
main

gets arguments using getopt

'''

def main(argv):

    input_image = ''
    output_image = ''
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
            output_image = arg
        elif opt in ("-s", "--seed"):
            seed = int(arg)
    if input_image == '' or output_image == '' or seed <= 0:
        print('decode.py -i <inputfile> -o <outputfile> -s <seed(integer)>')
        sys.exit(2)

    decoder_wrapper(input_image, output_image, seed)

if __name__ == "__main__":
   main(sys.argv[1:])
