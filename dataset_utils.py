import rasterio
import numpy as np
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
from fileManagment_utils import *


def initDataset(shapeFile, date, dictionary, outputDirectory):
    listOfImage = dictionary[date][shapeFile]

    template = outputDirectory + "/" + date + "/" + shapeFile + "/" + listOfImage[0]

    columns = len(listOfImage)
    with rasterio.open(template) as src:
        img_template = src.read(1)
        shape_template = img_template.shape
        dataset = np.zeros((shape_template[0] * shape_template[1], columns))

    return dataset


def resolutionResample(template, source):
    # description : feed with your template image and an image, you will get your image resample
    # open and read the shape of the template image here its resolution 10*10
    with rasterio.open(template) as src:
        img_template = src.read(1)
        shape_template = img_template.shape
    # open the image you want to resample
    with rasterio.open(source) as src:
        img = src.read(1)

        # Resample depending on the resolution
        if ("B05" in source) or ("B06" in source) or ("B07" in source) or ("B8A" in source) or ("B11" in source) or (
                "B12" in source):
            img = np.kron(img, np.ones((2, 2)))
            rowGap = img.shape[0] - shape_template[0]
            columnGap = img.shape[1] - shape_template[1]

            if rowGap == 0 and columnGap == 0:
                img = img
            if rowGap != 0 and columnGap == 0:
                img = img[:-rowGap, :]
            if rowGap == 0 and columnGap != 0:
                img = img[:, :-columnGap]
            if rowGap != 0 and columnGap != 0:
                img = img[:-rowGap, :-columnGap]

    return img


def fillDataset(shapeFile, date, dictionary, outputDirectory):
    dataset = initDataset(shapeFile, date, dictionary, outputDirectory)

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
        datasetIndex += 1

    return dataset


def samples(csvPath, source):
    data = pd.read_csv(csvPath, sep=';')

    sampleDictionary = {'id': [], 'geometry': []}

    for i in data.index:
        x = data['Est'][i]
        y = data['Nord'][i]
        id = data['id'][i]

        sampleDictionary['geometry'].append(Point(x, y))
        sampleDictionary['id'].append(id)

    with rasterio.open(source) as src:
        profile_src = src.profile
        sampleGeoData = gpd.GeoDataFrame(sampleDictionary, crs=4326)
        sampleGeoData = sampleGeoData.to_crs(profile_src['crs'])

    for i in range(len(sampleGeoData['geometry'])):
        data['Nord'][i] = sampleGeoData['geometry'][i].x
        data['Est'][i] = sampleGeoData['geometry'][i].y

    return data


def findValidIndex(source,data):

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
        row, col = src.index(x, y)

    return row,col