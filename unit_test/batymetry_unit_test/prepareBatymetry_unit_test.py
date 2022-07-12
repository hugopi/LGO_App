from matplotlib import pyplot as plt
from imagePreparation_utils import *

filePath = "E:/LGO/ressource/MNT_COTIER_MORBIHAN_TANDEM_PBMA/MNT_COTIER_MORBIHAN_TANDEM_PBMA/DONNEES/MNT_COTIER_MORBIHAN_TANDEM_20m_WGS84_PBMA_ZNEG.bag"
shapeFile = "E:/LGO/ressource/shapeFile/GDM1/GDM1.shp"
output = "E:/LGO/ressource/output"


with rasterio.open(filePath) as src:
    bat = src.read(1)
    profile = src.profile
    x, y = (src.bounds.left, src.bounds.top)
    row, col = src.index(x, y)
    pix = bat[row,col]
    coordone = src.xy(row,col)

plt.figure()
plt.imshow(bat)
plt.title("batymetry")



destination = output+ "/" + "test" + "/" + "baty"
destinationFile = destination + '/' + 'MNT_COTIER_MORBIHAN_TANDEM_20m_WGS84_PBMA_ZNEG.bag'

# if destination directory not exist create it, else overwrite
path = Path(destination)
path.mkdir(parents=True, exist_ok=True)

# copy the source file in the destination directory
shutil.copy2(filePath, destinationFile)

'''# update resolution
gdal.Warp(destinationFile, filePath, xRes=10, yRes=10)'''

baty, meta = prepareImageGPD(shapeFile,destinationFile)

# Overwrite the destination file created before with the cropped image
with rasterio.open(destinationFile, "w", **meta) as dest:
    dest.write(baty)

with rasterio.open(destinationFile) as src:
    img = src.read(1)

plt.figure()
plt.imshow(img)
plt.title("herbier")



