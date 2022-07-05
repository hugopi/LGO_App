from unsupervised_classification_utils import *

outputDirectory = "E:/LGO/ressource/output"
shapeFileDirectory = "E:/LGO/ressource/shapeFile"

k = 30

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
invert = False
# Drop all lines classified as earth
if invert:
    datasetWithPrediction.drop(datasetWithPrediction.loc[datasetWithPrediction['prediction'] == 0].index, inplace=True)
else:
    datasetWithPrediction.drop(datasetWithPrediction.loc[datasetWithPrediction['prediction'] == 1].index, inplace=True)
# remove the class column
del datasetWithPrediction['prediction']

# define classification model (kmeans) and the number of clusters desired
kmeans = KMeans(n_clusters=k, random_state=0)
# take a sample of the dataset in order to train the algorithm
trainingDataset = datasetWithPrediction.sample(frac=0.5, random_state=1)
# train the algorithm
kmeans.fit(trainingDataset)

# pixels classified in k class (goal find wich class correspond to herbier =
prediction = kmeans.predict(datasetWithPrediction)
# add 2 in order to differentiate those class from earth/sea class
prediction += 2

# Recover the full dataset : earth,sea,class
# add a column prediction
datasetWithPrediction.insert(datasetWithPrediction.shape[1], "Prediction", prediction, allow_duplicates=False)
# add all rows corresponding to earth by reindexing with 0 value
index = np.arange(0, dataset.shape[0], 1)
datasetWithPrediction = datasetWithPrediction.reindex(index, fill_value=0)
