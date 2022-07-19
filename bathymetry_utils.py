from imagePreparation_utils import *
import rasterio


def prepareBathymetry(bathymetryfilePath, outputBathymetrytDirectory, outputDirectory, shapeFileDirectory):

    dictionary = imageDictionary(outputDirectory, shapeFileDirectory)

    date, shapeFile = selectParameters(dictionary)

    # open an output image in order to get crs
    source = outputDirectory + '/' + date + '/' + shapeFile + '/' + dictionary[date][shapeFile][0]
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
    shape = shapeFileDirectory + '/' + shapeFile + '/' + shapeFile + '.shp'
    bathymetry_crop, meta = prepareImageGPD(shape, destinationFile)

    # Overwrite the destination file created before with the cropped image
    with rasterio.open(destinationFile, "w", **meta) as dst:
        dst.write(bathymetry_crop)
