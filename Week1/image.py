from PIL import Image
import numpy

ROWS = 28 #Height of image
COLS = 28 #width of image

'''
 Transforms the image in filename to a list of data
 compatible with MINST training dataset.
 The image is resized and converted to grayscale.
'''
def img2data(filename):
    im = Image.open( filename ) #reads the image
    im = im.convert("L")        #converts to grayscale
    im = im.resize([COLS, ROWS])#resizes th image
    a = list(im.getdata())      #converts to a list of ints 0-255
    return a

'''
 Transforms a list of data
 (compatible with MINST training dataset)
 to a grayscale COLSXROWS image.
'''
def data2img(lst):
    lst2d = [] #Transforms the list to a 2D list
    for i in range(ROWS):
        lst2d += [lst[COLS*i : COLS*(i+1)]]
    #Image.fromarray converts a numpy 2D array to an image
    return Image.fromarray(numpy.uint8(numpy.array(lst2d)))





