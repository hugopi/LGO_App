from dataset_utils import *

outputDirectory = "E:/LGO/ressource/output"
shapeFileDirectory = "E:/LGO/ressource/shapeFile"
shapeFile = "GDM4"
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
    print(boundingBox)
    dataMaskNord = data[data['Nord']<=boundingBox[3]]
    dataMaskNord = dataMaskNord[dataMaskNord['Nord'] >= boundingBox[1]]
    dataMaskEst = dataMaskNord[dataMaskNord['Est']<=boundingBox[2]]
    dataMaskEst = dataMaskEst[dataMaskEst['Est'] >= boundingBox[0]]
    dataMaskHerbier = dataMaskEst[dataMaskEst['herbier'] == 1]

    validIndex = []
    for i in dataMaskHerbier.index:
        x = dataMaskHerbier['Nord'][i]
        y = dataMaskHerbier['Est'][i]
        row, col = src.index(y, x)
        validIndex.append((row,col))

