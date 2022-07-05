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


for i in data.index:
    y = data['Est'][i]
    x = data['Nord'][i]
    for j in dictionary:
        for k in dictionary[j]:
            pixel = []
            for l in dictionary[j][k]:
                source = outputDirectory + "/" + j + "/" + k + "/" + l
                template = outputDirectory + "/" + j + "/" + k + "/" + dictionary[j][k][0]
                img = resolutionResample(template, source)

                with rasterio.open(source) as src:
                    row, col = src.index(y, x)
                    pixel.append((row,col))

# dataset = fillDataset(shapeFile, date, dictionary, outputDirectory)
