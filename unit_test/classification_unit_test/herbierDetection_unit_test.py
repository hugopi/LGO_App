from unsupervised_classification_utils import *
from collections import Counter

csvPath = "E:/LGO/ressource/sortie_bateau.csv"
outputDirectory = "E:/LGO/ressource/output"
shapeFileDirectory = "E:/LGO/ressource/shapeFile"
k = 30
invert = False


#herbierDetection(outputDirectory,shapeFileDirectory,csvPath,k,invert = False)

source, img_classified, prediction = classificationResults(outputDirectory, shapeFileDirectory, k,invert)
data = samples(csvPath,source)
validIndex = findValidIndex(source,data)

if len(validIndex) == 0:
    print("no valid data in this zone")
else:
    herbierClass = []
    for i in validIndex:
        herbierClass.append(img_classified[i[0],i[1]])

    h = Counter(herbierClass).keys()
    img_herbier = img_classified

    for i in h:

        img_herbier[img_herbier == i] = 100

    img_herbier[img_herbier != 100] = 0
    plt.figure()
    plt.imshow(img_herbier)
    plt.title("herbier")