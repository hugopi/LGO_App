from imagePreparation_utils import *
from unsupervised_classification_utils import *

# Path to directory where satellite images are stored
inputDirectoryPath = "E:/LGO/ressource/input"
# Path to directory where your prepared images will be stored
outputDirectoryPath = "E:/LGO/ressource/output"
# Path to your desired shapeFile
shapeFileDirectoryPath = "E:/LGO/ressource/shapeFile"
# Path to directory where you want to save results
savingShapeDirectory = "E:/LGO/ressource/savingShape"
# Path to your csv file
csvPath = "E:/LGO/ressource/sortie_bateau.csv"

# if you want to prepare your images set this flag to 1
flag_preparation = 0
# if you want to do k-means classification set this flag to 1
flag_classification = 1
# if you want to see herbier detection set this flag to 1
flag_herbierDetection = 0

if flag_preparation == 1:
    imagePreparation(inputDirectoryPath, outputDirectoryPath, shapeFileDirectoryPath)

if flag_classification == 1:
    source, image_classified, prediction = classificationResults(outputDirectoryPath, shapeFileDirectoryPath, 30,
                                                                 invert=False)
    wantedClass(image_classified, savingShapeDirectory, source)

if flag_herbierDetection == 1:
    herbierDetection(outputDirectoryPath, shapeFileDirectoryPath, csvPath, 30, invert=True)
