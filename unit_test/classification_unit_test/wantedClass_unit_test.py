from unsupervised_classification_utils import *

outputDirectory = "E:/LGO/ressource/output"
shapeFileDirectory = "E:/LGO/ressource/shapeFile"
k = 30


source, img_classified, prediction = classificationResults(outputDirectory,shapeFileDirectory, k)

wantedClass = int(input("write the number of the class you want to see :"))

img_herbier = copy.deepcopy(img_classified)

img_herbier[img_herbier != wantedClass] = 0

plt.figure()
plt.imshow(img_herbier)
plt.title("herbier")