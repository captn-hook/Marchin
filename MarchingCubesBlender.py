#import bpy
import time
import json
#get json from table2.txt 14- 271
lookup = {}
text = open("table2.txt", "r")
text = text[14:271]
lookup = json.loads(text)

print(lookup)

# Marching Squares Table
WAIT = .3

C = bpy.context
S = C.scene
D = bpy.data

def corner_table():
    table = {}
    for i in range(16):
        cs =[int(x) for x in bin(i)[2:].zfill(4)]
        #cs to tuple to make it hashable
        corners = tuple(cs)
        table[i] = corners
    return table

table = corner_table()

def obj_cr(verts, faces, name, orientation = 0):
    mesh = D.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    
    obj = D.objects.new(name, mesh)
    obj.rotation_mode = 'XYZ'
    obj.rotation_euler[2] = orientation * 1.5708

    return obj

def plane_mesh():
    verts = [(-1,-1,0), (1,-1,0), (1,1,0), (-1,1,0)]
    faces = [(0,1,2,3)]

    return obj_cr(verts, faces, "plane")

def half_plane(orientation = 0):
    verts = [(-1,-1,0), (1,-1,0), (1,0,0), (-1,0,0)]
    faces = [(0,1,2,3)]
    return obj_cr(verts, faces, "half_plane", orientation)


def triangle_mesh(orientation = 0):
    verts = [(-1,-1,0), (0,-1,0), (-1,0,0)]
    faces = [(0,1,2)]
    return obj_cr(verts, faces, "triangle", orientation)

def itriangle_mesh(orientation = 0):
    verts = [(-1,-1,0), (-1,1,0), (0,1,0), (1,0,0), (1,-1,0)]
    faces = [(0,1,2,3,4)]
    return obj_cr(verts, faces, "itriangle", orientation)

def line_mesh(orientation = False):
    verts = [(-1, -1, 0), (0,-1,0), (1,0,0), (1,1,0), (0,1,0), (-1,0,0)]
    faces = [(0,1,2,3,4,5)]

    if orientation:
        orientation = 1
    else:
        orientation = 0

    return obj_cr(verts, faces, "line", orientation)

#empty the scene
for obj in D.objects:
    D.objects.remove(obj)

out_table = {}

for i in table:
    v = table[i]
    value = v[0] + v[1] + v[2] + v[3]
    #if full case, where all corners are on or off
    if value == 4:
        out_table[table[i]] = plane_mesh()
    elif value == 0:
        out_table[table[i]] = None
    #if half case, where two adjacent corners are on and the other two are off
    elif value == 2 and (v[0] != v[3] and v[1] != v[2]):
        if v[0] == 1 and v[1] == 1:
            #top half
            out_table[table[i]] = half_plane(0)
        elif v[1] == 1 and v[3] == 1:
            #right half
            out_table[table[i]] = half_plane(1)
        elif v[2] == 1 and v[3] == 1:
            #bottom half
            out_table[table[i]] = half_plane(2)
        elif v[0] == 1 and v[2] == 1:
            #left half
            out_table[table[i]] = half_plane(3)
        else:
            print("half error")
    #place empty corner
    elif value == 3:
        if v[0]  == 0:
            #top left empty
            out_table[table[i]] = itriangle_mesh(2)
        elif v[1] == 0:
            #top right empty
            out_table[table[i]] = itriangle_mesh(3)
        elif v[2] == 0:
            #bottom left empty
            out_table[table[i]] = itriangle_mesh(1)
        elif v[3] == 0:
            #bottom right empty
            out_table[table[i]] = itriangle_mesh(0)
        else:
            print("empty error")
    #place corner
    elif value == 1:
        if v[0]  == 1:
            #top left
            out_table[table[i]] = triangle_mesh(0)
        elif v[1] == 1:
            #top right
            out_table[table[i]] = triangle_mesh(1)
        elif v[2] == 1:
            #bottom left
            out_table[table[i]] = triangle_mesh(3)
        elif v[3] == 1:
            #bottom right
            out_table[table[i]] = triangle_mesh(2)
        else:
            print("full error")
    else:
        if v[0] == 1 and v[3] == 1:
            #top left bottom right
            out_table[table[i]] = line_mesh(False)
        elif v[1] == 1 and v[2] == 1:
            #top right and bottom left
            out_table[table[i]] = line_mesh(True)
        else:
            print("apposing error")

s1 = [
    [0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0],
]

s2 = [
    [0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 0, 1, 1, 0, 0],
    [0, 1, 1, 0, 0, 0, 1, 1, 0],
    [1, 1, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 0, 0, 0, 1, 1],
    [0, 1, 1, 0, 0, 0, 1, 1, 0],
    [0, 0, 1, 1, 0, 1, 1, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0],
]

s3 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]

s = [s1, s2, s3]

def march_result(x, y, thing):
    tl = thing[y][x]
    tr = thing[y][x+1]
    bl = thing[y+1][x]
    br = thing[y+1][x+1]
    return (tl, tr, bl, br)

location_offset = (0, 0)

for sample in s:
    for row in sample:
        for cell in row:
            if cell == 1:
                print("#", end="")
            else:
                print(" ", end="")
        print()
    print()
    qrtr_list = []
    #march through the sample
    for y in range(len(sample) - 1):
        ls = []
        for x in range(len(sample[y]) - 1):
            ls.append(march_result(x, y, sample))
        qrtr_list.append(ls)
    
    for y in range(len(qrtr_list)):
        for x in range(len(qrtr_list[y])):
            #copy mesh, set location, and link to scene
            cp = out_table[qrtr_list[y][x]]

            if cp == None:
                continue
            else:
                #wait for time
                if WAIT > 0:
                    #force blender to update
                    C.view_layer.update()
                    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
                    time.sleep(WAIT)


            objec = cp.copy()
            objec.data = cp.data.copy()

            objec.location = (x * 2 + location_offset[0], y * 2 + location_offset[1], 0)

            C.collection.objects.link(objec)
            objec.select_set(True)
            C.view_layer.objects.active = objec
    print(x, y)
    location_offset = (location_offset[0]+x*2+3, location_offset[1]+y*2+3)