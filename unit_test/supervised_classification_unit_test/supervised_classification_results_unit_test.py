from supervised_classification_utils import *


csvPath = "E:/LGO/ressource/sortie_bateau.csv"
outputDirectory = "E:/LGO/ressource/output"
shapeFileDirectory = "E:/LGO/ressource/shapeFile"
k = 30

dictionary = imageDictionary(outputDirectory, shapeFileDirectory)

target,features = target_features(outputDirectory, csvPath, dictionary)

model = fitSupervised(target,features)

date, shapeFile = selectParameters(dictionary)

dataset = fillDataset(shapeFile, date, dictionary, outputDirectory)

separation = earthAndSea(dataset)

sea = seaDataset(dataset,separation,invert=True)*65535

prediction = model.predict(sea)

# Recover the full dataset : earth,sea,class
# add a column prediction
sea.insert(sea.shape[1], "Prediction", prediction, allow_duplicates=False)
# add all rows corresponding to earth by reindexing with 0 value
index = np.arange(0, dataset.shape[0], 1)
data = sea.reindex(index, fill_value=0)


source = outputDirectory + "/" + date + "/" + shapeFile + "/" + dictionary[date][shapeFile][0]

with rasterio.open(source) as src:
    img = src.read(1)
    shape = img.shape
pred = data['Prediction'].to_numpy()
img_classified = pred.reshape(shape[0],shape[1])

plt.figure()
plt.imshow(img_classified)
plt.title("herbier : supervised (SVM)")



