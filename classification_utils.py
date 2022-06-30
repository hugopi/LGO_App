import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from dataset_utils import *
import pandas as pd


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


def classification(separation, dataset, k):
    # transform separation into dataframe
    separationDataframe = pd.DataFrame(separation)
    # rename the column
    separationDataframe.columns = ['prediction']
    # transform dataset into dataframe
    dataframe = pd.DataFrame(dataset)
    # Create a dataset containing pixels and their class : earth or sea
    datasetWithPrediction = pd.concat((dataframe, separationDataframe), axis=1)
    # Drop all lines classified as earth
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
    datasetWithPrediction.insert(datasetWithPrediction.shape[1], "Prediction", prediction, allow_duplicates=False)
    index = np.arange(0, dataset.shape[0], 1)
    datasetWithPrediction = datasetWithPrediction.reindex(index, fill_value=0)

    return datasetWithPrediction['Prediction'].to_numpy()


def classificationResults(outputDirectory, dictionary, date, shapeFile, k):

    # Create a dataset with image data
    dataset = fillDataset(shapeFile, date, dictionary, outputDirectory)

    # do separation between earth and sea in order to classify only sea pixels
    separation = earthAndSea(dataset)

    # classification of sea pixels
    prediction = classification(separation, dataset, k)

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
    plt.title("output Image")

    return source, img_classified, prediction
