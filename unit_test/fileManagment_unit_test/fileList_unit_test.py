from fileManagment_utils import *

path = "E:/LGO/ressource"

parent = fileList(path)

child = {}

for i in parent:
    d = {i: fileList(path + "/" + i)}
    child.update(d)