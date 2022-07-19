import numpy as np

from imagePreparation_utils import *
import rasterio


def prepareBathymetry(bathymetryfilePath, outputBathymetrytDirectory, shapeFileDirectory, source, shapeFile):
    # open an output image in order to get crs
    with rasterio.open(source) as src:
        crs_img = src.crs

    print('Bathymetric data in preparation')

    # create a destination file which will be overwritten
    destination = outputBathymetrytDirectory + "/" + shapeFile
    destinationFile = destination + '/' + 'MNT_COTIER_MORBIHAN_TANDEM_20m_WGS84_PBMA_ZNEG.bag'

    # if destination directory not exist create it, else overwrite
    path = Path(destination)
    path.mkdir(parents=True, exist_ok=True)

    # copy the source file in the destination directory
    shutil.copy2(bathymetryfilePath, destinationFile)

    # open bathymetric data with gdal
    input_raster = gdal.Open(bathymetryfilePath)

    # reproject and update the resolution
    gdal.Warp(destinationFile, input_raster, dstSRS=crs_img, xRes=10, yRes=10)

    # crop
    shapeFilePath = shapeFileDirectory + '/' + shapeFile + '/' + shapeFile + '.shp'
    bathymetry_crop, meta = prepareImageGPD(shapeFilePath, destinationFile)

    # Overwrite the destination file created before with the cropped image
    with rasterio.open(destinationFile, "w", **meta) as dst:
        dst.write(bathymetry_crop)


def bathymetricData(bathymetryFile, source):
    ### complete with zero if its required

    with rasterio.open(bathymetryFile) as src:
        bathymetry = src.read(1)

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
    top = 0.5
    bottom = -4

    bathymetryVect[bathymetryVect <= bottom] = 0
    bathymetryVect[bathymetryVect >= top] = 0
    bathymetryVect[bathymetryVect != 0] = 1

    return bathymetryVect
