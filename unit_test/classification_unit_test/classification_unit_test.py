from unsupervised_classification_utils import *

outputDirectory = "E:/LGO/ressource/output"
shapeFileDirectory = "E:/LGO/ressource/shapeFile"

k = 30

dictionary = imageDictionary(outputDirectory, shapeFileDirectory)

date, shapeFile = selectParameters(dictionary)

dataset = fillDataset(shapeFile, date, dictionary, outputDirectory)

# classify the pixels of the dataset between earth and sea
separation = earthAndSea(dataset)

# create a dataset only with sea pixels
sea = seaDataset(dataset,separation,invert=True)

# define classification model (kmeans) and the number of clusters desired
kmeans = KMeans(n_clusters=k, random_state=0)
# take a sample of the dataset in order to train the algorithm
trainingDataset = sea.sample(frac=0.5, random_state=1)
# train the algorithm
kmeans.fit(trainingDataset)

# pixels classified in k class
prediction = kmeans.predict(sea)
# add 2 in order to differentiate those class from earth/sea class
prediction += 2

# Recover the full dataset : earth,sea,class
# add a column prediction
sea.insert(sea.shape[1], "Prediction", prediction, allow_duplicates=False)
# add all rows corresponding to earth by reindexing with 0 value
index = np.arange(0, dataset.shape[0], 1)
data = sea.reindex(index, fill_value=0)
