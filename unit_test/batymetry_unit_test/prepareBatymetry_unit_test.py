import numpy as np
from matplotlib import pyplot as plt
from imagePreparation_utils import *

bathymetryfilePath = "E:/LGO/ressource/MNT_COTIER_MORBIHAN_TANDEM_PBMA/MNT_COTIER_MORBIHAN_TANDEM_PBMA/DONNEES/MNT_COTIER_MORBIHAN_TANDEM_20m_WGS84_PBMA_ZNEG.bag"
outputBathymetrtDirectory = "E:/LGO/ressource/output_bathymetry"
outputDirectory = "E:/LGO/ressource/output"
shapeFileDirectory = "E:/LGO/ressource/shapeFile"

dictionary = imageDictionary(outputDirectory, shapeFileDirectory)

date, shapeFile = selectParameters(dictionary)

print('Bathymetric data in preparation')

destination = outputBathymetrtDirectory + "/" + shapeFile
destinationFile = destination + '/' + 'MNT_COTIER_MORBIHAN_TANDEM_20m_WGS84_PBMA_ZNEG.bag'

# if destination directory not exist create it, else overwrite
path = Path(destination)
path.mkdir(parents=True, exist_ok=True)

# copy the source file in the destination directory
shutil.copy2(bathymetryfilePath, destinationFile)

shapeFilePath = shapeFileDirectory + "/" + shapeFile + "/" + shapeFile + ".shp"

# crop the bathymetric data
baty, meta = prepareImageGPD(shapeFilePath, destinationFile)

# Overwrite the destination file created before with the cropped image
with rasterio.open(destinationFile, "w", **meta) as dest:
    dest.write(baty)

with rasterio.open(destinationFile) as src:
    img = src.read(1)

img = np.kron(img, np.ones((2, 2)))


with rasterio.open("E:/LGO/ressource/output/date1/GDM1/T30TWT_20220506T110621_B02.jp2") as src:
    img2 = src.read(1)


plt.figure()
plt.imshow(img)
plt.title("herbier")