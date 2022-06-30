from dataset_utils import *

outputDirectory = "E:/LGO/ressource/output"
shapeFileDirectory = "E:/LGO/ressource/shapeFile"
shapeFile = "GDM1"
date = "date1"

dictionary = imageDictionary(outputDirectory, shapeFileDirectory)
dataset = fillDataset(shapeFile,date,dictionary,outputDirectory)

'''dataset = initDataset(shapeFile, date, dictionary, outputDirectory)

listOfImage = dictionary[date][shapeFile]

template = outputDirectory + "/" + date + "/" + shapeFile + "/" + listOfImage[0]

with rasterio.open(template) as src:
    img_template = src.read(1)
    shape_template = img_template.shape

datasetIndex = 0
for i in listOfImage:
    source = outputDirectory + "/" + date + "/" + shapeFile + "/" + i
    # resample depending on the resolution
    img = resolutionResample(template, source)
    # normalize for easy computation
    img = img / 65535
    # Reshape the matrix in order to implement it in dataset
    img = img.reshape(shape_template[0] * shape_template[1])
    # overwrite initialized datasetComponent
    dataset[:, datasetIndex] = img
    datasetIndex += 1'''