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
# Path to your bathymetry data file
bathymetryfilePath = "E:/LGO/ressource/MNT_COTIER_MORBIHAN_TANDEM_PBMA/MNT_COTIER_MORBIHAN_TANDEM_PBMA/DONNEES/MNT_COTIER_MORBIHAN_TANDEM_20m_WGS84_PBMA_ZNEG.bag"
# Path to the directory where updated batymetry will be saved
outputBathymetrytDirectory = "E:/LGO/ressource/output_bathymetry"

# if you want to prepare your images set this flag to 1
flag_preparation = 0
# if you want to do k-means classification set this flag to 1
flag_classification = 1
# if you want to see herbier detection set this flag to 1
flag_herbierDetection = 0

if flag_preparation == 1:
    imagePreparation(inputDirectoryPath, outputDirectoryPath, shapeFileDirectoryPath)

if flag_classification == 1:
    source, image_classified, prediction = classificationResults(outputDirectoryPath, shapeFileDirectoryPath, bathymetryfilePath, outputBathymetrytDirectory, 30,
                          invert=True, bathymetry=False)
    wantedClass(image_classified, savingShapeDirectory, source)

if flag_herbierDetection == 1:
    herbierDetection(outputDirectoryPath, shapeFileDirectoryPath, csvPath, 30, invert=True)
