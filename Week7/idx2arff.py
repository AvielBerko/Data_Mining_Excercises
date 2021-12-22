from PIL import Image
import numpy

ROWS = 28 #Height of image
COLS = 28 #width of image

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
    n = numpy.array(lst2d)
    n2 = numpy.uint8(n)
    return Image.fromarray(n2)


def idx2pngs(images,labels,path):
    fimages = open(images,"rb")
    flabels = open(labels,"rb")
    flabels.seek(8)
    fimages.seek(16)
    x=fimages.read(1)
    index = 1
    while x!=b"":
        img = []
        img.append(ord(x))
        for i in range(783):
            img.append(ord(fimages.read(1)))
        png = data2img(img)
        png.save(path + str(index) + "_" + str(ord(flabels.read(1))) + ".png", format="png")
        index += 1
        x = fimages.read(1)
    fimages.close()
    flabels.close()

def idx2txt(images,labels):
    fout = open("data.txt", "w")
    fimages = open(images,"rb")
    flabels = open(labels,"rb")
    flabels.seek(8)
    fimages.seek(16)
    x=fimages.read(1)
    index = 1
    while x!=b"":
        fout.write('0 ' if ord(x) < 130 else '1 ')
        for i in range(783):
            fout.write('0 ' if ord(fimages.read(1)) < 130 else '1 ')
        fout.write(str(ord(flabels.read(1))) + '\n')
        x = fimages.read(1)
    fout.close()
    fimages.close()
    flabels.close()

#idx2arff("t10k-images.idx3-ubyte", "t10k-labels.idx1-ubyte", "images\\")
#idx2arff("train-images.idx3-ubyte", "train-labels.idx1-ubyte", "images\\")
idx2txt("train-images.idx3-ubyte", "train-labels.idx1-ubyte")



        
