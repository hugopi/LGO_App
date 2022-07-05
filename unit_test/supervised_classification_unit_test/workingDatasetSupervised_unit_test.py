from sklearn.model_selection import train_test_split
from sklearn import *
from unsupervised_classification_utils import *
from collections import Counter

csvPath = "E:/LGO/ressource/sortie_bateau.csv"
outputDirectory = "E:/LGO/ressource/output"
shapeFileDirectory = "E:/LGO/ressource/shapeFile"
k = 30

dictionary = imageDictionary(outputDirectory, shapeFileDirectory)

date, shapeFile = selectParameters(dictionary)

dataset = fillDataset(shapeFile, date, dictionary, outputDirectory)

crs_template = outputDirectory + "/" + date + "/" + shapeFile + "/" + dictionary[date][shapeFile][0]
data = samples(csvPath, crs_template)

dataWithPixel = pixelRecover(data,outputDirectory,dictionary)

target = dataWithPixel['herbier']
features = np.zeros((target.shape[0],len(dataWithPixel['pixel'][0])))

for i in range(features.shape[0]):
    for j in range(features.shape[1]):
        features[i,j] = dataWithPixel['pixel'][i][j]


X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.4, random_state=0)

clf = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)
score = clf.score(X_test, y_test)

prediction = clf.predict(dataset)



