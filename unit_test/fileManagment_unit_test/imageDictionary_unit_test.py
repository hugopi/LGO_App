from fileManagment_utils import *

outputDirectory = "/Users/pires/PycharmProjects/LGO/application/unit_test/ressource/output"
shapeFileDirectory = "/Users/pires/PycharmProjects/LGO/application/shapeFile"

#dictionary = imageDictionary(outputDirectory,shapeFileDirectory)

listOfDirectories = fileList(outputDirectory)
listOfShapeFiles = fileList(shapeFileDirectory)

dictionary = {}
for i in listOfDirectories:
    shapes = {}
    for j in range(len(listOfShapeFiles)):
        images = {listOfShapeFiles[j]: fileList(outputDirectory + "/" + i + "/" + listOfShapeFiles[j])}
        shapes.update(images)
    date = {i: shapes}
    dictionary.update(date)