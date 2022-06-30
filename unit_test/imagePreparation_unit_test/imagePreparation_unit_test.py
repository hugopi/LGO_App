from imagePreparation_utils import *

inputDirectory = "E:/LGO/ressource/input"
outputDirectory = "E:/LGO/ressource/output"
shapeFileDirectory = "E:/LGO/ressource/shapeFile"

#imagePreparation(inputDirectory,outputDirectory,shapeFileDirectory)

listOfDirectories = fileList(inputDirectory)
listOfShapeFiles = fileList(shapeFileDirectory)

listOfImages = {}
for i in listOfDirectories:
    d = {i: fileList(inputDirectory + "/" + i)}
    listOfImages.update(d)


for i in listOfDirectories:
    for j in listOfImages[i]:
        for k in listOfShapeFiles:
            sourceFile = inputDirectory + "/" + i + "/" + j
            destination = outputDirectory + "/" + i + "/" + k
            destinationFile = outputDirectory + "/" + i + "/" + k + "/" + j

            path = Path(destination)
            path.mkdir(parents=True, exist_ok=True)

            shutil.copy2(sourceFile, destinationFile)

            shapeFile = shapeFileDirectory + "/" + k +"/" + k+".shp"

            img,metha = prepareImageGPD(shapeFile, sourceFile)

            print(i,j," with ", k," Prepared")

            # Overwrite the destination file created before with the cropped image
            with rasterio.open(destinationFile, "w", **metha) as dest:
                dest.write(img)
