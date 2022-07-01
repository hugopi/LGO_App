from classification_utils import *

csvPath = "E:/LGO/ressource/sortie_bateau.csv"
outputDirectory = "E:/LGO/ressource/output"
shapeFileDirectory = "E:/LGO/ressource/shapeFile"
shapeFile = "GDM1"
date = "date1"
k = 30


#herbierDetection(outputDirectory,shapeFileDirectory,csvPath,k)

source, img_classified, prediction = classificationResults(outputDirectory, shapeFileDirectory, k)
data = samples(csvPath,source)
row,col = findValidIndex(source,data)

herbier = img_classified[row, col]
img_herbier = img_classified

img_herbier[img_herbier != herbier] = 0

plt.figure()
plt.imshow(img_herbier)
plt.title("herbier")