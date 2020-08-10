from PIL import Image
import sys, getopt

def decode_hdata(g, b, pos, hdata, hdatapos, hdatabitpos):
    gpix = g.getpixel(pos)
    bpix = b.getpixel(pos)

    hdatabyte = ord(hdata[hdatapos])

    hdatabyte |= (gpix & 0x1) << hdatabitpos
    hdatabyte |= (bpix & 0x1) << (hdatabitpos + 1)

    hdata[hdatapos] = str(chr(hdatabyte))

'''
encoder

opens image and converts to 4 x 8bit RGBA
loops through image's 2D matrix and applies a function to the image

for now the function applied just sets pixels to black. the next step will be encoding a hidden message
'''

def decoder(inputfile, outputfile):

    img = Image.open(inputfile)
    hdata = []

    print(hdata)
    print(img.mode)
    r, g, b, a = img.convert('RGBA').split()

    hdatapos = 0
    hdatabitpos = 0

    for y in range(img.height):
        for x in range(img.width):

            if hdatabitpos == 0:
                hdata.append('\0')
            decode_hdata(g, b, (x, y), hdata, hdatapos, hdatabitpos)

            hdatabitpos += 2
            if hdatabitpos > 6:
                #print(hdata[hdatapos])
                hdatapos += 1
                hdatabitpos = 0

    hdatalen = hdatapos

    print("".join(hdata))

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

    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('encoder.py -i <inputfile> -o <outputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print ('encoder.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    if inputfile == '' or outputfile == '':
        print('encoder.py -i <inputfile> -o <outputfile>')
        sys.exit(2)

    print ('Input file is "', inputfile)
    print ('Output file is "', outputfile)
    decoder(inputfile, outputfile)

if __name__ == "__main__":
   main(sys.argv[1:])
