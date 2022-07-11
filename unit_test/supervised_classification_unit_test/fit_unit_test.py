from supervised_classification_utils import *
from unsupervised_classification_utils import *

csvPath = "E:/LGO/ressource/sortie_bateau.csv"
outputDirectory = "E:/LGO/ressource/output"
shapeFileDirectory = "E:/LGO/ressource/shapeFile"

dictionary = imageDictionary(outputDirectory, shapeFileDirectory)

target, features = target_features(outputDirectory, csvPath, dictionary)

# choose the model you want
model = input('Choose your supervised model : SVM, NeuralNetwork')

if model == 'SVM':
    # model fit with target and features data
    clf = svm.SVC(kernel='linear', C=1).fit(features, target)
    # prediction test
    predictionTest = clf.predict(features)
    # score of the prediction
    score = clf.score(features, target)
    print('score : ', score)

if model == 'NeuralNetwork':
    # model fit with target and features data
    clf = neural_network.MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
    clf.fit(features, target)
    # prediction test
    predictionTest = clf.predict(features)
    # score of the prediction
    score = clf.score(features, target)
    print('score : ', score)