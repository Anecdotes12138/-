#!/usr/bin/python
# -*- coding: utf-8 -*-
#将数据处理的结果转化为矩阵模块，得到所有用户形成的相遇关系网络
import os
import csv
import datetime
from numpy import genfromtxt,zeros
from pylab import plot,show
from math import radians, cos, sin, asin, sqrt
import types

def toAdj(path,i):
    with open(path, "r") as f:
        lines = f.readlines()
        # print(lines)
        j = 0
        while(j<=i):
            a.append(0)
            j = j+1
        for line in lines:
            if line!='\r\n':
                a.append(1)
                continue
            a.append(0)

Path = 'E:\\Geolife\\Geolife Trajectories 1.3\\Data'
#path是Geolife数据的用户文件夹（如000，001，002……）所在的路径
files = os.listdir(Path)
ii = 0
A = []
for file in files:
    a = []
    gn=[]
    path = Path+'\\'+file+'\\'+'meet.csv'
    toAdj(path,ii)
    A.append(a)
    ii = ii + 1

ii = 0
temp = 0
while(ii<len(A[0])):
    jj = ii + 1
    while(jj<len(A)):
        A[jj][ii] = A[ii][jj]
        jj = jj+1
    ii = ii +1

ii = 0
GN= []

while(ii<len(A[0])):
    jj = ii + 1
    while(jj<len(A)):
        if A[ii][jj]==1:
            gnn = []
            gnn.append(ii+1)
            gnn.append(jj+1)
            GN.append(gnn)
        jj = jj + 1
    ii = ii + 1

ii = 1
while(ii<183):
    gnn = []
    gnn.append(ii)
    gnn.append(ii)
    GN.append(gnn)
    ii = ii + 1

with open("E:\\Geolife\\Geolife Trajectories 1.3"+'\\meetforGN.csv', "wb") as f:
    c_write = csv.writer(f, dialect='excel')
    for gnn in GN:
        c_write.writerow(gnn)

with open("E:\\Geolife\\Geolife Trajectories 1.3"+'\\meet.csv', "wb") as f:
    c_write = csv.writer(f, dialect='excel')
    for al in A:
        c_write.writerow(al)

with open("E:\\Geolife\\Geolife Trajectories 1.3"+'\\meet.csv', "r") as f:
    lines = f.readlines()

with open("E:\\Geolife\\Geolife Trajectories 1.3"+'\\meet.dat', "w") as f:
    for line in lines:
        new_line = line.replace(',',' ')
        f.write(new_line)