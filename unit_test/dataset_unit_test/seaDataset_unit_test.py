from unsupervised_classification_utils import *

csvPath = "E:/LGO/ressource/sortie_bateau.csv"
outputDirectory = "E:/LGO/ressource/output"
shapeFileDirectory = "E:/LGO/ressource/shapeFile"

dictionary = imageDictionary(outputDirectory, shapeFileDirectory)

date, shapeFile = selectParameters(dictionary)

dataset = fillDataset(shapeFile, date, dictionary, outputDirectory)

separation = earthAndSea(dataset)
# transform separation into dataframe
separationDataframe = pd.DataFrame(separation)
# rename the column
separationDataframe.columns = ['prediction']
# transform dataset into dataframe
dataframe = pd.DataFrame(dataset)
# Create a dataset containing pixels and their class : earth or sea
datasetWithPrediction = pd.concat((dataframe, separationDataframe), axis=1)
invert = True
# Drop all lines classified as earth
if invert:
    datasetWithPrediction.drop(datasetWithPrediction.loc[datasetWithPrediction['prediction'] == 0].index, inplace=True)
else:
    datasetWithPrediction.drop(datasetWithPrediction.loc[datasetWithPrediction['prediction'] == 1].index, inplace=True)
# remove the class column
del datasetWithPrediction['prediction']
