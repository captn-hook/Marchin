# http://paulbourke.net/geometry/polygonise/
# http://paulbourke.net/geometry/polygonise/table2.txt

import time
import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D, art3d

GRAPH_SIZE = (20, 20, 20)
LIMIT = 15
INTERP = True

def import_table(file_name = "table2.txt"):
    #get json from table2.txt 14- 271
    lookup = {}
    text = open(file_name, "r")

    text = text.read() 
    #remove chars {}  and split by \n
    text = text.replace("{", "")
    text = text.replace("}", "")
    text = text.replace(" ", "")
    text = text.split("\n")
    lookup_table = []

    for i in range(14, 270):
        lookup_table.append(text[i].split(","))

    return lookup_table

lookup_table = import_table()

#create sample data
def sample_0(x, y, z):
    return x + y + z

def sample_1(x, y, z):
    #returns distance from origin
    return np.sqrt(x**2 + y**2 + z**2) - 1

def sample_2(x, y, z):
    #returns distance from origin, except double the z axis
    return np.sqrt(x**2 + y**2 + (z*2)**2) - 1

def sample_3(x, y, z):
    #returns a saddle
    return x**2 - y**2 - z**2

def sample_4(x, y, z):
    #returns a double saddle
    return x**2 - y**2 - z**2 - 1

def sample_5(x, y, z):
    #returns a cone
    return np.sqrt(x**2 + y**2) - z

def sample_6(x, y, z):
    #returns a double cone
    return np.sqrt(x**2 + y**2) - z - 1

def sample_7(x, y, z):
    #returns a cylinder
    return np.sqrt(x**2 + y**2) - 1

def graph_v(v):
    
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")

    #every 3 points is a face, remap to v[f]
    verts = []
    temp = []
    while len(v) > 0:
        temp.append(v.pop(0))
        
        if len(temp) >= 3:
            verts.append(temp.copy())
            temp = []
    pc = art3d.Poly3DCollection(verts, edgecolor="black")
    ax.add_collection(pc)

    plt.show()
    
def sample(s):
    values = np.zeros((GRAPH_SIZE[0] * 2, GRAPH_SIZE[1] * 2, GRAPH_SIZE[2] * 2))
    for x in range(-GRAPH_SIZE[0], GRAPH_SIZE[0]):
        for y in range(-GRAPH_SIZE[1], GRAPH_SIZE[1]):
            for z in range(-GRAPH_SIZE[2], GRAPH_SIZE[2]):
                if s(x, y, z) > LIMIT:
                    values[x][y][z] = LIMIT
                elif s(x, y, z) < -LIMIT:
                    values[x][y][z] = -LIMIT
                else:
                    values[x][y][z] = s(x, y, z)
    return values

def get_index(values, x, y, z):
    #eight bits, each bit is a corner of the cube
    #get x, y, z, and each plus 1
    #if value is greater than limit, set bit to 1
    bits = 0
    corners = [(0,0,0), (1,0,0), (1, 1, 0), (0, 1, 0),
               (0,0,1), (1,0,1), (1, 1, 1), (0, 1, 1)]
    for i in range(8):
        corners[i] = (x + corners[i][0], y + corners[i][1], z + corners[i][2])
        if values[corners[i][0]][corners[i][1]][corners[i][2]] > LIMIT / 2:
            #set bit i to 1
            bits |= 1 << i

    return bits, corners

# VERTX
# 
#      4 - - - - - 5
#     /|          /|
#    / |         / |
#   /  |        /  |
#  7 - - - - - 6   |
#  |   |       |   |
#  |   0 - - - | - 1
#  |  /        |  /
#  | /         | /
#  |/          |/
#  3 - - - - - 2

# EDGE
# 
#      + - - 4 - - +
#     /|          /|
#    7 |         5 |
#   /  8        /  9
#  + - - 6 - - +   |
#  |   |       |   |
#  |   + - - 0 | - +
# 11  /       10  /
#  | 3         | 1
#  |/          |/
#  + - - 2 - - +

def e2v(e):
    #returns the two verts that make up an edge
    if 0 <= e < 7 and e != 3:
        #edge is just e, e + 1
        return e, e + 1
    elif e == 7:
        return 4, 7
    elif e == 3:
        return 0, 3
    elif e == 8:
        return 0, 4
    elif e == 9:
        return 1, 5
    elif e == 10:
        return 2, 6
    elif e == 11:
        return 3, 7
    
def vc(v):
    #converts a vertex n to a coordinate
    if v == 0:
        return (0, 0, 0)
    elif v == 1:
        return (1, 0, 0)
    elif v == 2:
        return (1, 1, 0)
    elif v == 3:
        return (0, 1, 0)
    elif v == 4:
        return (0, 0, 1)
    elif v == 5:
        return (1, 0, 1)
    elif v == 6:
        return (1, 1, 1)
    elif v == 7:
        return (0, 1, 1)
    
def interp(p1, p2, val1 = 0, val2 = 0):
    #interpolates between two points P = P1 + (isovalue - V1) (P2 - P1) / (V2 - V1)
    diff = val2 - val1
    pos_dif = (p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])
    if diff == 0:
        #return midpoint
        return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2, (p1[2] + p2[2]) / 2)
    else:
        x = p1[0] + (LIMIT/2 - val1) * pos_dif[0] / diff
        y = p1[1] + (LIMIT/2 - val1) * pos_dif[1] / diff
        z = p1[2] + (LIMIT/2 - val1) * pos_dif[2] / diff

        return (x, y, z)

def get_vert(e, corners, values):
    v1, v2 = e2v(e)
    v1 = corners[v1]
    v2 = corners[v2]

    #two of the coords should be the same, the last should be interpolated between based on the value at each
    if INTERP:
        val1 = values[v1[0]][v1[1]][v1[2]]
        val2 = values[v2[0]][v2[1]][v2[2]]
    else:
        val1, val2 = 0, 0       
    
    return interp(v1, v2, val1, val2)

def construct_tri(values, x, y, z):
    #get edges from lookup table, SKIP -> place verts according to values
    indx, corners = get_index(values, x, y, z)
    edges = lookup_table[indx]
    edges = [int(i) for i in edges[:-1] if i != "-1"]

    if len(edges) == 0:
        return None
    
    verts = []
    #each edge has 1*3 to 4*3 values, every 3 is a face
    for i in edges:
        verts.append(get_vert(i, corners, values))
        
    return verts

def construct_mesh(values):
    verts = []
    for x in range(-GRAPH_SIZE[0] + 1, GRAPH_SIZE[0] - 1):
        for y in range(-GRAPH_SIZE[1] + 1, GRAPH_SIZE[1] - 1):
            for z in range(-GRAPH_SIZE[2] + 1, GRAPH_SIZE[2] - 1):
                v = construct_tri(values, x, y, z)
                if v != None:
                    verts.extend(v)
    return verts

def main():
    graph_v(construct_mesh(sample(sample_4)))

if __name__ == "__main__":
    main()