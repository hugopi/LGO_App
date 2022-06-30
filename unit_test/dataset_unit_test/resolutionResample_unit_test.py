from fileManagment_utils import *
from dataset_utils import *

outputDirectory = "E:/LGO/ressource/output"
shapeFileDirectory = "E:/LGO/ressource/shapeFile"
shapeFile = "GDM1"
date = "date1"

dictionary = imageDictionary(outputDirectory,shapeFileDirectory)
# dataset,key = fillDataset(outputDirectory,shapeFileDirectory)

dataset = initDataset(shapeFile,date,dictionary,outputDirectory)
dictionary = imageDictionary(outputDirectory, shapeFileDirectory)
listOfImage = dictionary[date][shapeFile]

template = outputDirectory + "/" + date + "/" + shapeFile + "/" + listOfImage[0]
source = outputDirectory + "/" + date + "/" + shapeFile + "/" + listOfImage[7]


#img = resolutionResample(template, source)

with rasterio.open(template) as src:
    img_template = src.read(1)
    shape_template = img_template.shape
    print(shape_template)

with rasterio.open(source) as src:
    img = src.read(1)
    print(img.shape)

    # Resample depending on the resolution
    if ("B05" in source) or ("B06" in source) or ("B07" in source) or ("B8A" in source) or (
            "B11" in source) or (
            "B12" in source):
        img = np.kron(img, np.ones((2, 2)))
        rowGap = img.shape[0] - shape_template[0]
        columnGap = img.shape[1] - shape_template[1]
        if rowGap == 0 and columnGap == 0:
            img = img
        if rowGap != 0 and columnGap == 0:
            img = img[:-rowGap, :]
        if rowGap == 0 and columnGap != 0:
            img = img[:, :-columnGap]
        if rowGap != 0 and columnGap != 0:
            img = img[:-rowGap, :-columnGap]

    print(img.shape)