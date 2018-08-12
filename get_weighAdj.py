#!/usr/bin/python
# -*- coding: utf-8 -*-
#按照对相遇关系的要求修改rawAdj()的参数n,l
#n——相遇的次数
#l——相遇的总时长（单位：s）
import os
import csv
import datetime
from numpy import genfromtxt,zeros
from pylab import plot,show
from math import radians, cos, sin, asin, sqrt
import types
import numpy

def toAdj(Path,file,i):
    pa = Path + '\\' + file + '\\' + 'meet.csv'
    with open(pa, "r") as f:
        lines = f.readlines()

    tim = []
    tims = []
    j = 0
    while (j <= i):
        tim.append(0)
        tims.append(0)
        j = j + 1
    for line in lines:
        sum = 0
        if line != '\r\n':
            with open(Path + '\\' + file + '\\' + 'meet_w.csv', "w") as f_w:
                f_w.write(line)
            data = genfromtxt(Path + '\\' + file + '\\' + 'meet_w.csv', delimiter=',')
            if(data.shape==()):
                sum = float(data)
                tims.append(1)
            else:
                for da in data:
                    sum = sum + da
                tims.append(len(data))
            tim.append(sum)
            continue
        tim.append(0)
        tims.append(0)
    # print(lines)
    return tim,tims

def drawAdj(n=0,l=0):
    Path = 'E:\\Geolife\\Geolife Trajectories 1.3\\Data'
    # path是Geolife数据的用户文件夹（如000，001，002……）所在的路径
    files = os.listdir(Path)
    with_time = []
    with_times = []
    ii = 0
    for file in files:
        ti = []
        tis = []
        ti, tis = toAdj(Path, file,ii)
        with_time.append(ti)
        with_times.append(tis)
        ii = ii + 1

    # for w in with_time:
    #   for i in w:
    #      if type(i)==numpy.ndarray:
    #         temp = float(i)
    #        w.remove(i)
    #       w.append(temp)

    number = []
    length = []
    for w in with_times:
        number.append(set(w))
    for w in with_time:
        length.append(set(w))
    numb = []
    leng = []
    for w in number:
        numb.extend(w)
    for w in length:
        leng.extend(w)

    numb = sorted(set(numb), reverse=False)
    leng = sorted(set(leng), reverse=False)

    print(numb)
    print(leng)

    ii = 0
    temp = 0
    while (ii < len(with_time[0])):
        jj = ii + 1
        while (jj < len(with_time)):
            with_time[jj][ii] = with_time[ii][jj]
            with_times[jj][ii] = with_times[ii][jj]
            jj = jj + 1
        ii = ii + 1

    cho_tim = []
    A = []
    i = 0
    j = 0
    while(i<len(with_times[0])):
        j = i
        while(j<len(with_times)):
            cho = []
            if with_times[i][j]>n and with_time[i][j]>l:
                cho.append(i+1)
                cho.append(j+1)
                A[i][j] = 1
                A[j][i] = 1
                cho_tim.append(cho)
            else:
                A[i][j] = 0
                A[j][i] = 0
            j = j+1
        i = i + 1

    with open("E:\\Geolife\\Geolife Trajectories 1.3" + '\\meetforGN.csv', "w") as f:
        c_write = csv.writer(f, dialect='excel')
        for ch in cho_tim:
            c_write.writerow(ch)

    with open("E:\\Geolife\\Geolife Trajectories 1.3" + '\\meet.csv', "wb") as f:
        c_write = csv.writer(f, dialect='excel')
        for al in A:
            c_write.writerow(al)

    with open("E:\\Geolife\\Geolife Trajectories 1.3" + '\\meet.csv', "r") as f:
        lines = f.readlines()

    with open("E:\\Geolife\\Geolife Trajectories 1.3" + '\\meet.dat', "w") as f:
        for line in lines:
            new_line = line.replace(',', ' ')
            f.write(new_line)

drawAdj(10,3600)

