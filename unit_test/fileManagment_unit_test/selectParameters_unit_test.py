from fileManagment_utils import *

outputDirectory = "E:/LGO/ressource/output"
shapeFileDirectory = "E:/LGO/ressource/shapeFile"

dictionary = imageDictionary(outputDirectory,shapeFileDirectory)

dateKey= dictionary.keys()

for i in dateKey:
    print(i)

date = input("choose your date : ")

shapeKey = dictionary[date].keys()

for i in shapeKey:
    print(i)

shape = input("choose your shape : ")

print(date, shape)
