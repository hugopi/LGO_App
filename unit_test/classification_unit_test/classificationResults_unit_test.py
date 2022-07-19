from unsupervised_classification_utils import *
from bathymetry_utils import *

bathymetryfilePath = "E:/LGO/ressource/MNT_COTIER_MORBIHAN_TANDEM_PBMA/MNT_COTIER_MORBIHAN_TANDEM_PBMA/DONNEES/MNT_COTIER_MORBIHAN_TANDEM_20m_WGS84_PBMA_ZNEG.bag"
outputBathymetrytDirectory = "E:/LGO/ressource/output_bathymetry"
outputDirectory = "E:/LGO/ressource/output"
shapeFileDirectory = "E:/LGO/ressource/shapeFile"
k = 30

# source, image_classified, prediction = classificationResults(outputDirectory,shapeFileDirectory, k)

dictionary = imageDictionary(outputDirectory, shapeFileDirectory)

date, shapeFile = selectParameters(dictionary)

source = outputDirectory + "/" + date + "/" + shapeFile + "/" + dictionary[date][shapeFile][0]

# Create a dataset with image data
dataset = fillDataset(shapeFile, date, dictionary, outputDirectory)

# do separation between earth and sea in order to classify only sea pixels
separation = earthAndSea(dataset)

# modify dataset with bathymetry
prepareBathymetry(bathymetryfilePath,outputBathymetrytDirectory,shapeFileDirectory,source,shapeFile)
bathymetryFile = outputBathymetrytDirectory + '/' + shapeFile + '/' + "MNT_COTIER_MORBIHAN_TANDEM_20m_WGS84_PBMA_ZNEG.bag"
bathymetryData = bathymetricData(bathymetryFile,source)

dataset = np.concatenate((dataset, bathymetryData), axis=1)
# classification of sea pixels
prediction = classification(separation, dataset, k,invert=True)

# Get the shape of the image we want to display
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
