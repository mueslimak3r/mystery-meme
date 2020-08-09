import png
import numpy
from PIL import Image, ImageDraw
import sys, getopt

'''
setblack


debug function that sets pixels on rgb channels to black and makes them opaque
'''

def setblack (r, g, b, a, pos):
    r.putpixel(pos, 0)
    g.putpixel(pos, 0)
    b.putpixel(pos, 0)
    a.putpixel(pos, 255)

'''
encoder

opens image and converts to 4 x 8bit RGBA
loops through image's 2D matrix and applies a function to the image

for now the function applied just sets pixels to black. the next step will be encoding a hidden message
'''

def encoder(inputfile, outputfile):

    img = Image.open(inputfile)

    print(img.mode)
    r, g, b, a = img.convert('RGBA').split()
    for y in range(img.height):
        for x in range(img.width):
            # just sets pixel with full transparency to solid black for debugging. This is where the hidden message will be encoded
            if a.getpixel((x, y)) == 0:
                setblack(r, g, b, a, (x, y))
    newimage = Image.merge('RGBA', (r, g, b, a))
    newimage.save(outputfile, 'PNG')
    img.close()
    newimage.close()

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
    encoder(inputfile, outputfile)

if __name__ == "__main__":
   main(sys.argv[1:])
