from sklearn.model_selection import train_test_split
from sklearn import *
from unsupervised_classification_utils import *
from collections import Counter

csvPath = "E:/LGO/ressource/sortie_bateau.csv"
outputDirectory = "E:/LGO/ressource/output"
shapeFileDirectory = "E:/LGO/ressource/shapeFile"
k = 30

dictionary = imageDictionary(outputDirectory, shapeFileDirectory)

target,features = target_features(outputDirectory, csvPath, dictionary)


X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.4, random_state=0)

clf = svm.SVC(kernel='linear', C=1).fit(features, target)
predictionTest = clf.predict(X_test)
score = clf.score(X_test, y_test)

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

datasetSea = datasetWithPrediction*65535

prediction = clf.predict(datasetSea)

# Recover the full dataset : earth,sea,class
# add a column prediction
datasetSea.insert(datasetWithPrediction.shape[1], "Prediction", prediction, allow_duplicates=False)
# add all rows corresponding to earth by reindexing with 0 value
index = np.arange(0, dataset.shape[0], 1)
datasetSea = datasetSea.reindex(index, fill_value=0)


source = outputDirectory + "/" + date + "/" + shapeFile + "/" + dictionary[date][shapeFile][0]

with rasterio.open(source) as src:
    img = src.read(1)
    shape = img.shape
pred = datasetSea['Prediction'].to_numpy()
img_classified = pred.reshape(shape[0],shape[1])

plt.figure()
plt.imshow(img_classified)
plt.title("herbier : supervised (SVM)")



