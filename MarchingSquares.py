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
        #top
        if v[0] == 1 and v[1] == 1:
            print_table[table[i]] = half(0)
        #right
        elif v[1] == 1 and v[3] == 1:
            print_table[table[i]] = half(1)
        #bottom
        elif v[2] == 1 and v[3] == 1:
            print_table[table[i]] = half(2)
        #left
        elif v[0] == 1 and v[2] == 1:
            print_table[table[i]] =  half(3)
        else:
            print("half error")
    #place empty corner
    elif value == 3:
        #top left
        if v[0]  == 0:
            print_table[table[i]] = icorner(0)
        #top right
        elif v[1] == 0:
            print_table[table[i]] = icorner(1)
        #bottom left
        elif v[2] == 0:
            print_table[table[i]] = icorner(2)
        #bottom right
        elif v[3] == 0:
            print_table[table[i]] = icorner(3)
        else:
            print("empty error")
    #place corner
    elif value == 1:
    
        if v[0]  == 1:
            print_table[table[i]] = r"/  :   :   "
        #top right
        elif v[1] == 1:
            print_table[table[i]] = r"  \:   :   "
        #bottom left
        elif v[2] == 1:
            print_table[table[i]] = r"   :   :\  "
        #bottom right
        elif v[3] == 1:
            print_table[table[i]] = r"   :   :  /"
        else:
            print("full error")
    #place apposing corners
    elif AP_CD:
        #print("APOSE")
        if v[0] == 1 and v[3] == 1:
            #top left bottom right
            print_table[table[i]] = r"#/ :/ /: /#"
        elif v[1] == 1 and v[2] == 1:
            #top right and bottom left
            print_table[table[i]] = r" \#:\ \:#\ "
        else:
            print("apposing error")
    else:
        if v[0] == 1 and v[3] == 1:
            #top left bottom right
            print_table[table[i]] = r"#\ :\#\: \#"
        elif v[1] == 1 and v[2] == 1:
            #top right and bottom left
            print_table[table[i]] = r" /#:/#/:#/ "
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

def giv_me_the_thing(x, y, thing):

    # print("--------------------------------------")
    # print('getting', x, y)
    # for yi in range(len(thing)):
    #     if yi == y:
    #         print(" " * (3 * x + 2) + "\/")
    #         print(thing[yi])
    #         print(thing[yi + 1])
    # print("--")
    tl = thing[y][x]
    tr = thing[y][x+1]
    bl = thing[y+1][x]
    br = thing[y+1][x+1]
    # print(str(tl) + str(tr) + '\n' + str(bl) + str(br))
    # print("--------------------------------------")
    return (tl, tr, bl, br)


# print("--------------------------------------")
for sample in s:

    # print("--------------------------------------")
    for row in sample:
        for cell in row:
            if cell == 1:
                print("#", end="")
            else:
                print(" ", end="")
        print()
    print()
    # print("--------------------------------------")
    qrtr_list = []
    
    for y in range(len(sample) - 1):
        ls = []
        for x in range(len(sample[y]) - 1):
            ls.append(giv_me_the_thing(x, y, sample))
        qrtr_list.append(ls)

    # for row in sample:
    #     print(row, len(row))
    # for row in qrtr_list:
    #     print(row, len(row))
        
    #print_table will return 3 lines
    #split on new line and put into 3 lines for that row
    strn_list = []
    strn = ''
    for y in range(len(qrtr_list)):
        strn_row = ["", "", ""]
        for x in range(len(qrtr_list[y])):
            stn = print_table[qrtr_list[y][x]]
            #split and remove new line
            #print(stn)
            stn = stn.split(":")
            # print(stn[0])
            # print(stn[1])
            # print(stn[2])
            # print("____")
            stn[0] = stn[0]
            stn[1] = stn[1]
            stn[2] = stn[2]
            #fix backslash by doubling
            # stn[0] = stn[0].replace('\\', "\\")
            # stn[1] = stn[1].replace('\\', "\\")
            # stn[2] = stn[2].replace('\\', "\\")
            # print(stn)
            strn_row[0] += stn[0]
            strn_row[1] += stn[1]
            strn_row[2] += stn[2]
            if CUT:
                strn_row[0] += '|'
                strn_row[1] += '|'
                strn_row[2] += '|'
        #print('---------------------')
        strn_row[0] += "\n"
        strn_row[1] += "\n"
        strn_row[2] += "\n"

        strn += strn_row[0]
        strn += strn_row[1]
        strn += strn_row[2]
        if CUT:
            strn += len(qrtr_list[y]) * '____'
            strn += '\n'
    print("--------------------------------------")
    print(strn)
    # print("--------------------------------------")
