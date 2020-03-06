import json
import matplotlib.pyplot as plt
import cv2
import random
random.seed(22)


pole = cv2.imread("full_field_40.jpg")
pole = cv2.resize(pole, (0, 0), fx=0.15, fy=0.15)

d = json.load(open("map_full_1.json"))
print(d)


coordinates = {
    "s1": (0.29, 7.36),
    "s2": (7.73, 2.41),
    "g1": (0.81, 3.93),
    "g2": (1.36, 8-4.25),
    "g3": (0.81, 8-4.56),
    "g4": (1.35, 8-4.96),
    "g5": (0.81, 8-5.27),
    "g6": (1.35, 8-5.67),
    "g7": (0.81, 8-5.97),
    "y1": (4.28, 8-5.78),
    "y2": (3.76, 8-5.79),
    "y3": (4.28, 8-5.08),
    "y4": (3.75, 8-5.1),
    "y5": (4.28, 8-4,42),
    "y6": (3.75, 8-4.42),
    "b1": (6.7, 8-4.26),
    "b2": (7.23, 8-4.05),
    "b3": (6.69, 8-4.94),
    "b4": (7.23, 8-4.72),
    "b5": (6.68, 8-5.65),
    "b6": (7.22, 8-5.45),
    "r1": (6.47, 8-7.44),
    "r2": (5.86, 8-6.89),
    "r3": (5.77, 8-7.4),
    "r4": (5.16, 8-6.87),
    "r5": (5.06, 8-7.41),
    "r6": (2.84, 8-6.87),
    "r7": (2.56, 8-7.39),
    "r8": (2.15, 8-6.89),
    "r9": (1.89, 8-7.39),
    "o1": (2.35, 8-2.78),
    "o2": (2.54, 8-3.31),
    "o3": (2.99, 8-2.78),
    "o4": (5.03, 8-3.3),
    "o5": (5.5, 8-2.77),
    "o6": (5.65, 8-3.33),
    "grab1": (2.54, 8-1.14),
    "grab2": (2.51, 8-0.61),
    "grab3": (5.43, 8-0.6),
    "grab4": (5.46, 8-1.14),
    "park1": (0.27, 8-6.65),
    "park2": (0.28, 8-7.22),
    "park3": (0.28, 8-7.72),
    "park4": (7.76, 8-6.87),
    "c1": (1, 8-7.29),
    "c2": (1.46, 8-6.77),
    "c3": (6.62, 8-6.71),
    "c4": (7.11, 8-7.22),
    "cross1_1": (3.45, 8-7.4),
    "cross1_2": (3.47, 8-6.86),
    "cross1_3": (4.5, 8-6.87),
    "cross1_4": (4.5, 8-7.41),
    "cross1_5": (3.75, 8-6.58),
    "cross1_6": (4.28, 8-6.59),
    "cross2_1": (3.48, 8-2.79),
    "cross2_2": (3.48, 8-3.31),
    "cross2_3": (3.76, 8-3.58),
    "cross2_4": (4.26, 8-3.57),
    "cross2_5": (4.51, 8-3.33),
    "cross2_6": (4.54, 8-2.79),
    "cross2_7": (4.28, 8-2.53),
    "cross2_8": (3.76, 8-2.49),
    "round1_1": (0.79, 8-3.7),
    "round1_2": (1.32, 8-3.9),
    "round1_3": (2.15, 8-3.3),
    "round1_4": (2.13, 8-2.8),
    "round1_5": (1.32, 8-2.2),
    "round1_6": (0.77, 8-2.34),
    "round2_1": (7.2, 8-3.7),
    "round2_2": (6.68, 8-3.85),
    "round2_3": (5.85, 8-3.26),
    "round2_4": (5.84, 8-2.76),
    "round2_5": (6.74, 8-2.2),
    "round2_6": (7.2, 8-2.36),
    "cross3_1": (3.76, 8-1.39),
    "cross3_2": (4.28, 8-1.36),
    "cross3_3": (4.52, 8-1.12),
    "cross3_4": (4.53, 8-0.63),
    "cross3_5": (3.47, 8-0.63),
    "cross3_6": (3.47, 8-1.14),
    "cross4_1": (6.68, 8-1.02),
    "cross4_2": (7.211, 8-0.93),
    "c5": (6.96, 8-0.59),
    "c6": (6.67, 8-1.25),
    "c7": (0.83, 8-0.59),
    "c8": (1.41, 8-1.17),
    "cross5_1": (1.34, 8-0.97),
    "cross5_2": (0.82, 8-0.98)
}


font = cv2.FONT_HERSHEY_SIMPLEX
# bottomLeftCornerOfText = (10,500)
fontScale = 0.5
fontColor = (0, 0, 255)
lineType = 2



for type, coord in coordinates.items():
    x = coord[0]
    y = coord[1]
    plt.scatter(x, y)
    plt.text(x - 0.1, y + 0.1, type, fontsize=7, )
    ix = (x)*pole.shape[1]/8
    iy = pole.shape[0] - (y)*pole.shape[1]/8
    pole = cv2.circle(pole, (int(ix), int(iy)), 5, (0, 255, 0), thickness=-1)
    cv2.putText(pole, type,
                (int(ix), int(iy-5-random.random()*15)),
                font,
                fontScale,
                fontColor,
                lineType)
    l = list(d[type])
    for i in l:
        iix = (coordinates[i[0]][0])*pole.shape[1]/8
        iiy = pole.shape[0] - (coordinates[i[0]][1])*pole.shape[1]/8
        if "cross" in type and "cross" in i[0] or "round" in type and "round" in i[0]:
            cv2.arrowedLine(pole, (int(ix), int(iy)), (int(iix), int(iiy)), (0, 255, 150), thickness=2)
        else:
            cv2.arrowedLine(pole, (int(ix), int(iy)), (int(iix), int(iiy)), (0, 150, 255), thickness=2)


# plt.show()
# plt.savefig('graph.png')
cv2.imshow("pole", pole)
cv2.imwrite("pole_with_marker.jpg", pole)
cv2.waitKey(0)
with open("map_coordinates_full_1.json", "w") as write_f:
    json.dump(coordinates, write_f)
