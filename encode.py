from PIL import Image
from pathlib import Path
import sys, getopt

from imageviewer import view_image_object

'''
encode_hdata

encodes two bits from the source text into the LSBs of the source image's green and blue channels

'''

def encode_hdata(g, b, pos, hdata, hdatapos, hdatabitpos):

    gpix = g.getpixel(pos)
    bpix = b.getpixel(pos)

    hdatabyte = ord(hdata[hdatapos])
    gmask = (hdatabyte & (0x1 << hdatabitpos)) >> hdatabitpos
    bmask = (hdatabyte & (0x1 << (hdatabitpos + 1))) >> (hdatabitpos + 1)

    if gpix & 0x1 and gmask == 0:
        gpix -= 1
    else:
        gpix |= gmask
    if bpix & 0x1 and bmask == 0:
        bpix -= 1
    else:
        bpix |= bmask

    g.putpixel(pos, gpix)
    b.putpixel(pos, bpix)

'''
encoder

opens image and converts to 4 x 8bit RGBA
loops through image's 2D matrix and encodes the source text into the image at 2 bits per pixel

'''

def encoder(inputfile, outputfile, hiddendatafile):

    img = Image.open(inputfile)
    hdatareader = open(hiddendatafile)
    hdata = hdatareader.read()

    print(img.mode)
    print("input data will use ", Path(hiddendatafile).stat().st_size * 4, "of ", img.width * img.height, "pixels in the provided image")

    r, g, b, a = img.convert('RGBA').split()

    hdatalen = len(hdata)
    hdatapos = 0
    hdatabitpos = 0

    for y in range(img.height):
        for x in range(img.width):

            if hdatapos < hdatalen:
                encode_hdata(g, b, (x, y), hdata, hdatapos, hdatabitpos)

            hdatabitpos += 2
            if hdatabitpos > 6:
                hdatapos += 1
                hdatabitpos = 0



    newimage = Image.merge('RGBA', (r, g, b, a))
    newimage.save(outputfile, 'PNG')

    mode = newimage.mode
    size = newimage.size
    data = newimage.tobytes()

    view_image_object(data, size, mode)

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

    try:
        opts, args = getopt.getopt(argv,"hd:i:o:",["hdata=", "ifile=","ofile="])
    except getopt.GetoptError:
        print('encoder.py -d <hiddendata> -i <inputfile> -o <outputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print ('encoder.py -d <hiddendata> -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-d", "--hdata"):
            hiddendatafile = arg
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    if inputfile == '' or outputfile == '' or hiddendatafile == '':
        print('encoder.py -d <hiddendata> -i <inputfile> -o <outputfile>')
        sys.exit(2)

    print ('Input file is "', inputfile)
    print ('Output file is "', outputfile)
    print ('Hidden data file is "', hiddendatafile)
    encoder(inputfile, outputfile, hiddendatafile)

if __name__ == "__main__":
   main(sys.argv[1:])
