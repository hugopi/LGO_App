import pandas as pd

from dataset_utils import *

csvPath = "E:/LGO/ressource/sortie_bateau.csv"
outputDirectory = "E:/LGO/ressource/output"
shapeFileDirectory = "E:/LGO/ressource/shapeFile"
shapeFile = "GDM1"
date = "date1"

dictionary = imageDictionary(outputDirectory,shapeFileDirectory)
source = outputDirectory + "/" + date + "/" + shapeFile +"/" + dictionary[date][shapeFile][0]

#data = samples(csvPath, source)

"""data = pd.read_csv(csvPath, sep=';')

sampleDictionary = {'id': [], 'geometry': []}

for i in data.index:
    x = data['Est'][i]
    y = data['Nord'][i]
    id = data['id'][i]

    sampleDictionary['geometry'].append(Point(x, y))
    sampleDictionary['id'].append(id)

with rasterio.open(source) as src:
    profile_src = src.profile
    sampleGeoData = gpd.GeoDataFrame(sampleDictionary, crs=4326)
    sampleGeoData = sampleGeoData.to_crs(profile_src['crs'])


for i in range(len(sampleGeoData['geometry'])):
    data['Nord'][i] = sampleGeoData['geometry'][i].x
    data['Est'][i] = sampleGeoData['geometry'][i].y"""


