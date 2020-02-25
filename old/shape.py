import numpy as np
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
import math as math
from  itertools import combinations

class Block:
    def __init__(self, blockid, dmg, x, y, z):
        self.id = blockid
        self.dmg = dmg
        self.x = x
        self.y = y
        self.z = z
        self.used = False
        self.rx = x
        self.ry = y
        self.rz = z

    def __float__(self):
        return float(self.id + float(self.dmg)/100)
    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(float(self.id + float(self.dmg) / 100))
        #return '('+str(self.id)+', '+str(self.dmg)+') at ('+str(self.x)+', '+str(self.y)+', '+str(self.z)+')'

    def set_used(self,b):
        self.used = b

    def set_relative(self,f):
        self.rx = self.x-f[0]
        self.ry = self.y-f[1]
        self.rz = self.z-f[2]

class Shape:
    def __init__(self,b,plane):
        self.list = []
        self.plane = plane
        self.f = [b.x,b.y,b.z]
        self.append(b)

    def __iter__(self):
        for b in self.list:
            yield b

    def __eq__(self, other):
        if self.plane == other.plane and self.f == other.f and self.list == other.list:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.list)

    def __len__(self):
        return len(self.list)

    def __getitem__(self, item):
        return self.list[item]

    def copy(self):
        s = Shape(self.list[0], self.plane) #self.f
        s.list = self.list.copy()
        return s

    def extend(self,s):
        for b in s:
            self.append(b)

    def append(self,b):
        bn = (Block(b.id,b.dmg,b.x,b.y,b.z))
        bn.set_relative(self.f)
        #b.set_relative(self.f)
        self.list.append(bn) #(Block(b.id,b.dmg,b.x,b.y,b.z))

    def get_relative(self,item):
        #b = self.list[item]
        b = item
        print("RELATIVE")
        print('(' + str(self.f[0]) + ', ' + str(self.f[1]) + ', ' + str(self.f[2]) + ')')
        print('(' + str(b.x) + ', ' + str(b.y) + ', ' + str(b.z) + ')')
        return Block(b.id, b.dmg, b.x - self.f[0], b.y - self.f[1], b.z - self.f[2])

    def remove(self,s):
        self.list.remove(s)


def add_block(nb,prob,blockid,dmg):
    for b in prob:
        if b[0] == blockid and b[3] == dmg:
            b[1] = b[1]+1.0
            b[2] = b[1]/nb
            return
    prob.append([blockid,1.0,1.0/nb,dmg])

#HILL CLIMBING ALGO...

#extends a shape
def extend_shape(s,plane):
    dx, dy, dzx, dzy = 0, 0, 0, 0
    #we have xy, xz and zy planes
    if plane == 'xy':
        dx = 1
        dy = 1
    if plane == 'xz':
        dx = 1
        dzy = 1
    if plane == 'zy':
        dzx = 1
        dy = 1
    p = check_pos(m,b.x + dx,b.y,b.z + dzx)
    if p.id != 0:
        s, m = match_rect(p,m,plane)
        shape.extend(s)

    p = check_pos(m,b.x - dx,b.y,b.z - dzx)
    if p.id != 0:
        s, m = match_rect(p,m,plane)
        shape.extend(s)

    p = check_pos(m,b.x,b.y + dy,b.z + dzy)
    if p.id != 0:
        s, m = match_rect(p,m,plane)
        shape.extend(s)

    p = check_pos(m,b.x,b.y - dy,b.z - dzy)
    if p.id != 0:
        s, m = match_rect(p,m,plane)
        shape.extend(s)
    return s

#Returns the best possible merge for a set of shapes
def best_merge(shapes):
    saved_cost = 0
    best = []
    for s1 in shapes:
        for s2 in shapes:
            print("BEST  MERGE")
            print(shapes)
            print(s1)
            print(s2)
            print(s1.__ne__(s2))
            if s1.__ne__(s2):
                s = merge_shape(s1,s2)
                if not is_rect(s):
                    continue
                #print(s)
                saved = shape_cost(s1) + shape_cost(s2) - shape_cost(s)
                if saved > saved_cost:
                    saved_cost = saved
                    best = [s1,s2,s]
                else:
                    print("NOT BETTER")
            else:
                print("NOT EQUAL")
    if len(best) == 0:
        print("NO BETTER MERGE")
        return shapes
    print("appendshit")
    shapes.append(s)
    print(shapes)
    print(best[0])
    shapes.remove(best[0])
    print(shapes)
    print(best[1])
    shapes.remove(best[1])
    print(shapes)
    print("endappendshit")
    return shapes

#merges two shapes into one
def merge_shape(s1,s2):
    m = s1.copy()
    m.extend(s2)
    #if is_rect(m):
    #    return m
    return m

# Returns the best possible split for a set of shapes
def best_split(shapes):
    saved_cost = 0
    best = []
    for s in shapes:
        split = split_shape(s)
        if(s.__eq__(split[0]) and s.__eq__(split[1])):
            continue
        if shape_cost(s) - (shape_cost(split[0]) + shape_cost(split[1])) > saved_cost:
            saved_cost = shape_cost(s) - (shape_cost(split[0]) + shape_cost(split[1]))
            best = [s,split[0],split[1]]
    if len(best) == 0:
        return shapes
    print("SPLIT THESE")
    print(s)
    print(split[0])
    print(split[1])
    shapes.remove(s)
    shapes.append(split[0])
    shapes.append(split[1])
    return shapes

#splits a shape into two shapes - find the best split according to the minimal cost of the shapes
def split_shape(s):
    #r = find_rect(s)
    subshapes = sub_shapes(s)
    print(subshapes)
    possible_splits = []
    for sub in subshapes:
        print("SUB")
        print(sub)
        if is_rect(sub[0]) and is_rect(sub[1]):
            possible_splits.append(sub)
    print("POSSIBLE")
    print(possible_splits)
    print(s)
    best = [s,s]
    cost = shape_cost(best[0])
    print("COST")
    print(cost)
    for i in range(0,len(possible_splits)):
        print("COSTif")
        print(shape_cost(possible_splits[i][0]) + shape_cost(possible_splits[i][1]))
        if shape_cost(possible_splits[i][0]) + shape_cost(possible_splits[i][1]) < cost:
            best = possible_splits[i]
            cost = shape_cost(best[0]) + shape_cost(best[1])
    return best

#finds the sub_shape combinations for a certain shape
def sub_shapes(s):
    subshapes = []
    sub = []
    for i in range(1,len(s)):
        comb = combinations(s,i)
        for c in comb:
            print(c)
            if len(c) == 1:
                sub.append([c[0]])
            else:
                l = []
                for e in c:
                    l.append(e)
                sub.append(l)
    for i in range(0,len(sub)):
        subs = Shape(sub[i][0], s.plane)
        subs.extend(sub[i][1:])
        sob = [a for a in s if a not in sub[i]]
        sobs = Shape(sob[0], s.plane)
        sobs.extend(sob[1:])
        subsob = [subs, sobs]
        subshapes.append(subsob)
    return subshapes

#returns true if a shape is a rectangle
def is_rect(s):
    r = find_rect(s)
    if len(r) == 1:
        if abs(1 + r[0][2] - r[0][0]) * abs(1 + r[0][3] - r[0][1]) == len(s):
            return True
    return False

#find the shape rectangles
def find_rect(s):
    test = np.zeros((2*len(s)+1,2*len(s)+1))

    if s.plane == 'xy':
        for b in s:
            #print(str(b.x) + ', ' + str(b.y) + ', ' + str(b.z))
            #print(str(b.rx) + ', ' + str(b.ry) + ', ' + str(b.rz))
            test[b.rx+len(s)][b.ry+len(s)] = 1.0
    if s.plane == 'xz':
        for b in s:
            #print(str(b.rx) + ', ' + str(b.ry) + ', ' + str(b.rz))
            test[b.rx+len(s)][b.rz+len(s)] = 1.0
    if s.plane == 'zy':
        for b in s:
            #print(str(b.rx) + ', ' + str(b.ry) + ', ' + str(b.rz))
            test[b.ry+len(s)][b.rz+len(s)] = 1.0

    print("FULL")
    print(test)
    r = get_rectangle(test)
    print("RECTANGLE FOUND")
    print(r)
    return r

#gets the rectangles of a matrix - Prabhat Jha (https://www.geeksforgeeks.org/find-rectangles-filled-0/)
def get_rectangle(s):
    out = []
    index = -1

    for i in range(0, len(s)):
        for j in range(0, len(s[0])):
            if s[i][j] == 1:
                # storing initial position
                # of rectangle
                out.append([i, j])

                # will be used for the
                # last position
                index = index + 1
                findend(i, j, s, out, index)
    return out

#get_rectangle help function - Prabhat Jha (https://www.geeksforgeeks.org/find-rectangles-filled-0/)
def findend(i, j, s, out, index):
    flagc = 0
    flagr = 0

    for m in range(i, len(s)):
        if s[m][j] == 0:
            flagr = 1  # set the flag
            break
        if s[m][j] == 2:
            pass
        for n in range(j, len(s[0])):
            if s[m][n] == 0:
                flagc = 1
                break
            s[m][n] = 2

    if flagr == 1:
        out[index].append(m - 1)
    else:
        out[index].append(m)

    if flagc == 1:
        out[index].append(n - 1)
    else:
        out[index].append(n)

def shapes_cost(shapes):
    cost = 0
    for s in shapes:
        cost = cost + shape_cost(s)
    return cost

#cost function of a shape: entropy, hamming distance and MDL
def shape_cost(s):
    return entropy(s)

#returns the entropy of a shape
def entropy(s):
    nb = len(s)
    entropy = 0
    prob = []
    # sum block types = for
    for b in s:
        add_block(nb, prob, b.id, b.dmg)
    #Probability of certain block type * log of prob
    for p in prob:
        entropy = entropy + p[2] * math.log(p[2],2)
    entropy = - entropy
    return entropy

def hamming_distance(s):
    return

#the description length cost
def dl(shapes):
    return len(shapes)

def hill_climbing(shapes):
    #find initial set of shapes - given for now

    #choose between merge\split of a shape for a better cost
    same = 0
    while(same < 5 ):
        new = choice(shapes)
        print("STEP")
        print(shapes)
        print(new)
        if shapes_cost(new) == shapes_cost(shapes):
            same = same +1
        shapes = new
    #until we reach an optima
    return shapes

def choice(shapes):
    merge = best_merge(shapes.copy())
    print("CHOICE MERGE")
    print(merge)
    print(shapes_cost(merge))
    split = best_split(shapes.copy())
    print("CHOICE SPLIT")
    print(split)
    print(shapes_cost(split))
    if shapes_cost(merge) > shapes_cost(split):
        return split
    else:
        return merge

def main():
    print("MERGE")
    s = Shape(Block(20,0,0,0,0),'xy')
    s.append(Block(20,0,1,0,0))
    s.append(Block(30,0,2,0,0))
    #s.append(Block(23,0,3,0,0))
    #s.append(Block(24,0,4,0,0))
    s2 = Shape(Block(20,0,0,1,0),'xy')
    s2.append(Block(20,0,1,1,0))
    s2.append(Block(30,0,2,1,0))
    #s2.append(Block(34,0,3,1,0))
    #s2.append(Block(35,0,4,1,0))
    shapes = [s,s2]
    #find_rect(s2)
    #m = merge_shape(s,s2)
    #print(m)
    #print("SPLIT")
    #best = split_shape(m)
    #print("BEST SPLIT")
    #print(best)
    print(hill_climbing(shapes))
    return

if __name__ == "__main__":
    main()