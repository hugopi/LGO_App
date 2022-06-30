from classification_utils import *

outputDirectory = "E:/LGO/ressource/output"
shapeFileDirectory = "E:/LGO/ressource/shapeFile"
shapeFile = "GDM1"
date = "date1"

dictionary = imageDictionary(outputDirectory,shapeFileDirectory)

dataset = fillDataset(shapeFile,date,dictionary,outputDirectory)

#separation = earthAndSea(dataset)
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

source = outputDirectory + "/" + date + "/" + shapeFile +"/" + dictionary[date][shapeFile][0]
with rasterio.open(source) as src:
    img = src.read(1)
    shape = img.shape

image_predicted = prediction.reshape((shape[0],shape[1]))

# Plots
plt.figure()
plt.imshow(image_predicted)
plt.title("Input Image")