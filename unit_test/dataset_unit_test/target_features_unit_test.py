from unsupervised_classification_utils import *

csvPath = "E:/LGO/ressource/sortie_bateau.csv"
outputDirectory = "E:/LGO/ressource/output"
shapeFileDirectory = "E:/LGO/ressource/shapeFile"

dictionary = imageDictionary(outputDirectory, shapeFileDirectory)

# target, features = target_features(outputDirectory, csvPath, dictionary)

data = samples(outputDirectory, csvPath, dictionary)

dataWithPixel = pixelRecover(data, outputDirectory, dictionary)

target = dataWithPixel['herbier']
features = np.zeros((target.shape[0], len(dataWithPixel['pixel'][0])))

for i in range(features.shape[0]):
    for j in range(features.shape[1]):
        features[i, j] = dataWithPixel['pixel'][i][j]
