import copy
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from dataset_utils import *
from collections import Counter
import pandas as pd
from fileManagment_utils import imageDictionary


def earthAndSea(dataset):
    # import the dataset as a pandas dataframe
    dataset = pd.DataFrame(dataset)

    # take a sample of the dataset in order to train the algorithm
    trainingDataset = dataset.sample(frac=0.5, random_state=1)

    # define classification model (kmeans) and the number of clusters desired
    kmeans = KMeans(n_clusters=2, random_state=0)

    # train the algorithm
    kmeans.fit(trainingDataset)

    # pixels classified in 2 class : earth and sea
    prediction = kmeans.predict(dataset)

    # reshape the prediction in order to use it
    prediction = prediction.reshape(prediction.shape[0], 1)

    return prediction


def classification(separation, dataset, k, invert=False):
    # create a dataset only with sea pixels
    sea = seaDataset(dataset, separation, invert)
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
    # full dataset recover
    data = sea.reindex(index, fill_value=0)

    return data['Prediction'].to_numpy()


def classificationResults(outputDirectory, shapeFileDirectory, k, invert):
    dictionary = imageDictionary(outputDirectory, shapeFileDirectory)

    # ask the date and the shapefile you want
    date, shapeFile = selectParameters(dictionary)

    print(" \n classification is running, wait a moment ")

    # Create a dataset with image data
    dataset = fillDataset(shapeFile, date, dictionary, outputDirectory)

    # do separation between earth and sea in order to classify only sea pixels
    separation = earthAndSea(dataset)

    # classification of sea pixels
    prediction = classification(separation, dataset, k, invert)

    # Get the shape of the image we want to display
    source = outputDirectory + "/" + date + "/" + shapeFile + "/" + dictionary[date][shapeFile][0]
    with rasterio.open(source) as src:
        img = src.read(1)
        shape = img.shape

    # Recover the image matrix with classified pixels
    img_classified = prediction.reshape(shape[0], shape[1])

    # Plots
    plt.figure()
    plt.imshow(img)
    plt.title("Input Image")

    plt.figure()
    plt.imshow(img_classified)
    plt.title("Classified Image : unsupervised (kmeans)")

    return source, img_classified, prediction


def herbierDetection(outputDirectory, shapeFileDirectory, csvPath, k, invert=False):
    source, img_classified, prediction = classificationResults(outputDirectory, shapeFileDirectory, k, invert)
    dictionary = imageDictionary(outputDirectory, shapeFileDirectory)
    data = samples(outputDirectory, csvPath, dictionary)
    validIndex = findValidIndex(source, data)

    if len(validIndex) == 0:
        print("no valid data in this zone")
    else:
        herbierClass = []
        for i in validIndex:
            herbierClass.append(img_classified[i[0], i[1]])

        h = Counter(herbierClass).keys()
        img_herbier = img_classified

        for i in h:
            img_herbier[img_herbier == i] = 100

        img_herbier[img_herbier != 100] = 0
        plt.figure()
        plt.imshow(img_herbier)
        plt.title("herbier : unsupervised (kmeans)")


def wantedClass(img_classified, savingShapeDirectory, source):
    wantedClass = int(input("write the number of the class you want to see :"))

    img_herbier = copy.deepcopy(img_classified)

    img_herbier[img_herbier != wantedClass] = 0

    save = input('Do you want to save the result as .shp : yes or no')

    if save == 'yes':
        saveShape(savingShapeDirectory, img_classified, img_herbier, wantedClass, source)

    plt.figure()
    plt.imshow(img_herbier)
    plt.title("herbier : unsupervised (kmeans)")
