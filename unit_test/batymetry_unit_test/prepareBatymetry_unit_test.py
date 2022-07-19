import numpy as np

from bathymetry_utils import *

bathymetryfilePath = "E:/LGO/ressource/MNT_COTIER_MORBIHAN_TANDEM_PBMA/MNT_COTIER_MORBIHAN_TANDEM_PBMA/DONNEES/MNT_COTIER_MORBIHAN_TANDEM_20m_WGS84_PBMA_ZNEG.bag"
outputBathymetrytDirectory = "E:/LGO/ressource/output_bathymetry"
outputDirectory = "E:/LGO/ressource/output"
shapeFileDirectory = "E:/LGO/ressource/shapeFile"


#prepareBathymetry(bathymetryfilePath, outputBathymetrytDirectory, outputDirectory, shapeFileDirectory)


# check data
with rasterio.open(bathymetryfilePath) as src:
    bathymetry_src = src.read(1)

dictionary = imageDictionary(outputDirectory, shapeFileDirectory)

date, shapeFile = selectParameters(dictionary)

# open an output image in order to get crs
source = outputDirectory + '/' + date + '/' + shapeFile + '/' + dictionary[date][shapeFile][0]
with rasterio.open(source) as src:
    img = src.read(1)
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

# check data
with rasterio.open(destinationFile) as src:
    bathymetry_dst = src.read(1)
    profil_bathymetry_dst = src.profile

# crop 
shape = shapeFileDirectory + '/' + shapeFile + '/' + shapeFile + '.shp'
bathymetry_crop, meta = prepareImageGPD(shape, destinationFile)

# Overwrite the destination file created before with the cropped data
with rasterio.open(destinationFile, "w", **meta) as dest:
    dest.write(bathymetry_crop)

# complete with zero if its required
with rasterio.open(destinationFile) as src:
    bathymetry_final = src.read(1)

plt.figure()
plt.imshow(bathymetry_final)
plt.title("bathymetrie")

'''# open an output image in order to get crs
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
    dst.write(bathymetry_crop)'''