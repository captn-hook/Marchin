# shttp://paulbourke.net/geometry/polygonise/
# http://paulbourke.net/geometry/polygonise/table2.txt

import time
import json
#get json from table2.txt 14- 271
lookup = {}
text = open("table2.txt", "r")

text = text.read() 
#remove chars {}  and split by \n
text = text.replace("{", "")
text = text.replace("}", "")
text = text.replace(" ", "")
text = text.split("\n")
lookup_table = []
for i in range(14, 270):
    lookup_table.append(text[i].split(","))
print(lookup_table)