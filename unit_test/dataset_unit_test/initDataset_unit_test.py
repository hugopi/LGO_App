from fileManagment_utils import *
from dataset_utils import *

outputDirectory = "E:/LGO/ressource/output"
shapeFileDirectory = "E:/LGO/ressource/shapeFile"

shapeFile = "GDM1"
date = "date1"
dictionary = imageDictionary(outputDirectory,shapeFileDirectory)

#dataset = initDataset(shapeFile,date,dictionary,outputDirectory)

listOfImage = dictionary[date][shapeFile]

template = outputDirectory + "/" + date + "/" + shapeFile + "/" + listOfImage[0]

columns = len(listOfImage)
with rasterio.open(template) as src:
    img_template = src.read(1)
    shape_template = img_template.shape
    dataset = np.zeros((shape_template[0] * shape_template[1], columns))