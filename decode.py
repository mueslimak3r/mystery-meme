import sys, getopt
from PIL import Image

from generatepattern import generate_pattern

'''
decode_hdata

retrieves the data stored the the green and blue channel's LSBs and appends it to a list

'''

def decode_hdata(g, b, pos, hdata, hdatapos, hdatabitpos):
    gpix = g.getpixel(pos)
    bpix = b.getpixel(pos)

    hdatabyte = ord(hdata[hdatapos])

    hdatabyte |= (gpix & 0x1) << hdatabitpos
    hdatabyte |= (bpix & 0x1) << (hdatabitpos + 1)

    hdata[hdatapos] = str(chr(hdatabyte))


'''
decoder loop



'''
def decoder_loop(img, hdata, seed):
    r, g, b, a = img.convert('RGBA').split()

    encode_mask = generate_pattern(seed, img.width, img.height, int((img.width * img.height) / 4))
    hdatapos = 0
    hdatabitpos = 0

    for y in range(img.height):
        for x in range(img.width):
            if encode_mask[(y * img.width) + x] == 1:
                if hdatabitpos == 0:
                    hdata.append('\0')
                decode_hdata(g, b, (x, y), hdata, hdatapos, hdatabitpos)

                hdatabitpos += 2
                if hdatabitpos > 6:
                    if ord(hdata[hdatapos]) == 0:
                        return
                    hdatapos += 1
                    hdatabitpos = 0

'''
decoder

opens image and converts to 4 x 8bit RGBA
loops through image's 2D matrix and decodes the hidden data at 2 bits per pixel

'''

def decoder(inputfile, outputfile, seed):

    img = Image.open(inputfile)
    hdata = []

    print(hdata)
    print(img.mode)

    decoder_loop(img, hdata, seed)
    data = "".join(hdata)
    print(data)
    f = open(outputfile, "w")
    f.write(data)

    img.close()

'''
main

gets arguments using getopt,
checks for errors using getopts format checking and the getopterror exception,
then calls the 'encoder' function
'''

def main(argv):

    inputfile = ''
    outputfile = ''
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
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-s", "--seed"):
            seed = int(arg)
    if inputfile == '' or outputfile == '' or seed <= 0:
        print('decode.py -i <inputfile> -o <outputfile> -s <seed(integer)>')
        sys.exit(2)

    print ('Seed is -', seed)
    print ('Input file is -', inputfile)
    print ('Output file is -', outputfile)
    
    decoder(inputfile, outputfile, seed)

if __name__ == "__main__":
   main(sys.argv[1:])
