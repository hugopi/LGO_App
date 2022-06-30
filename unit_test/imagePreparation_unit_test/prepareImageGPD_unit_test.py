from imagePreparation_utils import *

shapeFile = "/Users/pires/PycharmProjects/LGO/application/shapeFile/GDM1/GDM1.shp"
source = "/Users/pires/PycharmProjects/LGO/application/ressource/input_image/date1/T30TWT_20220506T110621_B02.jp2"

#img, metha = prepareImageGPD(shapeFile,source)

# Open the shapeFile
shapeFile = gpd.read_file(shapeFile)

# Open the source image we want to crop, reproject the shapefile in the correct projection, create a cropped image
with rasterio.open(source) as src:
    img_src = src.read(1)
    profile_src = src.profile
    shapeFileReprojected = shapeFile.to_crs(profile_src['crs'])
    imgCrop, imgCropMeta = es.crop_image(src, shapeFileReprojected)