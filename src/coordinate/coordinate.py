x = float(input())
y = float(input())
ery = 0.44
erx = 0.28
def map_to_odom(x,y):
    yo = x+ery
    xo = y-erx
    return(xo,yo)
def odom_to_map(xo,yo):
    x = yo+ery
    y = x0-erx
    return(x,y)
   
cor = map_to_odom(x,y)
print(cor)
