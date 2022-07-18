import os
from pathlib import Path

import fiona
import rasterio
from matplotlib import pyplot as plt


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

    return date, shape


def generateShape(destination, source, img_herbier):
    # find the coordinates of herbier pixels
    xyList = []

    with rasterio.open(source) as src:
        crs_source = src.crs

        for i in range(img_herbier.shape[0]):
            for j in range(img_herbier.shape[1]):
                if img_herbier[i, j] != 0:
                    xyList.append(src.xy(i, j))

    # define schema
    schema = {
        'geometry': 'Point',
        'properties': [('Name', 'str')]
    }

    # open a fiona object
    pointShp = fiona.open(destination, mode='w', driver='ESRI Shapefile',
                          schema=schema, crs=crs_source)

    for i in xyList:
        rowDict = {
            'geometry': {'type': 'Point',
                         'coordinates': (i[0], i[1])},
            'properties': {'Name': 'point'},
        }
        pointShp.write(rowDict)
    # close fiona object
    pointShp.close()


def saveShape(savingShapeDirectory, img_classified, img_herbier, wantedClass, source):
    # names
    split = source.split('/')
    image = split[-3]
    shape = split[-2]
    destinationDirectory = savingShapeDirectory + '/' + image + '_' + shape + '_' + 'class' + '_' + str(wantedClass)

    # if destination directory not exist create it, else overwrite
    path = Path(destinationDirectory)
    path.mkdir(parents=True, exist_ok=True)

    # File names
    overviewFullFile = 'overview_full.jpeg'
    overviewClassFile = 'overview_class.jpeg'

    # save
    plt.imsave(destinationDirectory + "/" + overviewFullFile, img_classified)
    plt.imsave(destinationDirectory + "/" + overviewClassFile, img_herbier)
    generateShape(destinationDirectory + "/" + 'shapefile', source, img_herbier)
