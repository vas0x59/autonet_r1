import json
import numpy as np
import matplotlib.pyplot as plt

#real pic
#0.29 8
#0.025 x


d = {
     "s1": [("cross5_2", 1)],
     "s2": [("cross4_2", 1.83)],
     "g1": [("g3", 0.66)],
     "g2": [("round1_2", 0.41)],
     "g3": [("g5", 0.66)],
     "g4": [("g2", 0.66)],
     "g5": [("g7", 0.66)],
     "g6": [("g4", 0.66)],
     "g7": [("park_enter", 0.6)],
     "y1": [("y3", 0.66)],
     "y2": [("cross1_5", 0.66)],
     "y3": [("y5", 0.66)],
     "y4": [("y2", 0.66)],
     "y5": [("cross2_4", 0.66)],
     "y6": [("y4", 0.66)],
     "b1": [("b3", 0.66)],
     "b2": [("round2_1", 0.5)],
     "b3": [("b5", 0.66)],
     "b4": [("b2", 0.66)],
     "b5": [("c3", 0.7)],
     "b6": [("b4", 0.66)],
     "r1": [("c4", 0.66)],
     "r2": [("r4", 0.66)],
     "r3": [("r1", 0.66)],
     "r4": [("cross1_3", 0.45)],
     "r5": [("r3", 0.66)],
     "r6": [("r8", 0.66)],
     "r7": [("cross1_1", 0.66)],
     "r8": [("c2", 0.66)],
     "r9": [("r7", 0.66)],
     "o1": [("round1_4", 0.2)],
     "o2": [("cross2_2", 0.7)],
     "o3": [("o1", 0.66)],
     "o4": [("o6", 0.66)],
     "o5": [("cross2_6", 0.7)],
     "o6": [("round2_3", 0.2)],
     "grab1": [("cross3_6", 0.7)],
     "grab2": [("c7", 1.3), ("cross5_1", 1)],
     "grab3": [("cross3_4", 0.7)],
     "grab4": [("c6", 0.7)],
     "park1": [("c1", 1.1)],
     "park2": [("c1", 0.66)],
     "park3": [("c1", 0.66)],
     "park4": [("c4", 0.7), ("b6", 1.83)],
     "c1": [("r9", 0.7), ("park3", 0.7)],
     "c2": [("g6", 1.5)],
     "c3": [("r2", 0.66)],
     "c4": [("park4", 0.7), ("b6", 2)],
     "cross1_1": [("cross1_2", 0.66), ("cross1_4", 1), ("cross1_6", 1.1)],
     "cross1_2": [("r6", 0.2)],
     "cross1_3": [("cross1_6", 0.5), ("cross1_2", 1), ("cross1_4", 0.66)],
     "cross1_4": [("r5", 0.3)],
     "cross1_5": [("cross1_2", 0.5), ("cross1_6", 0.66), ("cross1_4", 1.1)],
     "cross1_6": [("y1", 0.7)],
     "cross2_1": [("o3", 0.3)],
     "cross2_2": [("cross2_7", 1.1), ("cross2_3", 0.5), ("cross2_5", 1), ("cross2_1", 0.66)],
     "cross2_3": [("y6", 0.7)],
     "cross2_4": [("cross2_5", 0.5), ("cross2_1", 1.1), ("cross2_7", 1), ("cross2_3", 0.66)],
     "cross2_5": [("o4", 0.3)],
     "cross2_6": [("cross2_7", 0.5), ("cross2_5", 0.66), ("cross2_1", 1), ("cross2_3", 1.1)],
     "cross2_7": [("cross3_2", 0.77)],
     "cross2_8": [("cross2_1", 0.5), ("cross2_3", 1), ("cross2_5", 1.1), ("cross2_7", 0.66)],
     "round1_1": [("g1", 0.1)],
     "round1_2": [("round1_3", 1), ("round1_inner2", 0.66), ("round1_1", 0.66)],
     "round1_3": [("o2", 0.6)],
     "round1_4": [("round1_5", 0.7), ("round1_inner3", 1.2), ("round1_3", 0.66)],
     "round1_5": [("c8", 0.8)],
     "round1_6": [("round1_1", 1), ("round1_inner1", 0.7), ("round1_5", 0.66)],
     "round2_1": [("round2_6", 1), ("round2_2", 0.66)],
     "round2_2": [("b1", 0.2), ("round2_1", 0.66)],
     "round2_3": [("round2_2", 1), ("round2_4", 0.66)],
     "round2_4": [("o5", 0.3), ("round2_3", 0.5)],
     "round2_5": [("round2_4", 1), ("round2_4", 1), ("round2_6", 0.66)],
     "round2_6": [("s2", 0.5), ("cross4_2", 1.8), ("round2_5", 0.66)],
     "cross3_1": [("cross2_8", 0.77)],
     "cross3_2": [("cross3_3", 0.5), ("cross3_1", 0.66), ("cross3_5", 1.1)],
     "cross3_3": [("grab4", 0.7)],
     "cross3_4": [("cross3_5", 1), ("cross3_1", 1.1), ("cross3_3", 0.66)],
     "cross3_5": [("grab2", 0.7)],
     "cross3_6": [("cross3_1", 0.5), ("cross3_3", 1), ("cross3_5", 0.66)],
     "cross4_1": [("c6", 0.2), ("grab3", 1.1)],
     "cross4_2": [("c5", 0.3)],
     "c5": [("grab3", 1.1), ("cross4_1", 0.2)],
     "c6": [("round2_5", 0.8)],
     "c7": [("cross5_2", 0.2)],
     "c8": [("grab1", 0.7), ("cross5_1", 0.4)],
     "cross5_1": [("c7", "0.5"), ("c8", 0.3)],
     "cross5_2": [("s1", 0.7), ("round1_6", 2)],
     "round1_inner1": [("round1_1", 1.1), ("round1_inner4", 0.7)],
     "round1_inner2": [("round1_5", 1)],
     "round1_inner3": [("round1_inner1", 0.8)],
     "round1_inner4": [("round1_3", 0.6)],
     "park_enter": [("park1", 1.27), ("park2", 1.74), ("c1", 0.5)]
}
with open("map_full_1.json", "w") as write_file:
    json.dump(d, write_file)
