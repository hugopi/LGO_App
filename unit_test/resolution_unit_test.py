import shutil

import rasterio
from osgeo import gdal
from fileManagment_utils import imageDictionary, fileList

inputDirectory = "E:/LGO/ressource/input"
out = "E:/LGO/test"
shapeFileDirectory = "E:/LGO/ressource/shapeFile"
shapeFile = "GDM1"
date = "date1"


listOfDirectories = fileList(inputDirectory)
listOfImages = {}
for i in listOfDirectories:
    d = {i: fileList(inputDirectory + "/" + i)}
    listOfImages.update(d)

source = inputDirectory+ "/" + date + "/" + listOfImages[date][6]
dest = out+'/'+ listOfImages[date][6]

shutil.copy2(source, dest)

with rasterio.open(source) as src:
    img = src.read(1)

gdal.Warp(dest, source, xRes=10, yRes=10)

with rasterio.open(dest) as dst:
    img2 = dst.read(1)