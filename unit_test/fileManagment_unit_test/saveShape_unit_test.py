from unsupervised_classification_utils import *
import cv2

# Path to directory where satellite images are stored
inputDirectoryPath = "E:/LGO/ressource/input"
# Path to directory where your prepared images will be stored
outputDirectoryPath = "E:/LGO/ressource/output"
# Path to your desired shapeFile
shapeFileDirectoryPath = "E:/LGO/ressource/shapeFile"
savingShapeDirectory = "E:/LGO/ressource/savingShape"
k = 30

source, img_classified, prediction = classificationResults(outputDirectoryPath, shapeFileDirectoryPath, k,
                                                           invert=True)
wantedClass = int(input("write the number of the class you want to see :"))
img_herbier = copy.deepcopy(img_classified)
img_herbier[img_herbier != wantedClass] = 0

### save img classified

# create a destinationFile name
split = source.split('/')
destinationFile = split[-3] + '_' + split[-2] + '_' + 'classification' + '.jpeg'
destination = savingShapeDirectory + '/' + split[-3] + '/' + split[-2]

# if destination directory not exist create it, else overwrite
path = Path(destination)
path.mkdir(parents=True, exist_ok=True)

plt.imsave(destination + "/" + destinationFile, img_classified)

### save img herbier
# create a destinationFile name
split = source.split('/')
destinationFile = split[-3] + '_' + split[-2] + '_' + 'class' + '_' + str(wantedClass) + '.jpeg'
destination = savingShapeDirectory + '/' + split[-3] + '/' + split[-2] + '/' + 'class' + '_' + str(wantedClass)

# if destination directory not exist create it, else overwrite
path = Path(destination)
path.mkdir(parents=True, exist_ok=True)

plt.imsave(destination + "/" + destinationFile, img_herbier)

### contouring
im = cv2.imread(destination + "/" + destinationFile)
imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 127, 255, 0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
draw = cv2.drawContours(im, contours, -1, (0, 255, 0), 3)
cv2.imshow('contour', draw)
'''
#### save shapeFile 
# find the coordinates of herbier pixels
xyList = []

with rasterio.open(source) as src:
    crs_source = src.crs

    for i in range(img_herbier.shape[0]):
        for j in range(img_herbier.shape[1]):
            if img_herbier[i, j] != 0:
                xyList.append(src.xy(i, j))

# define schema
schema = {
    'geometry': 'Point',
    'properties': [('Name', 'str')]
}

# create a destinationFile name
split = source.split('/')
destinationFile = split[-3] + '_' + split[-2] + '_' + 'class' + '_' + str(wantedClass) + '.shp'
destination = savingShapeDirectory + '/' + split[-3] + '/' + split[-2] + '/' + 'class' + '_' + str(wantedClass)

# if destination directory not exist create it, else overwrite
path = Path(destination)
path.mkdir(parents=True, exist_ok=True)

destination = destination + '/' + destinationFile

# open a fiona object
pointShp = fiona.open(destination, mode='w', driver='ESRI Shapefile',
                     schema=schema, crs=crs_source)


for i in xyList:
    rowDict = {
        'geometry' : {'type':'Point',
                     'coordinates': (i[0],i[1])},
        'properties': {'Name' : 'point'},
    }
    pointShp.write(rowDict)
#close fiona object
pointShp.close()
'''
