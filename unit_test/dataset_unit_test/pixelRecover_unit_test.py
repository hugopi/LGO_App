from unsupervised_classification_utils import *
from collections import Counter

csvPath = "E:/LGO/ressource/sortie_bateau.csv"
outputDirectory = "E:/LGO/ressource/output"
shapeFileDirectory = "E:/LGO/ressource/shapeFile"
k = 30

dictionary = imageDictionary(outputDirectory, shapeFileDirectory)

date, shapeFile = selectParameters(dictionary)

crs_template = outputDirectory + "/" + date + "/" + shapeFile + "/" + dictionary[date][shapeFile][0]
data = samples(csvPath, crs_template)

data.insert(loc=5,column='pixel',value=['nan']*len(data))

for i in data.index:
    y = data['Est'][i]
    x = data['Nord'][i]
    for j in dictionary:
        for k in dictionary[j]:
            pixel=[]
            for l in dictionary[j][k]:

                source = outputDirectory + "/" + j + "/" + k + "/" + l

                with rasterio.open(source) as src:
                    img = src.read(1)
                    boundingBox = src.bounds

                    if boundingBox[1] <= x <= boundingBox[3] and boundingBox[0] <= y <= boundingBox[2]:
                        row, col = src.index(y, x)
                        pixel.append(img[row, col])

            if len(pixel) != 0:
                data['pixel'][i] = pixel
                break

