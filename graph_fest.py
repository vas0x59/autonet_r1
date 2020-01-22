import json
import numpy as np
import matplotlib.pyplot as plt

#real pic
#0.29 8
#0.025 x


d = {"r1": [("cross2_2", 0.69)],
     "r2": [("r4", 0.83)],
     "r3": [("r1", 0.83)],
     "r4": [("corner1_1", 0.83)],
     "o1": [("corner2_2", 1.38)],
     "o2": [("o4", 0.83)],
     "o3": [("o1", 0.83)],
     "o4": [("cross2_4", 0.69)],
     "g1": [("g3", 0.83)],
     "g2": [("round1_2", 0.69)],
     "g3": [("corner1_2", 1.4)],
     "g4": [("g2", 0.83)],
     "y1": [("y3", 0.83)],
     "y2": [("cross1_4", 1)],
     "y3": [("cross2_6", 0.69)],
     "y4": [("y2", 0.83)],
     "b1": [("corner2_1", 0.83)],
     "b2": [("b4", 0.83)],
     "b3": [("b1", 0.83)],
     "b4": [("round2_1", 0.83)],
     "grab1": [("cross1_2", 1)],
     "grab2": [("round2_3", 0.5)],
     "grab3": [("round1_4", 0.5)],
     "grab4": [("cross1_6", 1)],
     "s1": [("g1", 1)],
     "s2": [("round2_1", 1)],
     "round1_1": [("g1", 1)],
     "round1_2": [("round1_3", 0.83)],
     "round1_3": [("grab1", 0.5)],
     "round1_4": [("round1_1", 1.5)],
     "round2_1": [("round2_4", 1.5)],
     "round2_2": [("b3", 0.69)],
     "round2_3": [("round2_2", 0.83)],
     "round2_4": [("grab4", 0.5)],
     "cross1_1": [("grab3", 1)],
     "cross1_2": [("cross1_3", 0.25), ("cross1_5", 0.83)],
     "cross1_3": [("y1", 1)],
     "cross1_4": [("cross1_1", 1), ("cross1_5", 0.25)],
     "cross2_1": [("r2", 0.69)],
     "cross2_2": [("cross2_5", 1)],
     "cross2_3": [("o3", 0.69)],
     "cross2_4": [("cross2_5", 0.25), ("cross2_1", 0.83)],
     "corner1_1": [("g4", 0.83)],
     "corner1_2": [("r3", 1.4)],
     "corner2_1": [("o2", 0.83)],
     "corner2_2": [("b2", 1.4)]
     }
with open("map_1.json", "w") as write_file:
    json.dump(d, write_file)
