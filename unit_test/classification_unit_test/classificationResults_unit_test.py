from classification_utils import*

outputDirectory = "E:/LGO/ressource/output"
shapeFileDirectory = "E:/LGO/ressource/shapeFile"
shapeFile = "GDM1"
date = "date1"
k = 30


#source, image_classified, prediction = classificationResults(outputDirectory,shapeFileDirectory, k)

dictionary = imageDictionary(outputDirectory,shapeFileDirectory)

date,shapeFile = selectParameters(dictionary)

# Create a dataset with image data
dataset = fillDataset(shapeFile,date,dictionary,outputDirectory)

# do separation between earth and sea in order to classify only sea pixels
separation = earthAndSea(dataset)

# classification of sea pixels
prediction = classification(separation, dataset, k)

# Get the shape of the image we want to display
source = outputDirectory + "/" + date + "/" + shapeFile +"/" + dictionary[date][shapeFile][0]
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