from math import sqrt

v = [[4,1,3,-1],[2,1,-3,4],[1,0,-2,7],[6,2,9,-5]]
def calculate_basis(v):
    value =0
    for i in v:
        value+= i*i
    return sqrt(value)

def dot_product(v1,v2):
    value =0
    for i, j in zip(v1,v2):
        value+= i*j
    return value

def plus_minus_matrix(v1,v2,sign):
    value =[]
    for i, j in zip(v1,v2):
        if sign == 1:
            value.append(i+j)
        else:
            value.append(i-j)
    return value

def time_value(v1,v2):
    value =[]
    for i in v1:
        value.append(i*v2)
    return value

def deduct_value(v1,v2):
    value =[]
    for i in v1:
        value.append(i/v2)
    return value

def Gram_schmidt(v):
    v1 = deduct_value(v[0],calculate_basis(v[0]))
    list_v = []
    list_v.append(v1)
    for i in range(1,len(v)):
        h = len(list_v)-1
        temp =v[i]
        while h>-1:
            temp_value = dot_product(v[i],list_v[h])
            temp_value = time_value(list_v[h],temp_value)
            temp = plus_minus_matrix(temp,temp_value,0)
            h-=1
        temp =deduct_value(temp,calculate_basis(temp))
        list_v.append(temp)
    return list_v

def Gausisian_lattice(v1,v2):
    while True:
        if calculate_basis(v1) > calculate_basis(v2):
            v1,v2= v2,v1
        m = round(dot_product(v1,v2)/dot_product(v1,v1))
        if m ==0:
            return v1,v2
        else:
            v2= plus_minus_matrix(v2,time_value(v1,m),0)


def Det3(v1,v2,v3):
    return v1[0]*(v2[1]*v3[2]-v2[2]*v3[1])-v1[1]*(v2[0]*v3[2]-v2[2]*v3[0])+v1[2]*(v2[0]*v3[1]-v2[1]*v3[0])

