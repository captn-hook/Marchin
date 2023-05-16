#import bpy

# Marching Squares Table
AP_CD = False
CUT = False

print_table = {}

def corner_table():
    table = {}
    for i in range(16):
        cs =[int(x) for x in bin(i)[2:].zfill(4)]
        #cs to tuple to make it hashable
        corners = tuple(cs)
        table[i] = corners
    return table

table = corner_table()

def fill(x = 1):
    if x == 1:
        return r"###:###:###"
    else:
        return r"   :   :   "
    
def half(x = 0):
    #top
    if x == 0:
        return r"###:---:   "
    #right
    elif x == 1:
        return r" |#: |#: |#"
    #bottom
    elif x == 2:
        return r"   :---:###"
    #left
    else:
        return r"#| :#| :#| "
    
def icorner(x = 0):
    if x == 0:
        return r" /#:/##:###"
    #top right
    elif x == 1:
        return r"#\ :##\:###"
    #bottom left
    elif x == 2:
        return r"###:\##: \#"
    #bottom right
    else:
        return r"###:##/:#/ "

def corner(x = 0):
    if x  == 0:
        return r"/  :   :   "
    #top right
    elif x == 1:
        return r"  \:   :   "
    #bottom left
    elif x == 2:
        return r"   :   :\  "
    #bottom right
    else:
        return r"   :   :  /"
    
def acorner(x = False):
    if x:
        return r"#\ :\#\: \#"
    else:
        return r" /#:/#/:#/ "
 
for i in table:
    v = table[i]
    value = v[0] + v[1] + v[2] + v[3]
    #if full case, where all corners are on or off
    if value == 4:
        print_table[table[i]] = fill()
    elif value == 0:
        print_table[table[i]] = fill(0)
    #if half case, where two adjacent corners are on and the other two are off
    elif value == 2 and (v[0] != v[3] and v[1] != v[2]):
        if v[0] == 1 and v[1] == 1:
            print_table[table[i]] = half(0)
        elif v[1] == 1 and v[3] == 1:
            print_table[table[i]] = half(1)
        elif v[2] == 1 and v[3] == 1:
            print_table[table[i]] = half(2)
        elif v[0] == 1 and v[2] == 1:
            print_table[table[i]] =  half(3)
        else:
            print("half error")
    #place empty corner
    elif value == 3:
        if v[0]  == 0:
            print_table[table[i]] = icorner(0)
        elif v[1] == 0:
            print_table[table[i]] = icorner(1)
        elif v[2] == 0:
            print_table[table[i]] = icorner(2)
        elif v[3] == 0:
            print_table[table[i]] = icorner(3)
        else:
            print("empty error")
    #place corner
    elif value == 1:
        if v[0]  == 1:
            print_table[table[i]] = corner(0)
        elif v[1] == 1:
            print_table[table[i]] = corner(1)
        elif v[2] == 1:
            print_table[table[i]] = corner(2)
        elif v[3] == 1:
            print_table[table[i]] = corner(3)
        else:
            print("full error")
    else:
        if v[0] == 1 and v[3] == 1:
            #top left bottom right
            print_table[table[i]] = acorner(True)
        elif v[1] == 1 and v[2] == 1:
            #top right and bottom left
            print_table[table[i]] = acorner(False)
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

    strn_list = []
    strn = ''
    for y in range(len(qrtr_list)):
        strn_row = ["", "", ""]
        for x in range(len(qrtr_list[y])):
            stn = print_table[qrtr_list[y][x]]
            stn = stn.split(":")

            for i in range(len(stn)):
                stn[i] = stn[i]
                strn_row[i] += stn[i]
                if CUT:
                    strn_row[0] += '|'
        for i in range(len(strn_row)):
            strn_row[i] += "\n"
            strn += strn_row[i]
        if CUT:
            strn += len(qrtr_list[y]) * '____'
            strn += '\n'
    print("--------------------------------------")
    print(strn)
