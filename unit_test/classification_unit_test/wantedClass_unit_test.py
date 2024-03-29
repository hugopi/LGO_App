from unsupervised_classification_utils import *

outputDirectory = "E:/LGO/ressource/output"
shapeFileDirectory = "E:/LGO/ressource/shapeFile"
savingShapeDirectory = "E:/LGO/ressource/savingShape"
k = 30

source, img_classified, prediction = classificationResults(outputDirectory, shapeFileDirectory, k,invert= True)

wantedClass = int(input("write the number of the class you want to see :"))

img_herbier = copy.deepcopy(img_classified)

img_herbier[img_herbier != wantedClass] = 0

save = input('Do you want to save the result as .shp : yes or no')

if save == 'yes':
    saveShape(savingShapeDirectory, img_herbier, wantedClass, source)

plt.figure()
plt.imshow(img_herbier)
plt.title("herbier")
