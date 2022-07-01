from dataset_utils import *

outputDirectory = "E:/LGO/ressource/output"
shapeFileDirectory = "E:/LGO/ressource/shapeFile"
shapeFile = "GDM1"
date = "date1"
csvPath = "E:/LGO/ressource/sortie_bateau.csv"

dictionary = imageDictionary(outputDirectory, shapeFileDirectory)

source = outputDirectory + "/" + date + "/" + shapeFile + "/" + dictionary[date][shapeFile][0]

data = samples(csvPath, source)

# row,col = findValidIndex(source,data)

with rasterio.open(source) as src:
    img = src.read(1)
    shape = img.shape
    boundingBox = src.bounds
    dataMaskNord = data[data['Nord']<=boundingBox[1]]
    dataMaskNord = dataMaskNord[dataMaskNord['Nord'] >= boundingBox[0]]
    dataMaskEst = dataMaskNord[dataMaskNord['Est']<=boundingBox[3]]
    dataMaskEst = dataMaskEst[dataMaskEst['Est'] >= boundingBox[2]]
    dataMaskHerbier = dataMaskEst[dataMaskEst['herbier'] == 1]
    valid = dataMaskHerbier.sample()
    x = valid['Nord']
    y = valid['Est']
    row, col = src.index(x, y)
