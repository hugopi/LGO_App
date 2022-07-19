from bathymetry_utils import *
from unsupervised_classification_utils import *

outputBathymetryDirectory = "E:/LGO/ressource/output_bathymetry"
outputDirectory = "E:/LGO/ressource/output"
shapeFileDirectory = "E:/LGO/ressource/shapeFile"

dictionary = imageDictionary(outputDirectory, shapeFileDirectory)

date, shapeFile = selectParameters(dictionary)

bathymetryFile = outputBathymetryDirectory + '/' + shapeFile + '/' + "MNT_COTIER_MORBIHAN_TANDEM_20m_WGS84_PBMA_ZNEG.bag"

### complete with zero if its required

with rasterio.open(bathymetryFile) as src:
    bathymetry = src.read(1)
    shape = bathymetry.shape

    source = outputDirectory + '/' + date + '/' + shapeFile + '/' + dictionary[date][shapeFile][0]

    with rasterio.open(source) as src:
        img = src.read(1)

    if bathymetry.shape[0] != img.shape[0]:
        gap = img.shape[0] - bathymetry.shape[0]
        zero = np.zeros((gap, img.shape[1]))
        bathymetry = np.concatenate((bathymetry, zero), axis=0)

    if bathymetry.shape[1] != img.shape[1]:
        gap = img.shape[1] - bathymetry.shape[1]
        zero = np.zeros((img.shape[0], gap))
        bathymetry = np.concatenate((bathymetry, zero), axis=1)

bathymetryVect = bathymetry.reshape((img.shape[0] * img.shape[1], 1))

### choose value
top = -0.5
bottom = -1.2

bathymetryVect[bathymetryVect<=bottom] = 0
bathymetryVect[bathymetryVect>=top] = 0
bathymetryVect[bathymetryVect!=0] = 1

###
dataset = fillDataset(shapeFile, date, dictionary, outputDirectory)
dataset2 = np.concatenate((dataset, bathymetryVect), axis=1)

# classify the pixels of the dataset between earth and sea
separation = earthAndSea(dataset2)

# create a dataset only with sea pixels
sea = seaDataset(dataset2, separation, invert=True)