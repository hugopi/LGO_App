from imagePreparation_utils import *
import rasterio


def prepareBathymetry(bathymetryfilePath, outputDirectory, shapeFile):

    print('Bathymetric data in preparation')

    shapeName = shapeFile.split('/')[-2]
    destination = outputDirectory + "/" + shapeName
    destinationFile = destination + '/' + 'MNT_COTIER_MORBIHAN_TANDEM_20m_WGS84_PBMA_ZNEG.bag'

    # if destination directory not exist create it, else overwrite
    path = Path(destination)
    path.mkdir(parents=True, exist_ok=True)

    # copy the source file in the destination directory
    shutil.copy2(bathymetryfilePath, destinationFile)

    '''# update resolution
    gdal.Warp(destinationFile, filePath, xRes=10, yRes=10)'''

    # crop the bathymetric data
    baty, meta = prepareImageGPD(shapeFile, destinationFile)

    # Overwrite the destination file created before with the cropped image
    with rasterio.open(destinationFile, "w", **meta) as dest:
        dest.write(baty)
