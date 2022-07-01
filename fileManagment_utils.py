import os


def fileList(directoryPath):
    # list the different files in the directory
    liste = os.listdir(directoryPath)
    return liste


def imageDictionary(outputDirectory, shapeFileDirectory):

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

    return dictionary

def selectParameters(dictionary):

    dateKey = dictionary.keys()

    for i in dateKey:
        print(i)

    date = input("choose your date : ")

    shapeKey = dictionary[date].keys()

    for i in shapeKey:
        print(i)

    shape = input("choose your shape : ")

    return date,shape
