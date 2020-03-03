import numpy as np 
import math

import json 

d = json.load(open("map_1.json"))
c = json.load(open("map_coordinates_1.json"))

def get_dist(p1, p2):
    return ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)**0.5


for i in d.keys():
    for j in d[i]:
        j[1] = get_dist(c[i], c[j[0]])
    print(d[i])

with open("map_1.json", "w") as write_file:
    json.dump(d, write_file)
