import geopandas as gpd
import earthpy.spatial as es
import shutil
from osgeo import gdal

from fileManagment_utils import *


def prepareImageGPD(shapeFilePath, source):
    # description : feed with a shapeFile and an image, you will get the image cropped
    # Open the shapeFile
    shapeFile = gpd.read_file(shapeFilePath)

    # Open the source image we want to crop
    with rasterio.open(source) as src:
        profile_src = src.profile
        # reproject the shapefile in the correct projection
        shapeFileReprojected = shapeFile.to_crs(profile_src['crs'])
        # create a cropped image
        imgCrop, imgCropMeta = es.crop_image(src, shapeFileReprojected)

    return imgCrop, imgCropMeta


def imagePreparation(inputDirectory, outputDirectory, shapeFileDirectory):
    # description : the function will browse all input images, prepare them and store them
    # list the directories (different dates) in the input directory
    listOfDirectories = fileList(inputDirectory)
    # list the shapeFiles (different dates) in the shapeFile directory
    listOfShapeFiles = fileList(shapeFileDirectory)

    # create a dictionary {'date': ['image_name'],'date': ['image_name']}
    listOfImages = {}
    for i in listOfDirectories:
        d = {i: fileList(inputDirectory + "/" + i)}
        listOfImages.update(d)

    for i in listOfDirectories:
        for j in listOfImages[i]:
            for k in listOfShapeFiles:
                sourceFile = inputDirectory + "/" + i + "/" + j
                destination = outputDirectory + "/" + i + "/" + k
                destinationFile = outputDirectory + "/" + i + "/" + k + "/" + j

                # if destination directory not exist create it, else overwrite
                path = Path(destination)
                path.mkdir(parents=True, exist_ok=True)

                # copy the source file in the destination directory
                shutil.copy2(sourceFile, destinationFile)

                # update resolution
                gdal.Warp(destinationFile, sourceFile, xRes=10, yRes=10)

                # get the correct shapeFile
                shapeFile = shapeFileDirectory + "/" + k + "/" + k + ".shp"

                # Prepare the image (crop)
                img, metha = prepareImageGPD(shapeFile, destinationFile)

                print(i, j, " with ", k, " Prepared")

                # Overwrite the destination file created before with the cropped image
                with rasterio.open(destinationFile, "w", **metha) as dest:
                    dest.write(img)
