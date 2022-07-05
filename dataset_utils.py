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

    datasetIndex = 0
    for i in listOfImage:
        source = outputDirectory + "/" + date + "/" + shapeFile + "/" + i

        with rasterio.open(source) as src:
            img = src.read(1)
            shape = img.shape
        # normalize for easy computation
        img = img / 65535
        # Reshape the matrix in order to implement it in dataset
        img = img.reshape(shape[0] * shape[1])
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
        data['Nord'][i] = sampleGeoData['geometry'][i].y
        data['Est'][i] = sampleGeoData['geometry'][i].x

    return data


def findValidIndex(source, data):
    with rasterio.open(source) as src:
        img = src.read(1)
        shape = img.shape
        boundingBox = src.bounds
        dataMaskNord = data[data['Nord'] <= boundingBox[3]]
        dataMaskNord = dataMaskNord[dataMaskNord['Nord'] >= boundingBox[1]]
        dataMaskEst = dataMaskNord[dataMaskNord['Est'] <= boundingBox[2]]
        dataMaskEst = dataMaskEst[dataMaskEst['Est'] >= boundingBox[0]]
        dataMaskHerbier = dataMaskEst[dataMaskEst['herbier'] == 1]

        validIndex = []
        for i in dataMaskHerbier.index:
            x = dataMaskHerbier['Nord'][i]
            y = dataMaskHerbier['Est'][i]
            row, col = src.index(y, x)
            validIndex.append((row, col))

    return validIndex


def pixelRecover(data, outputDirectory, dictionary):
    data.insert(loc=5, column='pixel', value=['nan'] * len(data))

    for i in data.index:
        y = data['Est'][i]
        x = data['Nord'][i]
        for j in dictionary:
            for k in dictionary[j]:
                pixel = []
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
    return data
