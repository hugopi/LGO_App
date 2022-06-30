from dataset_utils import *

outputDirectory = "E:/LGO/ressource/output"
shapeFileDirectory = "E:/LGO/ressource/shapeFile"
shapeFile = "GDM1"
date = "date1"
csvPath = "E:/LGO/ressource/sortie_bateau.csv"

dictionary = imageDictionary(outputDirectory, shapeFileDirectory)

source = outputDirectory + "/" + date + "/" + shapeFile + "/" + dictionary[date][shapeFile][0]

data = samples(csvPath, source)

#row,col = findValidIndex(source,data)

with rasterio.open(source) as src:
    img = src.read(1)
    shape = img.shape
    boundingBox = src.bounds

    stop = False
    for i in data['Nord']:
        if stop == True:
            break
        for j in data['Est']:
            if boundingBox[0] < i < boundingBox[1] and boundingBox[2] < j < boundingBox[3]:
                valid = data[data['Nord'] == i]
                stop = True
                break
            else:
                continue
    x = valid['Nord']
    y = valid['Est']
    row,col = src.index(x,y)