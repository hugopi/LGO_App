import os
from pathlib import Path

import fiona
import rasterio


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


def saveShape(savingShapeDirectory, img_herbier, wantedClass, source):
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
        'geometry': 'Polygon',
        'properties': [('Name', 'str')]
    }

    # create a destinationFile name
    split = source.split('/')
    destinationFile = split[-3] + '_' + split[-2] + '_' + 'class' + '_' + str(wantedClass) + '.shp'
    destination = savingShapeDirectory + '/' + split[-3] + '/' + split[-2] + '/' + 'class' + '_' + str(wantedClass)

    # if destination directory not exist create it, else overwrite
    path = Path(destination)
    path.mkdir(parents=True, exist_ok=True)

    destination = destination + '/' + destinationFile

    # open a fiona object
    polyShp = fiona.open(destination, mode='w', driver='ESRI Shapefile',
                         schema=schema, crs=crs_source)

    # save record and close shapefile
    rowDict = {
        'geometry': {'type': 'Polygon', 'coordinates': [xyList]},
        'properties': {'Name': split[-2]},
    }

    polyShp.write(rowDict)

    # close fiona object
    polyShp.close()
