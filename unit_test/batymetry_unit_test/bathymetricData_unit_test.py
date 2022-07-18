from bathymetry_utils import *
from unsupervised_classification_utils import *

bathymetryfilePath = "E:/LGO/ressource/MNT_COTIER_MORBIHAN_TANDEM_PBMA/MNT_COTIER_MORBIHAN_TANDEM_PBMA/DONNEES/MNT_COTIER_MORBIHAN_TANDEM_20m_WGS84_PBMA_ZNEG.bag"
outputBathymetrtDirectory = "E:/LGO/ressource/output_bathymetry"
outputDirectory = "E:/LGO/ressource/output"
shapeFileDirectory = "E:/LGO/ressource/shapeFile"

dictionary = imageDictionary(outputDirectory, shapeFileDirectory)

date, shapeFile = selectParameters(dictionary)

prepareBathymetry(bathymetryfilePath, outputBathymetrtDirectory, shapeFileDirectory, shapeFile)

source = "E:/LGO/ressource/output/date1/GDM1/T30TWT_20220506T110621_B02.jp2"
bathymetryFile = "E:/LGO/ressource/output_bathymetry/GDM1/MNT_COTIER_MORBIHAN_TANDEM_20m_WGS84_PBMA_ZNEG.bag"

'''with rasterio.open(source) as src:
    img = src.read(1)
    shape = img.shape

    coordinateList = []

    for row in range(img.shape[0]):
        for col in range(img.shape[1]):
            coordinateList.append(src.xy(row, col))'''

### convert bathy coordinates
with rasterio.open(source) as src:
    profile_src = src.profile

with rasterio.open(bathymetryFile) as src:
    bat = src.read(1)
    coordinateList = []

    bathyDictionary = {'id': [], 'geometry': []}

    for row in range(bat.shape[0]):
        for col in range(bat.shape[1]):
            point = src.xy(row, col)
            bathyDictionary['geometry'].append(Point(point[0], point[1]))
            bathyDictionary['id'].append(str(row) + '_' + str(col))

    bathyGeoData = gpd.GeoDataFrame(bathyDictionary, crs=4326)
    bathyGeoData = bathyGeoData.to_crs(profile_src['crs'])

### create a dataFrame with bathy value and coordinates

nord = []
est = []
for i in bathyGeoData['geometry']:
    nord.append(i.y)
    est.append(i.x)

d = {'value': bat.reshape(bat.shape[0] * bat.shape[1]),
     'Nord': nord,
     'Est': est}

bathyDataframe = pd.DataFrame(d)

### choose only the point you want

top = -0.8
bottom = -1.2

bathyDataframe = bathyDataframe[bathyDataframe.value <= top]
bathyDataframe = bathyDataframe[bathyDataframe.value >= bottom]

dataset = fillDataset(shapeFile, date, dictionary, outputDirectory)

# classify the pixels of the dataset between earth and sea
separation = earthAndSea(dataset)

# create a dataset only with sea pixels
sea = seaDataset(dataset, separation, invert=True)
