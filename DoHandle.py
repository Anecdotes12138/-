#!/usr/bin/python
# -*- coding: utf-8 -*-
#数据处理模块
import os
import csv
import datetime
from numpy import genfromtxt,zeros
from pylab import plot,show
from math import radians, cos, sin, asin, sqrt
import types


def delete6(path):
    with open(path, "r") as f:
        lines = f.readlines()
        # print(lines)
    with open(path, "w") as f_w:
        for line in lines:
            if "Geolife" in line \
                    or "WGS" in line \
                    or "Altitude" in line \
                    or "Reserved" in line \
                    or "Track" in line \
                    or len(line)<3:
                continue
            f_w.write(line)


def Segmentation(file,pa,path):  #将path路径下的所有文件进行分割
    All = []
    filena = file[0:8]
    reader = csv.reader(open(pa, ), delimiter=',')
    for line in list(reader):
        All.append(line)

    i = 1
    bp = []
    while (i < len(All)):
        tim = (datetime.datetime.strptime(All[i][6], '%H:%M:%S') - datetime.datetime.strptime(
            All[i - 1][6], '%H:%M:%S')).seconds
        if tim > 300:
            bp.append(i)
        i = i + 1
    print(bp)

    i = 0
    k = 0
    for b in bp:
        j = b
        f = open(path+'\\'+filena + datetime.datetime.strptime(All[i][6], '%H:%M:%S').strftime('%H%M%S') + '.csv', 'w')
        print(path+'\\'+filena + datetime.datetime.strptime(All[i][6], '%H:%M:%S').strftime('%H%M%S'))

        while (k >= i and k < j):
            f.write(All[k][0])
            f.write(',')
            f.write(All[k][1])
            f.write(',')
            f.write(All[k][2])
            f.write(',')
            f.write(All[k][3])
            f.write(',')
            f.write(All[k][4])
            f.write(',')
            f.write(All[k][5])
            f.write(',')
            f.write(All[k][6])
            f.write('\n')
            k = k + 1
        i = k



def meeting(pa1, pa2,date,number):
    dataA = genfromtxt(pa1, delimiter=',', usecols=(0, 1, 3, 4))
    dataB = genfromtxt(pa2, delimiter=',', usecols=(0, 1, 3, 4))

    timeA = []
    reader = csv.reader(open(pa1, ), delimiter=',')
    for line in list(reader):
        timeA.append(line[6])

    timeB = []
    reader = csv.reader(open(pa2, ), delimiter=',')
    for line in list(reader):
        timeB.append(line[6])

    amax = 0
    amin = 0
    bmax = 0
    bmin = 0
    if len(dataA.shape)==1:
        amax = dataA[3]
        amin = dataA[3]
    else:
        amax = max(dataA[:, 3])
        amin = min(dataA[:, 3])

    if len(dataB.shape)==1:
        bmax = dataB[3]
        bmin = dataB[3]
    else:
        bmax = max(dataB[:, 3])
        bmin = min(dataB[:, 3])

    print(amax, amin, bmax, bmin)
    print(pa1,pa2)

    mt = [[],[],[],[]]

    if amax==amin or bmax==bmin:
        if amax == amin and bmax!=bmin:
            if bmax>amax and bmin < amax:
                for j in range(len(dataB[:, 3])):
                    if dataB[j,3]> amax:
                        bx1 = dataB[j - 1, 0]
                        bx2 = dataB[j, 0]
                        by1 = dataB[j - 1, 1]
                        by2 = dataB[j, 1]
                        ax = dataA[0]
                        ay = dataA[1]
                        distance1 = haversine(bx1, by1, ax, ay)
                        distance2 = haversine(bx2, by2, ax, ay)
                        inchdis1 = abs(dataA[2] - dataB[j - 1, 2])
                        inchdis2 = abs(dataA[2] - dataB[j, 2])
                        print("the distance is %d,%d\n" % (distance1, distance2))
                        if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                            tim = (datetime.datetime.strptime(timeB[j],
                                                              '%H:%M:%S') - datetime.datetime.strptime(
                                timeB[j - 1], '%H:%M:%S')).seconds
                            print("the tim is %d\n" % (tim))
                            mt[0].append(date)
                            mt[1].append(number)
                            mt[2].append(1)
                            mt[3].append(tim)
                        break
                    if dataB[j,3]==amax:
                        bx1 = dataB[j - 1, 0]
                        bx2 = dataB[j + 1, 0]
                        by1 = dataB[j - 1, 1]
                        by2 = dataB[j + 1, 1]
                        ax = dataA[0]
                        ay = dataA[1]
                        distance1 = haversine(bx1, by1, ax, ay)
                        distance2 = haversine(bx2, by2, ax, ay)
                        inchdis1 = abs(dataA[2] - dataB[j - 1, 2])
                        inchdis2 = abs(dataA[2] - dataB[j + 1, 2])
                        print("the distance is %d,%d\n" % (distance1, distance2))
                        if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                            tim = (datetime.datetime.strptime(timeB[j + 1],
                                                              '%H:%M:%S') - datetime.datetime.strptime(
                                timeB[j - 1], '%H:%M:%S')).seconds
                            print("the tim is %d\n" % (tim))
                            mt[0].append(date)
                            mt[1].append(number)
                            mt[2].append(1)
                            mt[3].append(tim)
                        break
        if amax != amin and bmax==bmin:
            if amax>bmax and amin < bmax:
                for i in range(len(dataA[:,3])):
                    if dataA[i,3]> bmax:
                        ax1 = dataA[i - 1, 0]
                        ax2 = dataA[i, 0]
                        ay1 = dataA[i - 1, 1]
                        ay2 = dataA[i, 1]
                        bx = dataB[0]
                        by = dataB[1]
                        distance1 = haversine(ax1, ay1, bx, by)
                        distance2 = haversine(ax2, ay2, bx, by)
                        inchdis1 = abs(dataB[2] - dataA[i - 1, 2])
                        inchdis2 = abs(dataB[2] - dataA[i, 2])
                        print("the distance is %d,%d\n" % (distance1, distance2))
                        if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                            tim = (datetime.datetime.strptime(timeA[i],
                                                              '%H:%M:%S') - datetime.datetime.strptime(
                                timeA[i - 1], '%H:%M:%S')).seconds
                            print("the tim is %d\n" % (tim))
                            mt[0].append(date)
                            mt[1].append(number)
                            mt[2].append(1)
                            mt[3].append(tim)
                        break
                    if dataA[i,3]==bmax:
                        ax1 = dataA[i - 1, 0]
                        ax2 = dataA[i + 1, 0]
                        ay1 = dataA[i - 1, 1]
                        ay2 = dataA[i + 1, 1]
                        bx = dataB[0]
                        by = dataB[1]
                        distance1 = haversine(ax1, ay1, bx, by)
                        distance2 = haversine(ax2, ay2, bx, by)
                        inchdis1 = abs(dataB[2] - dataA[i - 1, 2])
                        inchdis2 = abs(dataB[2] - dataA[i + 1, 2])
                        print("the distance is %d,%d\n" % (distance1, distance2))
                        if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                            tim = (datetime.datetime.strptime(timeA[i + 1],
                                                              '%H:%M:%S') - datetime.datetime.strptime(
                                timeA[i - 1], '%H:%M:%S')).seconds
                            print("the tim is %d\n" % (tim))
                            mt[0].append(date)
                            mt[1].append(number)
                            mt[2].append(1)
                            mt[3].append(tim)
                        break
    else:
        if amax > bmax:
            if bmax > amin:
                if bmin > amin:
                    mi = 0
                    ma = 0
                    time = 0  # 相遇时间长度
                    num = 0  # 相遇次数
                    flag = 0

                    for i in range(len(dataA[:, 3])):
                        if dataA[i, 3] >= bmin:
                            mi = i
                            break
                    for i in range(len(dataA[:, 3])):
                        if dataA[i, 3] > bmax:
                            ma = i
                            break
                    i = mi
                    j = 0
                    print(pa1, pa2)
                    while (i < ma and j < len(dataB[:, 3])):
                        if i > 0 and j > 0:
                            while dataA[i, 3] < dataB[j - 1, 3]:
                                i = i + 1
                                if i >= ma:
                                    i = i - 1
                                    break
                            while dataB[j, 3] < dataA[i - 1, 3]:
                                j = j + 1
                                if j >= len(dataB[:, 3]):
                                    j = j - 1
                                    break
                            if dataA[i, 3] < dataB[j - 1, 3] or dataB[j, 3] < dataA[i - 1, 3]:
                                break
                            if dataA[i - 1, 3] == dataB[j - 1, 3] and dataA[i, 3] == dataB[j, 3]:
                                distance1 = haversine(dataA[i - 1, 0], dataA[i - 1, 1], dataB[j - 1, 0],
                                                      dataB[j - 1, 1])
                                distance2 = haversine(dataA[i, 0], dataA[i, 1], dataB[j, 0],
                                                      dataB[j, 1])
                                inchdis1 = abs(dataA[i - 1, 2] - dataB[j - 1, 2])
                                inchdis2 = abs(dataA[i, 2] - dataB[j, 2])
                                print("the distance is %d,%d\n" % (distance1, distance2))
                                if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                    tim = (datetime.datetime.strptime(timeA[i],
                                                                      '%H:%M:%S') - datetime.datetime.strptime(
                                        timeA[i - 1], '%H:%M:%S')).seconds
                                    print("the tim is %d\n" % (tim))
                                    if flag == 0:
                                        time = tim
                                        num = num + 1
                                        mt[0].append(date)
                                        mt[1].append(number)
                                        mt[2].append(num)
                                        mt[3].append(time)
                                    else:
                                        time = time + tim
                                        mt[3][num - 1] = time
                                    flag = 1
                                else:
                                    flag = 0

                            if (dataA[i - 1, 3] > dataB[j - 1, 3] and dataA[i, 3] == dataB[j, 3]):
                                bx1 = dataB[j - 1, 0]
                                bx2 = dataB[j, 0]
                                by1 = dataB[j - 1, 1]
                                by2 = dataB[j, 1]
                                ax = dataA[i - 1, 0]
                                ay = dataA[i - 1, 1]
                                distance1 = haversine(bx1, by1, ax, ay)
                                distance2 = haversine(bx2, by2, ax, ay)
                                inchdis1 = abs(dataA[i - 1, 2] - dataB[j - 1, 2])
                                inchdis2 = abs(dataA[i - 1, 2] - dataB[j, 2])
                                print("the distance is %d,%d\n" % (distance1, distance2))
                                if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                    tim = (datetime.datetime.strptime(timeB[j],
                                                                      '%H:%M:%S') - datetime.datetime.strptime(
                                        timeB[j - 1], '%H:%M:%S')).seconds
                                    print("the tim is %d\n" % (tim))
                                    if flag == 0:
                                        time = tim
                                        num = num + 1
                                        print(type(num))
                                        mt[0].append(date)
                                        mt[1].append(number)
                                        mt[2].append(num)
                                        mt[3].append(time)
                                    else:
                                        time = time + tim
                                        mt[3][num - 1] = time
                                    flag = 1
                                else:
                                    flag = 0

                            if (dataA[i - 1, 3] < dataB[j - 1, 3] and dataA[i, 3] == dataB[j, 3]):
                                ax1 = dataA[i - 1, 0]
                                ax2 = dataA[i, 0]
                                ay1 = dataA[i - 1, 1]
                                ay2 = dataA[i, 1]
                                bx = dataB[j - 1, 0]
                                by = dataB[j - 1, 1]
                                distance1 = haversine(ax1, ay1, bx, by)
                                distance2 = haversine(ax2, ay2, bx, by)
                                inchdis1 = abs(dataB[j - 1, 2] - dataA[i - 1, 2])
                                inchdis2 = abs(dataB[j - 1, 2] - dataA[i, 2])
                                print("the distance is %d,%d\n" % (distance1, distance2))
                                if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                    tim = (datetime.datetime.strptime(timeA[i],
                                                                      '%H:%M:%S') - datetime.datetime.strptime(
                                        timeA[i - 1], '%H:%M:%S')).seconds
                                    print("the tim is %d\n" % (tim))
                                    if flag == 0:
                                        time = tim
                                        num = num + 1
                                        print(type(num))
                                        mt[0].append(date)
                                        mt[1].append(number)
                                        mt[2].append(num)
                                        mt[3].append(time)
                                    else:
                                        time = time + tim
                                        mt[3][num - 1] = time
                                    flag = 1
                                else:
                                    flag = 0

                            if dataA[i, 3] < dataB[j, 3]:
                                bx1 = dataB[j - 1, 0]
                                bx2 = dataB[j, 0]
                                by1 = dataB[j - 1, 1]
                                by2 = dataB[j, 1]
                                ax = dataA[i, 0]
                                ay = dataA[i, 1]
                                distance1 = haversine(bx1, by1, ax, ay)
                                distance2 = haversine(bx2, by2, ax, ay)
                                inchdis1 = abs(dataA[i, 2] - dataB[j - 1, 2])
                                inchdis2 = abs(dataA[i, 2] - dataB[j, 2])
                                print("the distance is %d,%d\n" % (distance1, distance2))
                                if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                    tim = (datetime.datetime.strptime(timeB[j],
                                                                      '%H:%M:%S') - datetime.datetime.strptime(
                                        timeB[j - 1], '%H:%M:%S')).seconds
                                    print("the tim is %d\n" % (tim))
                                    if flag == 0:
                                        time = tim
                                        num = num + 1
                                        print(type(num))
                                        mt[0].append(date)
                                        mt[1].append(number)
                                        mt[2].append(num)
                                        mt[3].append(time)
                                    else:
                                        time = time + tim
                                        mt[3][num - 1] = time
                                    flag = 1
                                else:
                                    flag = 0

                            if dataA[i, 3] > dataB[j, 3]:
                                ax1 = dataA[i - 1, 0]
                                ax2 = dataA[i, 0]
                                ay1 = dataA[i - 1, 1]
                                ay2 = dataA[i, 1]
                                bx = dataB[j, 0]
                                by = dataB[j, 1]
                                distance1 = haversine(ax1, ay1, bx, by)
                                distance2 = haversine(ax2, ay2, bx, by)
                                inchdis1 = abs(dataB[j, 2] - dataA[i - 1, 2])
                                inchdis2 = abs(dataB[j, 2] - dataA[i, 2])
                                print("the distance is %d,%d\n" % (distance1, distance2))
                                if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                    tim = (datetime.datetime.strptime(timeA[i],
                                                                      '%H:%M:%S') - datetime.datetime.strptime(
                                        timeA[i - 1], '%H:%M:%S')).seconds
                                    print("the tim is %d\n" % (tim))
                                    if flag == 0:
                                        time = tim
                                        num = num + 1
                                        print(type(num))
                                        mt[0].append(date)
                                        mt[1].append(number)
                                        mt[2].append(num)
                                        mt[3].append(time)
                                    else:
                                        time = time + tim
                                        mt[3][num - 1] = time
                                    flag = 1
                                else:
                                    flag = 0
                        else:
                            if dataA[i, 3] > dataB[j, 3]:
                                ax1 = dataA[i - 1, 0]
                                ax2 = dataA[i, 0]
                                ay1 = dataA[i - 1, 1]
                                ay2 = dataA[i, 1]
                                bx = dataB[j, 0]
                                by = dataB[j, 1]
                                distance1 = haversine(ax1, ay1, bx, by)
                                distance2 = haversine(ax2, ay2, bx, by)
                                inchdis1 = abs(dataB[j, 2] - dataA[i - 1, 2])
                                inchdis2 = abs(dataB[j, 2] - dataA[i, 2])
                                print("the distance is %d,%d\n" % (distance1, distance2))
                                if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                    tim = (datetime.datetime.strptime(timeA[i],
                                                                      '%H:%M:%S') - datetime.datetime.strptime(
                                        timeA[i - 1], '%H:%M:%S')).seconds
                                    print("the tim is %d\n" % (tim))
                                    if flag == 0:
                                        time = tim
                                        num = num + 1
                                        print(type(num))
                                        mt[0].append(date)
                                        mt[1].append(number)
                                        mt[2].append(num)
                                        mt[3].append(time)
                                    else:
                                        time = time + tim
                                        mt[3][num - 1] = time
                                    flag = 1
                                else:
                                    flag = 0
                        print("%d,%d--the time and num are %d,%d\n" % (i, j, time, num))
                        i = i + 1
                        j = j + 1
                else:
                    if bmin == amin:
                        mi = 0
                        ma = 0
                        time = 0  # 相遇时间长度
                        num = 0  # 相遇次数
                        flag = 0
                        for i in range(len(dataA[:, 3])):
                            if dataA[i, 3] > bmax:
                                ma = i
                                break
                        i = 0
                        j = 0
                        print(pa1, pa2)
                        while (i < ma) and j < len(dataB[:, 3]):
                            if i > 0 and j > 0:
                                while dataA[i, 3] < dataB[j - 1, 3]:
                                    i = i + 1
                                    if i >= ma:
                                        i = i - 1
                                        break
                                while dataB[j, 3] < dataA[i - 1, 3]:
                                    j = j + 1
                                    if j >= len(dataB[:, 3]):
                                        j = j - 1
                                        break
                                if dataA[i, 3] < dataB[j - 1, 3] or dataB[j, 3] < dataA[i - 1, 3]:
                                    break
                                if dataA[i - 1, 3] == dataB[j - 1, 3] and dataA[i, 3] == dataB[j, 3]:
                                    distance1 = haversine(dataA[i - 1, 0], dataA[i - 1, 1], dataB[j - 1, 0],
                                                          dataB[j - 1, 1])
                                    distance2 = haversine(dataA[i, 0], dataA[i, 1], dataB[j, 0],
                                                          dataB[j, 1])
                                    inchdis1 = abs(dataA[i - 1, 2] - dataB[j - 1, 2])
                                    inchdis2 = abs(dataA[i, 2] - dataB[j, 2])
                                    print("the distance is %d,%d\n" % (distance1, distance2))
                                    if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                        tim = (datetime.datetime.strptime(timeA[i],
                                                                          '%H:%M:%S') - datetime.datetime.strptime(
                                            timeA[i - 1], '%H:%M:%S')).seconds
                                        print("the tim is %d\n" % (tim))
                                        if flag == 0:
                                            time = tim
                                            num = num + 1
                                            print(type(num))
                                            mt[0].append(date)
                                            mt[1].append(number)
                                            mt[2].append(num)
                                            mt[3].append(time)
                                        else:
                                            time = time + tim
                                            mt[3][num - 1] = time
                                        flag = 1
                                    else:
                                        flag = 0

                                if (dataA[i - 1, 3] > dataB[j - 1, 3] and dataA[i, 3] == dataB[j, 3]):
                                    bx1 = dataB[j - 1, 0]
                                    bx2 = dataB[j, 0]
                                    by1 = dataB[j - 1, 1]
                                    by2 = dataB[j, 1]
                                    ax = dataA[i - 1, 0]
                                    ay = dataA[i - 1, 1]
                                    distance1 = haversine(bx1, by1, ax, ay)
                                    distance2 = haversine(bx2, by2, ax, ay)
                                    inchdis1 = abs(dataA[i - 1, 2] - dataB[j - 1, 2])
                                    inchdis2 = abs(dataA[i - 1, 2] - dataB[j, 2])
                                    print("the distance is %d,%d\n" % (distance1, distance2))
                                    if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                        tim = (datetime.datetime.strptime(timeB[j],
                                                                          '%H:%M:%S') - datetime.datetime.strptime(
                                            timeB[j - 1], '%H:%M:%S')).seconds
                                        print("the tim is %d\n" % (tim))
                                        if flag == 0:
                                            time = tim
                                            num = num + 1
                                            print(type(num))
                                            mt[0].append(date)
                                            mt[1].append(number)
                                            mt[2].append(num)
                                            mt[3].append(time)
                                        else:
                                            time = time + tim
                                            mt[3][num - 1] = time
                                        flag = 1
                                    else:
                                        flag = 0

                                if (dataA[i - 1, 3] < dataB[j - 1, 3] and dataA[i, 3] == dataB[j, 3]):
                                    ax1 = dataA[i - 1, 0]
                                    ax2 = dataA[i, 0]
                                    ay1 = dataA[i - 1, 1]
                                    ay2 = dataA[i, 1]
                                    bx = dataB[j - 1, 0]
                                    by = dataB[j - 1, 1]
                                    distance1 = haversine(ax1, ay1, bx, by)
                                    distance2 = haversine(ax2, ay2, bx, by)
                                    inchdis1 = abs(dataB[j - 1, 2] - dataA[i - 1, 2])
                                    inchdis2 = abs(dataB[j - 1, 2] - dataA[i, 2])
                                    print("the distance is %d,%d\n" % (distance1, distance2))
                                    if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                        tim = (datetime.datetime.strptime(timeA[i],
                                                                          '%H:%M:%S') - datetime.datetime.strptime(
                                            timeA[i - 1], '%H:%M:%S')).seconds
                                        print("the tim is %d\n" % (tim))
                                        if flag == 0:
                                            time = tim
                                            num = num + 1
                                            print(type(num))
                                            mt[0].append(date)
                                            mt[1].append(number)
                                            mt[2].append(num)
                                            mt[3].append(time)
                                        else:
                                            time = time + tim
                                            mt[3][num - 1] = time
                                        flag = 1
                                    else:
                                        flag = 0

                                if dataA[i, 3] < dataB[j, 3]:
                                    bx1 = dataB[j - 1, 0]
                                    bx2 = dataB[j, 0]
                                    by1 = dataB[j - 1, 1]
                                    by2 = dataB[j, 1]
                                    ax = dataA[i, 0]
                                    ay = dataA[i, 1]
                                    distance1 = haversine(bx1, by1, ax, ay)
                                    distance2 = haversine(bx2, by2, ax, ay)
                                    inchdis1 = abs(dataA[i, 2] - dataB[j - 1, 2])
                                    inchdis2 = abs(dataA[i, 2] - dataB[j, 2])
                                    print("the distance is %d,%d\n" % (distance1, distance2))
                                    if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                        tim = (datetime.datetime.strptime(timeB[j],
                                                                          '%H:%M:%S') - datetime.datetime.strptime(
                                            timeB[j - 1], '%H:%M:%S')).seconds
                                        print("the tim is %d\n" % (tim))
                                        if flag == 0:
                                            time = tim
                                            num = num + 1
                                            print(type(num))
                                            mt[0].append(date)
                                            mt[1].append(number)
                                            mt[2].append(num)
                                            mt[3].append(time)
                                        else:
                                            time = time + tim
                                            mt[3][num - 1] = time
                                        flag = 1
                                    else:
                                        flag = 0

                                if dataA[i, 3] > dataB[j, 3]:
                                    ax1 = dataA[i - 1, 0]
                                    ax2 = dataA[i, 0]
                                    ay1 = dataA[i - 1, 1]
                                    ay2 = dataA[i, 1]
                                    bx = dataB[j, 0]
                                    by = dataB[j, 1]
                                    distance1 = haversine(ax1, ay1, bx, by)
                                    distance2 = haversine(ax2, ay2, bx, by)
                                    inchdis1 = abs(dataB[j, 2] - dataA[i - 1, 2])
                                    inchdis2 = abs(dataB[j, 2] - dataA[i, 2])
                                    print("the distance is %d,%d\n" % (distance1, distance2))
                                    if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                        tim = (datetime.datetime.strptime(timeA[i],
                                                                          '%H:%M:%S') - datetime.datetime.strptime(
                                            timeA[i - 1], '%H:%M:%S')).seconds
                                        print("the tim is %d\n" % (tim))
                                        if flag == 0:
                                            time = tim
                                            num = num + 1
                                            print(type(num))
                                            mt[0].append(date)
                                            mt[1].append(number)
                                            mt[2].append(num)
                                            mt[3].append(time)
                                        else:
                                            time = time + tim
                                            mt[3][num - 1] = time
                                        flag = 1
                                    else:
                                        flag = 0
                            print("%d,%d--the time and num are %d,%d\n" % (i, j, time, num))
                            i = i + 1
                            j = j + 1
                    else:
                        mi = 0
                        ma = 0
                        time = 0  # 相遇时间长度
                        num = 0  # 相遇次数
                        flag = 0
                        for j in range(len(dataB[:, 3])):
                            if dataB[j, 3] >= amin:
                                mi = j
                                break
                        for i in range(len(dataA[:, 3])):
                            if dataA[i, 3] > bmax:
                                ma = i
                                break
                        print(min, max)
                        j = mi
                        i = 0
                        print(pa1, pa2)
                        while (j < len(dataB[:, 3]) and i < ma):  # b集合中的序号
                            if i > 0 and j > 0:
                                while dataA[i, 3] < dataB[j - 1, 3]:
                                    i = i + 1
                                    if i >= ma:
                                        i = i - 1
                                        break
                                while dataB[j, 3] < dataA[i - 1, 3]:
                                    j = j + 1
                                    if j >= len(dataB[:, 3]):
                                        j = j - 1
                                        break
                                if dataA[i, 3] < dataB[j - 1, 3] or dataB[j, 3] < dataA[i - 1, 3]:
                                    break
                                if dataA[i - 1, 3] == dataB[j - 1, 3] and dataA[i, 3] == dataB[j, 3]:
                                    distance1 = haversine(dataA[i - 1, 0], dataA[i - 1, 1], dataB[j - 1, 0],
                                                          dataB[j - 1, 1])
                                    distance2 = haversine(dataA[i, 0], dataA[i, 1], dataB[j, 0],
                                                          dataB[j, 1])
                                    inchdis1 = abs(dataA[i - 1, 2] - dataB[j - 1, 2])
                                    inchdis2 = abs(dataA[i, 2] - dataB[j, 2])
                                    print("the distance is %d,%d\n" % (distance1, distance2))
                                    if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                        tim = (datetime.datetime.strptime(timeA[i],
                                                                          '%H:%M:%S') - datetime.datetime.strptime(
                                            timeA[i - 1], '%H:%M:%S')).seconds
                                        print("the tim is %d\n" % (tim))
                                        if flag == 0:
                                            time = tim
                                            num = num + 1
                                            print(type(num))
                                            mt[0].append(date)
                                            mt[1].append(number)
                                            mt[2].append(num)
                                            mt[3].append(time)
                                        else:
                                            time = time + tim
                                            mt[3][num - 1] = time
                                        flag = 1
                                    else:
                                        flag = 0

                                if (dataA[i - 1, 3] > dataB[j - 1, 3] and dataA[i, 3] == dataB[j, 3]):
                                    bx1 = dataB[j - 1, 0]
                                    bx2 = dataB[j, 0]
                                    by1 = dataB[j - 1, 1]
                                    by2 = dataB[j, 1]
                                    ax = dataA[i - 1, 0]
                                    ay = dataA[i - 1, 1]
                                    distance1 = haversine(bx1, by1, ax, ay)
                                    distance2 = haversine(bx2, by2, ax, ay)
                                    inchdis1 = abs(dataA[i - 1, 2] - dataB[j - 1, 2])
                                    inchdis2 = abs(dataA[i - 1, 2] - dataB[j, 2])
                                    print("the distance is %d,%d\n" % (distance1, distance2))
                                    if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                        tim = (datetime.datetime.strptime(timeB[j],
                                                                          '%H:%M:%S') - datetime.datetime.strptime(
                                            timeB[j - 1], '%H:%M:%S')).seconds
                                        print("the tim is %d\n" % (tim))
                                        if flag == 0:
                                            time = tim
                                            num = num + 1
                                            print(type(num))
                                            mt[0].append(date)
                                            mt[1].append(number)
                                            mt[2].append(num)
                                            mt[3].append(time)
                                        else:
                                            time = time + tim
                                            mt[3][num - 1] = time
                                        flag = 1
                                    else:
                                        flag = 0

                                if (dataA[i - 1, 3] < dataB[j - 1, 3] and dataA[i, 3] == dataB[j, 3]):
                                    ax1 = dataA[i - 1, 0]
                                    ax2 = dataA[i, 0]
                                    ay1 = dataA[i - 1, 1]
                                    ay2 = dataA[i, 1]
                                    bx = dataB[j - 1, 0]
                                    by = dataB[j - 1, 1]
                                    distance1 = haversine(ax1, ay1, bx, by)
                                    distance2 = haversine(ax2, ay2, bx, by)
                                    inchdis1 = abs(dataB[j - 1, 2] - dataA[i - 1, 2])
                                    inchdis2 = abs(dataB[j - 1, 2] - dataA[i, 2])
                                    print("the distance is %d,%d\n" % (distance1, distance2))
                                    if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                        tim = (datetime.datetime.strptime(timeA[i],
                                                                          '%H:%M:%S') - datetime.datetime.strptime(
                                            timeA[i - 1], '%H:%M:%S')).seconds
                                        print("the tim is %d\n" % (tim))
                                        if flag == 0:
                                            time = tim
                                            num = num + 1
                                            print(type(num))
                                            mt[0].append(date)
                                            mt[1].append(number)
                                            mt[2].append(num)
                                            mt[3].append(time)
                                        else:
                                            time = time + tim
                                            mt[3][num - 1] = time
                                        flag = 1
                                    else:
                                        flag = 0

                                if dataA[i, 3] < dataB[j, 3]:
                                    bx1 = dataB[j - 1, 0]
                                    bx2 = dataB[j, 0]
                                    by1 = dataB[j - 1, 1]
                                    by2 = dataB[j, 1]
                                    ax = dataA[i, 0]
                                    ay = dataA[i, 1]
                                    distance1 = haversine(bx1, by1, ax, ay)
                                    distance2 = haversine(bx2, by2, ax, ay)
                                    inchdis1 = abs(dataA[i, 2] - dataB[j - 1, 2])
                                    inchdis2 = abs(dataA[i, 2] - dataB[j, 2])
                                    print("the distance is %d,%d\n" % (distance1, distance2))
                                    if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                        tim = (datetime.datetime.strptime(timeB[j],
                                                                          '%H:%M:%S') - datetime.datetime.strptime(
                                            timeB[j - 1], '%H:%M:%S')).seconds
                                        print("the tim is %d\n" % (tim))
                                        if flag == 0:
                                            time = tim
                                            num = num + 1
                                            print(type(num))
                                            mt[0].append(date)
                                            mt[1].append(number)
                                            mt[2].append(num)
                                            mt[3].append(time)
                                        else:
                                            time = time + tim
                                            mt[3][num - 1] = time
                                        flag = 1
                                    else:
                                        flag = 0

                                if dataA[i, 3] > dataB[j, 3]:
                                    ax1 = dataA[i - 1, 0]
                                    ax2 = dataA[i, 0]
                                    ay1 = dataA[i - 1, 1]
                                    ay2 = dataA[i, 1]
                                    bx = dataB[j, 0]
                                    by = dataB[j, 1]
                                    distance1 = haversine(ax1, ay1, bx, by)
                                    distance2 = haversine(ax2, ay2, bx, by)
                                    inchdis1 = abs(dataB[j, 2] - dataA[i - 1, 2])
                                    inchdis2 = abs(dataB[j, 2] - dataA[i, 2])
                                    print("the distance is %d,%d\n" % (distance1, distance2))
                                    if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                        tim = (datetime.datetime.strptime(timeA[i],
                                                                          '%H:%M:%S') - datetime.datetime.strptime(
                                            timeA[i - 1], '%H:%M:%S')).seconds
                                        print("the tim is %d\n" % (tim))
                                        if flag == 0:
                                            time = tim
                                            num = num + 1
                                            print(type(num))
                                            mt[0].append(date)
                                            mt[1].append(number)
                                            mt[2].append(num)
                                            mt[3].append(time)
                                        else:
                                            time = time + tim
                                            mt[3][num - 1] = time
                                        flag = 1
                                    else:
                                        flag = 0
                            else:
                                if dataA[i, 3] < dataB[j, 3]:
                                    bx1 = dataB[j - 1, 0]
                                    bx2 = dataB[j, 0]
                                    by1 = dataB[j - 1, 1]
                                    by2 = dataB[j, 1]
                                    ax = dataA[i, 0]
                                    ay = dataA[i, 1]
                                    distance1 = haversine(bx1, by1, ax, ay)
                                    distance2 = haversine(bx2, by2, ax, ay)
                                    inchdis1 = abs(dataA[i, 2] - dataB[j - 1, 2])
                                    inchdis2 = abs(dataA[i, 2] - dataB[j, 2])
                                    print("the distance is %d,%d\n" % (distance1, distance2))
                                    if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                        tim = (datetime.datetime.strptime(timeB[j],
                                                                          '%H:%M:%S') - datetime.datetime.strptime(
                                            timeB[j - 1], '%H:%M:%S')).seconds
                                        print("the tim is %d\n" % (tim))
                                        if flag == 0:
                                            time = tim
                                            num = num + 1
                                            print(type(num))
                                            mt[0].append(date)
                                            mt[1].append(number)
                                            mt[2].append(num)
                                            mt[3].append(time)
                                        else:
                                            time = time + tim
                                            mt[3][num - 1] = time
                                        flag = 1
                                    else:
                                        flag = 0
                            print("%d,%d--the time and num are %d,%d\n" % (i, j, time, num))
                            i = i + 1
                            j = j + 1


        else:
            if amax == bmax:
                if bmin > amin:
                    mi = 0
                    ma = 0
                    time = 0  # 相遇时间长度
                    num = 0  # 相遇次数
                    flag = 0
                    for i in range(len(dataA[:, 3])):
                        if dataA[i, 3] >= bmin:
                            mi = i
                            break
                    i = mi
                    j = 0
                    print(pa1, pa2)
                    while (i < len(dataA[:,3]) and j < len(dataB[:, 3])):
                        if i > 0 and j > 0:
                            while dataA[i, 3] < dataB[j - 1, 3]:
                                i = i + 1
                                if i >= len(dataA[:, 3]):
                                    i = i - 1
                                    break
                            while dataB[j, 3] < dataA[i - 1, 3]:
                                j = j + 1
                                if j >= len(dataB[:, 3]):
                                    j = j - 1
                                    break
                            if dataA[i, 3] < dataB[j - 1, 3] or dataB[j, 3] < dataA[i - 1, 3]:
                                break
                            if dataA[i - 1, 3] == dataB[j - 1, 3] and dataA[i, 3] == dataB[j, 3]:
                                distance1 = haversine(dataA[i - 1, 0], dataA[i - 1, 1], dataB[j - 1, 0],
                                                      dataB[j - 1, 1])
                                distance2 = haversine(dataA[i, 0], dataA[i, 1], dataB[j, 0],
                                                      dataB[j, 1])
                                inchdis1 = abs(dataA[i - 1, 2] - dataB[j - 1, 2])
                                inchdis2 = abs(dataA[i, 2] - dataB[j, 2])
                                print("the distance is %d,%d\n" % (distance1, distance2))
                                if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                    tim = (datetime.datetime.strptime(timeA[i],
                                                                      '%H:%M:%S') - datetime.datetime.strptime(
                                        timeA[i - 1], '%H:%M:%S')).seconds
                                    print("the tim is %d\n" % (tim))
                                    if flag == 0:
                                        time = tim
                                        num = num + 1
                                        print(type(num))
                                        mt[0].append(date)
                                        mt[1].append(number)
                                        mt[2].append(num)
                                        mt[3].append(time)
                                    else:
                                        time = time + tim
                                        mt[3][num - 1] = time
                                    flag = 1
                                else:
                                    flag = 0

                            if (dataA[i - 1, 3] > dataB[j - 1, 3] and dataA[i, 3] == dataB[j, 3]):
                                bx1 = dataB[j - 1, 0]
                                bx2 = dataB[j, 0]
                                by1 = dataB[j - 1, 1]
                                by2 = dataB[j, 1]
                                ax = dataA[i - 1, 0]
                                ay = dataA[i - 1, 1]
                                distance1 = haversine(bx1, by1, ax, ay)
                                distance2 = haversine(bx2, by2, ax, ay)
                                inchdis1 = abs(dataA[i - 1, 2] - dataB[j - 1, 2])
                                inchdis2 = abs(dataA[i - 1, 2] - dataB[j, 2])
                                print("the distance is %d,%d\n" % (distance1, distance2))
                                if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                    tim = (datetime.datetime.strptime(timeB[j],
                                                                      '%H:%M:%S') - datetime.datetime.strptime(
                                        timeB[j - 1], '%H:%M:%S')).seconds
                                    print("the tim is %d\n" % (tim))
                                    if flag == 0:
                                        time = tim
                                        num = num + 1
                                        print(type(num))
                                        mt[0].append(date)
                                        mt[1].append(number)
                                        mt[2].append(num)
                                        mt[3].append(time)
                                    else:
                                        time = time + tim
                                        mt[3][num - 1] = time
                                    flag = 1
                                else:
                                    flag = 0

                            if (dataA[i - 1, 3] < dataB[j - 1, 3] and dataA[i, 3] == dataB[j, 3]):
                                ax1 = dataA[i - 1, 0]
                                ax2 = dataA[i, 0]
                                ay1 = dataA[i - 1, 1]
                                ay2 = dataA[i, 1]
                                bx = dataB[j - 1, 0]
                                by = dataB[j - 1, 1]
                                distance1 = haversine(ax1, ay1, bx, by)
                                distance2 = haversine(ax2, ay2, bx, by)
                                inchdis1 = abs(dataB[j - 1, 2] - dataA[i - 1, 2])
                                inchdis2 = abs(dataB[j - 1, 2] - dataA[i, 2])
                                print("the distance is %d,%d\n" % (distance1, distance2))
                                if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                    tim = (datetime.datetime.strptime(timeA[i],
                                                                      '%H:%M:%S') - datetime.datetime.strptime(
                                        timeA[i - 1], '%H:%M:%S')).seconds
                                    print("the tim is %d\n" % (tim))
                                    if flag == 0:
                                        time = tim
                                        num = num + 1
                                        print(type(num))
                                        mt[0].append(date)
                                        mt[1].append(number)
                                        mt[2].append(num)
                                        mt[3].append(time)
                                    else:
                                        time = time + tim
                                        mt[3][num - 1] = time
                                    flag = 1
                                else:
                                    flag = 0

                            if dataA[i, 3] < dataB[j, 3]:
                                bx1 = dataB[j - 1, 0]
                                bx2 = dataB[j, 0]
                                by1 = dataB[j - 1, 1]
                                by2 = dataB[j, 1]
                                ax = dataA[i, 0]
                                ay = dataA[i, 1]
                                distance1 = haversine(bx1, by1, ax, ay)
                                distance2 = haversine(bx2, by2, ax, ay)
                                inchdis1 = abs(dataA[i, 2] - dataB[j - 1, 2])
                                inchdis2 = abs(dataA[i, 2] - dataB[j, 2])
                                print("the distance is %d,%d\n" % (distance1, distance2))
                                if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                    tim = (datetime.datetime.strptime(timeB[j],
                                                                      '%H:%M:%S') - datetime.datetime.strptime(
                                        timeB[j - 1], '%H:%M:%S')).seconds
                                    print("the tim is %d\n" % (tim))
                                    if flag == 0:
                                        time = tim
                                        num = num + 1
                                        print(type(num))
                                        mt[0].append(date)
                                        mt[1].append(number)
                                        mt[2].append(num)
                                        mt[3].append(time)
                                    else:
                                        time = time + tim
                                        mt[3][num - 1] = time
                                    flag = 1
                                else:
                                    flag = 0

                            if dataA[i, 3] > dataB[j, 3]:
                                ax1 = dataA[i - 1, 0]
                                ax2 = dataA[i, 0]
                                ay1 = dataA[i - 1, 1]
                                ay2 = dataA[i, 1]
                                bx = dataB[j, 0]
                                by = dataB[j, 1]
                                distance1 = haversine(ax1, ay1, bx, by)
                                distance2 = haversine(ax2, ay2, bx, by)
                                inchdis1 = abs(dataB[j, 2] - dataA[i - 1, 2])
                                inchdis2 = abs(dataB[j, 2] - dataA[i, 2])
                                print("the distance is %d,%d\n" % (distance1, distance2))
                                if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                    tim = (datetime.datetime.strptime(timeA[i],
                                                                      '%H:%M:%S') - datetime.datetime.strptime(
                                        timeA[i - 1], '%H:%M:%S')).seconds
                                    print("the tim is %d\n" % (tim))
                                    if flag == 0:
                                        time = tim
                                        num = num + 1
                                        print(type(num))
                                        mt[0].append(date)
                                        mt[1].append(number)
                                        mt[2].append(num)
                                        mt[3].append(time)
                                    else:
                                        time = time + tim
                                        mt[3][num - 1] = time
                                    flag = 1
                                else:
                                    flag = 0
                        else:
                            if dataA[i, 3] > dataB[j, 3]:
                                ax1 = dataA[i - 1, 0]
                                ax2 = dataA[i, 0]
                                ay1 = dataA[i - 1, 1]
                                ay2 = dataA[i, 1]
                                bx = dataB[j, 0]
                                by = dataB[j, 1]
                                distance1 = haversine(ax1, ay1, bx, by)
                                distance2 = haversine(ax2, ay2, bx, by)
                                inchdis1 = abs(dataB[j, 2] - dataA[i - 1, 2])
                                inchdis2 = abs(dataB[j, 2] - dataA[i, 2])
                                print("the distance is %d,%d\n" % (distance1, distance2))
                                if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                    tim = (datetime.datetime.strptime(timeA[i],
                                                                      '%H:%M:%S') - datetime.datetime.strptime(
                                        timeA[i - 1], '%H:%M:%S')).seconds
                                    print("the tim is %d\n" % (tim))
                                    if flag == 0:
                                        time = tim
                                        num = num + 1
                                        print(type(num))
                                        mt[0].append(date)
                                        mt[1].append(number)
                                        mt[2].append(num)
                                        mt[3].append(time)
                                    else:
                                        time = time + tim
                                        mt[3][num - 1] = time
                                    flag = 1
                                else:
                                    flag = 0
                        print("%d,%d--the time and num are %d,%d\n" % (i, j, time, num))
                        i = i + 1
                        j = j + 1
                else:
                    if bmin == amin:
                        mi = 0
                        ma = 0
                        time = 0  # 相遇时间长度
                        num = 0  # 相遇次数
                        i = 0
                        j = 0
                        flag = 0
                        print(pa1, pa2)
                        while i < len(dataA[:, 3]) and j < len(dataB[:, 3]):
                            if i > 0 and j > 0:
                                while dataA[i, 3] < dataB[j - 1, 3]:
                                    i = i + 1
                                    if i >= len(dataA[:, 3]):
                                        i = i - 1
                                        break
                                while dataB[j, 3] < dataA[i - 1, 3]:
                                    j = j + 1
                                    if j >= len(dataB[:, 3]):
                                        j = j - 1
                                        break
                                if dataA[i, 3] < dataB[j - 1, 3] or dataB[j, 3] < dataA[i - 1, 3]:
                                    break
                                if dataA[i - 1, 3] == dataB[j - 1, 3] and dataA[i, 3] == dataB[j, 3]:
                                    distance1 = haversine(dataA[i - 1, 0], dataA[i - 1, 1], dataB[j - 1, 0],
                                                          dataB[j - 1, 1])
                                    distance2 = haversine(dataA[i, 0], dataA[i, 1], dataB[j, 0],
                                                          dataB[j, 1])
                                    inchdis1 = abs(dataA[i - 1, 2] - dataB[j - 1, 2])
                                    inchdis2 = abs(dataA[i, 2] - dataB[j, 2])
                                    print("the distance is %d,%d\n" % (distance1, distance2))
                                    if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                        tim = (datetime.datetime.strptime(timeA[i],
                                                                          '%H:%M:%S') - datetime.datetime.strptime(
                                            timeA[i - 1], '%H:%M:%S')).seconds
                                        print("the tim is %d\n" % (tim))
                                        if flag == 0:
                                            time = tim
                                            num = num + 1
                                            print(type(num))
                                            mt[0].append(date)
                                            mt[1].append(number)
                                            mt[2].append(num)
                                            mt[3].append(time)
                                        else:
                                            time = time + tim
                                            mt[3][num - 1] = time
                                        flag = 1
                                    else:
                                        flag = 0

                                if (dataA[i - 1, 3] > dataB[j - 1, 3] and dataA[i, 3] == dataB[j, 3]):
                                    bx1 = dataB[j - 1, 0]
                                    bx2 = dataB[j, 0]
                                    by1 = dataB[j - 1, 1]
                                    by2 = dataB[j, 1]
                                    ax = dataA[i - 1, 0]
                                    ay = dataA[i - 1, 1]
                                    distance1 = haversine(bx1, by1, ax, ay)
                                    distance2 = haversine(bx2, by2, ax, ay)
                                    inchdis1 = abs(dataA[i - 1, 2] - dataB[j - 1, 2])
                                    inchdis2 = abs(dataA[i - 1, 2] - dataB[j, 2])
                                    print("the distance is %d,%d\n" % (distance1, distance2))
                                    if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                        tim = (datetime.datetime.strptime(timeB[j],
                                                                          '%H:%M:%S') - datetime.datetime.strptime(
                                            timeB[j - 1], '%H:%M:%S')).seconds
                                        print("the tim is %d\n" % (tim))
                                        if flag == 0:
                                            time = tim
                                            num = num + 1
                                            print(type(num))
                                            mt[0].append(date)
                                            mt[1].append(number)
                                            mt[2].append(num)
                                            mt[3].append(time)
                                        else:
                                            time = time + tim
                                            mt[3][num - 1] = time
                                        flag = 1
                                    else:
                                        flag = 0

                                if (dataA[i - 1, 3] < dataB[j - 1, 3] and dataA[i, 3] == dataB[j, 3]):
                                    ax1 = dataA[i - 1, 0]
                                    ax2 = dataA[i, 0]
                                    ay1 = dataA[i - 1, 1]
                                    ay2 = dataA[i, 1]
                                    bx = dataB[j - 1, 0]
                                    by = dataB[j - 1, 1]
                                    distance1 = haversine(ax1, ay1, bx, by)
                                    distance2 = haversine(ax2, ay2, bx, by)
                                    inchdis1 = abs(dataB[j - 1, 2] - dataA[i - 1, 2])
                                    inchdis2 = abs(dataB[j - 1, 2] - dataA[i, 2])
                                    print("the distance is %d,%d\n" % (distance1, distance2))
                                    if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                        tim = (datetime.datetime.strptime(timeA[i],
                                                                          '%H:%M:%S') - datetime.datetime.strptime(
                                            timeA[i - 1], '%H:%M:%S')).seconds
                                        print("the tim is %d\n" % (tim))
                                        if flag == 0:
                                            time = tim
                                            num = num + 1
                                            print(type(num))
                                            mt[0].append(date)
                                            mt[1].append(number)
                                            mt[2].append(num)
                                            mt[3].append(time)
                                        else:
                                            time = time + tim
                                            mt[3][num - 1] = time
                                        flag = 1
                                    else:
                                        flag = 0

                                if dataA[i, 3] < dataB[j, 3]:
                                    bx1 = dataB[j - 1, 0]
                                    bx2 = dataB[j, 0]
                                    by1 = dataB[j - 1, 1]
                                    by2 = dataB[j, 1]
                                    ax = dataA[i, 0]
                                    ay = dataA[i, 1]
                                    distance1 = haversine(bx1, by1, ax, ay)
                                    distance2 = haversine(bx2, by2, ax, ay)
                                    inchdis1 = abs(dataA[i, 2] - dataB[j - 1, 2])
                                    inchdis2 = abs(dataA[i, 2] - dataB[j, 2])
                                    print("the distance is %d,%d\n" % (distance1, distance2))
                                    if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                        tim = (datetime.datetime.strptime(timeB[j],
                                                                          '%H:%M:%S') - datetime.datetime.strptime(
                                            timeB[j - 1], '%H:%M:%S')).seconds
                                        print("the tim is %d\n" % (tim))
                                        if flag == 0:
                                            time = tim
                                            num = num + 1
                                            print(type(num))
                                            mt[0].append(date)
                                            mt[1].append(number)
                                            mt[2].append(num)
                                            mt[3].append(time)
                                        else:
                                            time = time + tim
                                            mt[3][num - 1] = time
                                        flag = 1
                                    else:
                                        flag = 0

                                if dataA[i, 3] > dataB[j, 3]:
                                    ax1 = dataA[i - 1, 0]
                                    ax2 = dataA[i, 0]
                                    ay1 = dataA[i - 1, 1]
                                    ay2 = dataA[i, 1]
                                    bx = dataB[j, 0]
                                    by = dataB[j, 1]
                                    distance1 = haversine(ax1, ay1, bx, by)
                                    distance2 = haversine(ax2, ay2, bx, by)
                                    inchdis1 = abs(dataB[j, 2] - dataA[i - 1, 2])
                                    inchdis2 = abs(dataB[j, 2] - dataA[i, 2])
                                    print("the distance is %d,%d\n" % (distance1, distance2))
                                    if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                        tim = (datetime.datetime.strptime(timeA[i],
                                                                          '%H:%M:%S') - datetime.datetime.strptime(
                                            timeA[i - 1], '%H:%M:%S')).seconds
                                        print("the tim is %d\n" % (tim))
                                        if flag == 0:
                                            time = tim
                                            num = num + 1
                                            print(type(num))
                                            mt[0].append(date)
                                            mt[1].append(number)
                                            mt[2].append(num)
                                            mt[3].append(time)
                                        else:
                                            time = time + tim
                                            mt[3][num - 1] = time
                                        flag = 1
                                    else:
                                        flag = 0
                            print("%d,%d--the time and num are %d,%d\n" % (i, j, time, num))
                            i = i + 1
                            j = j + 1
                    else:
                        mi = 0
                        ma = 0
                        time = 0  # 相遇时间长度
                        num = 0  # 相遇次数
                        flag = 0
                        for j in range(len(dataB[:, 3])):
                            if dataB[j, 3] >= amin:
                                mi = j
                                break
                        j = mi
                        i = 0
                        print(pa1, pa2)
                        while (j < len(dataB[:, 3]) and i < len(dataA[:, 3])):  # b集合中的序号
                            if i > 0:
                                while dataA[i, 3] < dataB[j - 1, 3]:
                                    i = i + 1
                                    if i >= len(dataA[:, 3]):
                                        i = i - 1
                                        break
                                while dataB[j, 3] < dataA[i - 1, 3]:
                                    j = j + 1
                                    if j >= len(dataB[:, 3]):
                                        j = j - 1
                                        break
                                if dataA[i, 3] < dataB[j - 1, 3] or dataB[j, 3] < dataA[i - 1, 3]:
                                    break
                                if dataA[i - 1, 3] == dataB[j - 1, 3] and dataA[i, 3] == dataB[j, 3]:
                                    distance1 = haversine(dataA[i - 1, 0], dataA[i - 1, 1], dataB[j - 1, 0],
                                                          dataB[j - 1, 1])
                                    distance2 = haversine(dataA[i, 0], dataA[i, 1], dataB[j, 0],
                                                          dataB[j, 1])
                                    inchdis1 = abs(dataA[i - 1, 2] - dataB[j - 1, 2])
                                    inchdis2 = abs(dataA[i, 2] - dataB[j, 2])
                                    print("the distance is %d,%d\n" % (distance1, distance2))
                                    if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                        tim = (datetime.datetime.strptime(timeA[i],
                                                                          '%H:%M:%S') - datetime.datetime.strptime(
                                            timeA[i - 1], '%H:%M:%S')).seconds
                                        print("the tim is %d\n" % (tim))
                                        if flag == 0:
                                            time = tim
                                            num = num + 1
                                            print(type(num))
                                            mt[0].append(date)
                                            mt[1].append(number)
                                            mt[2].append(num)
                                            mt[3].append(time)
                                        else:
                                            time = time + tim
                                            mt[3][num - 1] = time
                                        flag = 1
                                    else:
                                        flag = 0

                                if (dataA[i - 1, 3] > dataB[j - 1, 3] and dataA[i, 3] == dataB[j, 3]):
                                    bx1 = dataB[j - 1, 0]
                                    bx2 = dataB[j, 0]
                                    by1 = dataB[j - 1, 1]
                                    by2 = dataB[j, 1]
                                    ax = dataA[i - 1, 0]
                                    ay = dataA[i - 1, 1]
                                    distance1 = haversine(bx1, by1, ax, ay)
                                    distance2 = haversine(bx2, by2, ax, ay)
                                    inchdis1 = abs(dataA[i - 1, 2] - dataB[j - 1, 2])
                                    inchdis2 = abs(dataA[i - 1, 2] - dataB[j, 2])
                                    print("the distance is %d,%d\n" % (distance1, distance2))
                                    if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                        tim = (datetime.datetime.strptime(timeB[j],
                                                                          '%H:%M:%S') - datetime.datetime.strptime(
                                            timeB[j - 1], '%H:%M:%S')).seconds
                                        print("the tim is %d\n" % (tim))
                                        if flag == 0:
                                            time = tim
                                            num = num + 1
                                            print(type(num))
                                            mt[0].append(date)
                                            mt[1].append(number)
                                            mt[2].append(num)
                                            mt[3].append(time)
                                        else:
                                            time = time + tim
                                            mt[3][num - 1] = time
                                        flag = 1
                                    else:
                                        flag = 0

                                if (dataA[i - 1, 3] < dataB[j - 1, 3] and dataA[i, 3] == dataB[j, 3]):
                                    ax1 = dataA[i - 1, 0]
                                    ax2 = dataA[i, 0]
                                    ay1 = dataA[i - 1, 1]
                                    ay2 = dataA[i, 1]
                                    bx = dataB[j - 1, 0]
                                    by = dataB[j - 1, 1]
                                    distance1 = haversine(ax1, ay1, bx, by)
                                    distance2 = haversine(ax2, ay2, bx, by)
                                    inchdis1 = abs(dataB[j - 1, 2] - dataA[i - 1, 2])
                                    inchdis2 = abs(dataB[j - 1, 2] - dataA[i, 2])
                                    print("the distance is %d,%d\n" % (distance1, distance2))
                                    if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                        tim = (datetime.datetime.strptime(timeA[i],
                                                                          '%H:%M:%S') - datetime.datetime.strptime(
                                            timeA[i - 1], '%H:%M:%S')).seconds
                                        print("the tim is %d\n" % (tim))
                                        if flag == 0:
                                            time = tim
                                            num = num + 1
                                            print(type(num))
                                            mt[0].append(date)
                                            mt[1].append(number)
                                            mt[2].append(num)
                                            mt[3].append(time)
                                        else:
                                            time = time + tim
                                            mt[3][num - 1] = time
                                        flag = 1
                                    else:
                                        flag = 0

                                if dataA[i, 3] < dataB[j, 3]:
                                    bx1 = dataB[j - 1, 0]
                                    bx2 = dataB[j, 0]
                                    by1 = dataB[j - 1, 1]
                                    by2 = dataB[j, 1]
                                    ax = dataA[i, 0]
                                    ay = dataA[i, 1]
                                    distance1 = haversine(bx1, by1, ax, ay)
                                    distance2 = haversine(bx2, by2, ax, ay)
                                    inchdis1 = abs(dataA[i, 2] - dataB[j - 1, 2])
                                    inchdis2 = abs(dataA[i, 2] - dataB[j, 2])
                                    print("the distance is %d,%d\n" % (distance1, distance2))
                                    if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                        tim = (datetime.datetime.strptime(timeB[j],
                                                                          '%H:%M:%S') - datetime.datetime.strptime(
                                            timeB[j - 1], '%H:%M:%S')).seconds
                                        print("the tim is %d\n" % (tim))
                                        if flag == 0:
                                            time = tim
                                            num = num + 1
                                            print(type(num))
                                            mt[0].append(date)
                                            mt[1].append(number)
                                            mt[2].append(num)
                                            mt[3].append(time)
                                        else:
                                            time = time + tim
                                            mt[3][num - 1] = time
                                        flag = 1
                                    else:
                                        flag = 0

                                if dataA[i, 3] > dataB[j, 3]:
                                    ax1 = dataA[i - 1, 0]
                                    ax2 = dataA[i, 0]
                                    ay1 = dataA[i - 1, 1]
                                    ay2 = dataA[i, 1]
                                    bx = dataB[j, 0]
                                    by = dataB[j, 1]
                                    distance1 = haversine(ax1, ay1, bx, by)
                                    distance2 = haversine(ax2, ay2, bx, by)
                                    inchdis1 = abs(dataB[j, 2] - dataA[i - 1, 2])
                                    inchdis2 = abs(dataB[j, 2] - dataA[i, 2])
                                    print("the distance is %d,%d\n" % (distance1, distance2))
                                    if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                        tim = (datetime.datetime.strptime(timeA[i],
                                                                          '%H:%M:%S') - datetime.datetime.strptime(
                                            timeA[i - 1], '%H:%M:%S')).seconds
                                        print("the tim is %d\n" % (tim))
                                        if flag == 0:
                                            time = tim
                                            num = num + 1
                                            print(type(num))
                                            mt[0].append(date)
                                            mt[1].append(number)
                                            mt[2].append(num)
                                            mt[3].append(time)
                                        else:
                                            time = time + tim
                                            mt[3][num - 1] = time
                                        flag = 1
                                    else:
                                        flag = 0

                            else:
                                if dataA[i, 3] < dataB[j, 3]:
                                    bx1 = dataB[j - 1, 0]
                                    bx2 = dataB[j, 0]
                                    by1 = dataB[j - 1, 1]
                                    by2 = dataB[j, 1]
                                    ax = dataA[i, 0]
                                    ay = dataA[i, 1]
                                    distance1 = haversine(bx1, by1, ax, ay)
                                    distance2 = haversine(bx2, by2, ax, ay)
                                    inchdis1 = abs(dataA[i, 2] - dataB[j - 1, 2])
                                    inchdis2 = abs(dataA[i, 2] - dataB[j, 2])
                                    print("the distance is %d,%d\n" % (distance1, distance2))
                                    if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                        tim = (datetime.datetime.strptime(timeB[j],
                                                                          '%H:%M:%S') - datetime.datetime.strptime(
                                            timeB[j - 1], '%H:%M:%S')).seconds
                                        print("the tim is %d\n" % (tim))
                                        if flag == 0:
                                            time = tim
                                            num = num + 1
                                            print(type(num))
                                            mt[0].append(date)
                                            mt[1].append(number)
                                            mt[2].append(num)
                                            mt[3].append(time)
                                        else:
                                            time = time + tim
                                            mt[3][num - 1] = time
                                        flag = 1
                                    else:
                                        flag = 0
                            print("%d,%d--the time and num are %d,%d\n" % (i, j, time, num))
                            i = i + 1
                            j = j + 1
            else:
                if amax > bmin:
                    if amin > bmin:
                        mi = 0
                        ma = 0
                        time = 0  # 相遇时间长度
                        num = 0  # 相遇次数
                        flag = 0
                        for j in range(len(dataB[:, 3])):
                            if dataB[j, 3] >= amin:
                                mi = j
                                break
                        for j in range(len(dataB[:, 3])):
                            if dataB[j, 3] > amax:
                                ma = j
                                break
                        j = mi
                        i = 0
                        print(pa1, pa2)
                        while (j < ma and i < len(dataA[:, 3])):
                            if i > 0:
                                while dataA[i, 3] < dataB[j - 1, 3]:
                                    i = i + 1
                                    if i >= len(dataA[:, 3]):
                                        i = i - 1
                                        break
                                while dataB[j, 3] < dataA[i - 1, 3]:
                                    j = j + 1
                                    if j >= ma:
                                        j = j - 1
                                        break
                                if dataA[i, 3] < dataB[j - 1, 3] or dataB[j, 3] < dataA[i - 1, 3]:
                                    break
                                if dataA[i - 1, 3] == dataB[j - 1, 3] and dataA[i, 3] == dataB[j, 3]:
                                    distance1 = haversine(dataA[i - 1, 0], dataA[i - 1, 1], dataB[j - 1, 0],
                                                          dataB[j - 1, 1])
                                    distance2 = haversine(dataA[i, 0], dataA[i, 1], dataB[j, 0],
                                                          dataB[j, 1])
                                    inchdis1 = abs(dataA[i - 1, 2] - dataB[j - 1, 2])
                                    inchdis2 = abs(dataA[i, 2] - dataB[j, 2])
                                    print("the distance is %d,%d\n" % (distance1, distance2))
                                    if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                        tim = (datetime.datetime.strptime(timeA[i],
                                                                          '%H:%M:%S') - datetime.datetime.strptime(
                                            timeA[i - 1], '%H:%M:%S')).seconds
                                        print("the tim is %d\n" % (tim))
                                        if flag == 0:
                                            time = tim
                                            num = num + 1
                                            print(type(num))
                                            mt[0].append(date)
                                            mt[1].append(number)
                                            mt[2].append(num)
                                            mt[3].append(time)
                                        else:
                                            time = time + tim
                                            mt[3][num - 1] = time
                                        flag = 1
                                    else:
                                        flag = 0

                                if (dataA[i - 1, 3] > dataB[j - 1, 3] and dataA[i, 3] == dataB[j, 3]):
                                    bx1 = dataB[j - 1, 0]
                                    bx2 = dataB[j, 0]
                                    by1 = dataB[j - 1, 1]
                                    by2 = dataB[j, 1]
                                    ax = dataA[i - 1, 0]
                                    ay = dataA[i - 1, 1]
                                    distance1 = haversine(bx1, by1, ax, ay)
                                    distance2 = haversine(bx2, by2, ax, ay)
                                    inchdis1 = abs(dataA[i - 1, 2] - dataB[j - 1, 2])
                                    inchdis2 = abs(dataA[i - 1, 2] - dataB[j, 2])
                                    print("the distance is %d,%d\n" % (distance1, distance2))
                                    if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                        tim = (datetime.datetime.strptime(timeB[j],
                                                                          '%H:%M:%S') - datetime.datetime.strptime(
                                            timeB[j - 1], '%H:%M:%S')).seconds
                                        print("the tim is %d\n" % (tim))
                                        if flag == 0:
                                            time = tim
                                            num = num + 1
                                            print(type(num))
                                            mt[0].append(date)
                                            mt[1].append(number)
                                            mt[2].append(num)
                                            mt[3].append(time)
                                        else:
                                            time = time + tim
                                            mt[3][num - 1] = time
                                        flag = 1
                                    else:
                                        flag = 0

                                if (dataA[i - 1, 3] < dataB[j - 1, 3] and dataA[i, 3] == dataB[j, 3]):
                                    ax1 = dataA[i - 1, 0]
                                    ax2 = dataA[i, 0]
                                    ay1 = dataA[i - 1, 1]
                                    ay2 = dataA[i, 1]
                                    bx = dataB[j - 1, 0]
                                    by = dataB[j - 1, 1]
                                    distance1 = haversine(ax1, ay1, bx, by)
                                    distance2 = haversine(ax2, ay2, bx, by)
                                    inchdis1 = abs(dataB[j - 1, 2] - dataA[i - 1, 2])
                                    inchdis2 = abs(dataB[j - 1, 2] - dataA[i, 2])
                                    print("the distance is %d,%d\n" % (distance1, distance2))
                                    if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                        tim = (datetime.datetime.strptime(timeA[i],
                                                                          '%H:%M:%S') - datetime.datetime.strptime(
                                            timeA[i - 1], '%H:%M:%S')).seconds
                                        print("the tim is %d\n" % (tim))
                                        if flag == 0:
                                            time = tim
                                            num = num + 1
                                            print(type(num))
                                            mt[0].append(date)
                                            mt[1].append(number)
                                            mt[2].append(num)
                                            mt[3].append(time)
                                        else:
                                            time = time + tim
                                            mt[3][num - 1] = time
                                        flag = 1
                                    else:
                                        flag = 0

                                if dataA[i, 3] < dataB[j, 3]:
                                    bx1 = dataB[j - 1, 0]
                                    bx2 = dataB[j, 0]
                                    by1 = dataB[j - 1, 1]
                                    by2 = dataB[j, 1]
                                    ax = dataA[i, 0]
                                    ay = dataA[i, 1]
                                    distance1 = haversine(bx1, by1, ax, ay)
                                    distance2 = haversine(bx2, by2, ax, ay)
                                    inchdis1 = abs(dataA[i, 2] - dataB[j - 1, 2])
                                    inchdis2 = abs(dataA[i, 2] - dataB[j, 2])
                                    print("the distance is %d,%d\n" % (distance1, distance2))
                                    if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                        tim = (datetime.datetime.strptime(timeB[j],
                                                                          '%H:%M:%S') - datetime.datetime.strptime(
                                            timeB[j - 1], '%H:%M:%S')).seconds
                                        print("the tim is %d\n" % (tim))
                                        if flag == 0:
                                            time = tim
                                            num = num + 1
                                            print(type(num))
                                            mt[0].append(date)
                                            mt[1].append(number)
                                            mt[2].append(num)
                                            mt[3].append(time)
                                        else:
                                            time = time + tim
                                            mt[3][num - 1] = time
                                        flag = 1
                                    else:
                                        flag = 0

                                if dataA[i, 3] > dataB[j, 3]:
                                    ax1 = dataA[i - 1, 0]
                                    ax2 = dataA[i, 0]
                                    ay1 = dataA[i - 1, 1]
                                    ay2 = dataA[i, 1]
                                    bx = dataB[j, 0]
                                    by = dataB[j, 1]
                                    distance1 = haversine(ax1, ay1, bx, by)
                                    distance2 = haversine(ax2, ay2, bx, by)
                                    inchdis1 = abs(dataB[j, 2] - dataA[i - 1, 2])
                                    inchdis2 = abs(dataB[j, 2] - dataA[i, 2])
                                    print("the distance is %d,%d\n" % (distance1, distance2))
                                    if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                        tim = (datetime.datetime.strptime(timeA[i],
                                                                          '%H:%M:%S') - datetime.datetime.strptime(
                                            timeA[i - 1], '%H:%M:%S')).seconds
                                        print("the tim is %d\n" % (tim))
                                        if flag == 0:
                                            time = tim
                                            num = num + 1
                                            print(type(num))
                                            mt[0].append(date)
                                            mt[1].append(number)
                                            mt[2].append(num)
                                            mt[3].append(time)
                                        else:
                                            time = time + tim
                                            mt[3][num - 1] = time
                                        flag = 1
                                    else:
                                        flag = 0

                            else:
                                if dataA[i, 3] < dataB[j, 3]:
                                    bx1 = dataB[j - 1, 0]
                                    bx2 = dataB[j, 0]
                                    by1 = dataB[j - 1, 1]
                                    by2 = dataB[j, 1]
                                    ax = dataA[i, 0]
                                    ay = dataA[i, 1]
                                    distance1 = haversine(bx1, by1, ax, ay)
                                    distance2 = haversine(bx2, by2, ax, ay)
                                    inchdis1 = abs(dataA[i, 2] - dataB[j - 1, 2])
                                    inchdis2 = abs(dataA[i, 2] - dataB[j, 2])
                                    print("the distance is %d,%d\n" % (distance1, distance2))
                                    if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                        tim = (datetime.datetime.strptime(timeB[j],
                                                                          '%H:%M:%S') - datetime.datetime.strptime(
                                            timeB[j - 1], '%H:%M:%S')).seconds
                                        print("the tim is %d\n" % (tim))
                                        if flag == 0:
                                            time = tim
                                            num = num + 1
                                            print(type(num))
                                            mt[0].append(date)
                                            mt[1].append(number)
                                            mt[2].append(num)
                                            mt[3].append(time)
                                        else:
                                            time = time + tim
                                            mt[3][num - 1] = time
                                        flag = 1
                                    else:
                                        flag = 0
                            print("%d,%d--the time and num are %d,%d\n" % (i, j, time, num))
                            i = i + 1
                            j = j + 1
                    else:
                        if amin == bmin:
                            mi = 0
                            ma = 0
                            time = 0  # 相遇时间长度
                            num = 0  # 相遇次数
                            flag = 0
                            for j in range(len(dataB[:, 3])):
                                if dataB[j, 3] > amax:
                                    ma = j
                                    break
                            i = 0
                            j = 0
                            print(pa1, pa2)
                            while (j < ma) and i < len(dataA[:, 3]):  # i为dataB序号，j为dataA序号
                                if j > 0 and i > 0:
                                    while dataA[i, 3] < dataB[j - 1, 3]:
                                        i = i + 1
                                        if i >= len(dataA[:, 3]):
                                            i = i - 1
                                            break
                                    while dataB[j, 3] < dataA[i - 1, 3]:
                                        j = j + 1
                                        if j >= ma:
                                            j = j - 1
                                            break
                                    if dataA[i, 3] < dataB[j - 1, 3] or dataB[j, 3] < dataA[i - 1, 3]:
                                        break
                                    if dataA[i - 1, 3] == dataB[j - 1, 3] and dataA[i, 3] == dataB[j, 3]:
                                        distance1 = haversine(dataA[i - 1, 0], dataA[i - 1, 1], dataB[j - 1, 0],
                                                              dataB[j - 1, 1])
                                        distance2 = haversine(dataA[i, 0], dataA[i, 1], dataB[j, 0],
                                                              dataB[j, 1])
                                        inchdis1 = abs(dataA[i - 1, 2] - dataB[j - 1, 2])
                                        inchdis2 = abs(dataA[i, 2] - dataB[j, 2])
                                        print("the distance is %d,%d\n" % (distance1, distance2))
                                        if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                            tim = (datetime.datetime.strptime(timeA[i],
                                                                              '%H:%M:%S') - datetime.datetime.strptime(
                                                timeA[i - 1], '%H:%M:%S')).seconds
                                            print("the tim is %d\n" % (tim))
                                            if flag == 0:
                                                time = tim
                                                num = num + 1
                                                print(type(num))
                                                mt[0].append(date)
                                                mt[1].append(number)
                                                mt[2].append(num)
                                                mt[3].append(time)
                                            else:
                                                time = time + tim
                                                mt[3][num - 1] = time
                                            flag = 1
                                        else:
                                            flag = 0

                                    if (dataA[i - 1, 3] > dataB[j - 1, 3] and dataA[i, 3] == dataB[j, 3]):
                                        bx1 = dataB[j - 1, 0]
                                        bx2 = dataB[j, 0]
                                        by1 = dataB[j - 1, 1]
                                        by2 = dataB[j, 1]
                                        ax = dataA[i - 1, 0]
                                        ay = dataA[i - 1, 1]
                                        distance1 = haversine(bx1, by1, ax, ay)
                                        distance2 = haversine(bx2, by2, ax, ay)
                                        inchdis1 = abs(dataA[i - 1, 2] - dataB[j - 1, 2])
                                        inchdis2 = abs(dataA[i - 1, 2] - dataB[j, 2])
                                        print("the distance is %d,%d\n" % (distance1, distance2))
                                        if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                            tim = (datetime.datetime.strptime(timeB[j],
                                                                              '%H:%M:%S') - datetime.datetime.strptime(
                                                timeB[j - 1], '%H:%M:%S')).seconds
                                            print("the tim is %d\n" % (tim))
                                            if flag == 0:
                                                time = tim
                                                num = num + 1
                                                print(type(num))
                                                mt[0].append(date)
                                                mt[1].append(number)
                                                mt[2].append(num)
                                                mt[3].append(time)
                                            else:
                                                time = time + tim
                                                mt[3][num - 1] = time
                                            flag = 1
                                        else:
                                            flag = 0

                                    if (dataA[i - 1, 3] < dataB[j - 1, 3] and dataA[i, 3] == dataB[j, 3]):
                                        ax1 = dataA[i - 1, 0]
                                        ax2 = dataA[i, 0]
                                        ay1 = dataA[i - 1, 1]
                                        ay2 = dataA[i, 1]
                                        bx = dataB[j - 1, 0]
                                        by = dataB[j - 1, 1]
                                        distance1 = haversine(ax1, ay1, bx, by)
                                        distance2 = haversine(ax2, ay2, bx, by)
                                        inchdis1 = abs(dataB[j - 1, 2] - dataA[i - 1, 2])
                                        inchdis2 = abs(dataB[j - 1, 2] - dataA[i, 2])
                                        print("the distance is %d,%d\n" % (distance1, distance2))
                                        if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                            tim = (datetime.datetime.strptime(timeA[i],
                                                                              '%H:%M:%S') - datetime.datetime.strptime(
                                                timeA[i - 1], '%H:%M:%S')).seconds
                                            print("the tim is %d\n" % (tim))
                                            if flag == 0:
                                                time = tim
                                                num = num + 1
                                                print(type(num))
                                                mt[0].append(date)
                                                mt[1].append(number)
                                                mt[2].append(num)
                                                mt[3].append(time)
                                            else:
                                                time = time + tim
                                                mt[3][num - 1] = time
                                            flag = 1
                                        else:
                                            flag = 0

                                    if dataA[i, 3] < dataB[j, 3]:
                                        bx1 = dataB[j - 1, 0]
                                        bx2 = dataB[j, 0]
                                        by1 = dataB[j - 1, 1]
                                        by2 = dataB[j, 1]
                                        ax = dataA[i, 0]
                                        ay = dataA[i, 1]
                                        distance1 = haversine(bx1, by1, ax, ay)
                                        distance2 = haversine(bx2, by2, ax, ay)
                                        inchdis1 = abs(dataA[i, 2] - dataB[j - 1, 2])
                                        inchdis2 = abs(dataA[i, 2] - dataB[j, 2])
                                        print("the distance is %d,%d\n" % (distance1, distance2))
                                        if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                            tim = (datetime.datetime.strptime(timeB[j],
                                                                              '%H:%M:%S') - datetime.datetime.strptime(
                                                timeB[j - 1], '%H:%M:%S')).seconds
                                            print("the tim is %d\n" % (tim))
                                            if flag == 0:
                                                time = tim
                                                num = num + 1
                                                print(type(num))
                                                mt[0].append(date)
                                                mt[1].append(number)
                                                mt[2].append(num)
                                                mt[3].append(time)
                                            else:
                                                time = time + tim
                                                mt[3][num - 1] = time
                                            flag = 1
                                        else:
                                            flag = 0

                                    if dataA[i, 3] > dataB[j, 3]:
                                        ax1 = dataA[i - 1, 0]
                                        ax2 = dataA[i, 0]
                                        ay1 = dataA[i - 1, 1]
                                        ay2 = dataA[i, 1]
                                        bx = dataB[j, 0]
                                        by = dataB[j, 1]
                                        distance1 = haversine(ax1, ay1, bx, by)
                                        distance2 = haversine(ax2, ay2, bx, by)
                                        inchdis1 = abs(dataB[j, 2] - dataA[i - 1, 2])
                                        inchdis2 = abs(dataB[j, 2] - dataA[i, 2])
                                        print("the distance is %d,%d\n" % (distance1, distance2))
                                        if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                            tim = (datetime.datetime.strptime(timeA[i],
                                                                              '%H:%M:%S') - datetime.datetime.strptime(
                                                timeA[i - 1], '%H:%M:%S')).seconds
                                            print("the tim is %d\n" % (tim))
                                            if flag == 0:
                                                time = tim
                                                num = num + 1
                                                print(type(num))
                                                mt[0].append(date)
                                                mt[1].append(number)
                                                mt[2].append(num)
                                                mt[3].append(time)
                                            else:
                                                time = time + tim
                                                mt[3][num - 1] = time
                                            flag = 1
                                        else:
                                            flag = 0

                                print("%d,%d--the time and num are %d,%d\n" % (i, j, time, num))
                                i = i + 1
                                j = j + 1
                        else:
                            mi = 0
                            ma = 0
                            time = 0  # 相遇时间长度
                            num = 0  # 相遇次数
                            flag = 0
                            for i in range(len(dataA[:, 3])):
                                if dataA[i, 3] >= bmin:
                                    mi = i
                                    break
                            for i in range(len(dataB[:, 3])):
                                if dataB[i, 3] > amax:
                                    ma = i
                                    break
                            i = mi
                            j = 0
                            print(pa1, pa2)
                            while (i < len(dataA[:, 3]) and j < ma):  # b集合中的序号
                                if j > 0:
                                    while dataA[i, 3] < dataB[j - 1, 3]:
                                        i = i + 1
                                        if i >= len(dataA[:, 3]):
                                            i = i - 1
                                            break
                                    while dataB[j, 3] < dataA[i - 1, 3]:
                                        j = j + 1
                                        if j >= ma:
                                            j = j - 1
                                            break
                                    if dataA[i, 3] < dataB[j - 1, 3] or dataB[j, 3] < dataA[i - 1, 3]:
                                        break
                                    if dataA[i - 1, 3] == dataB[j - 1, 3] and dataA[i, 3] == dataB[j, 3]:
                                        distance1 = haversine(dataA[i - 1, 0], dataA[i - 1, 1], dataB[j - 1, 0],
                                                              dataB[j - 1, 1])
                                        distance2 = haversine(dataA[i, 0], dataA[i, 1], dataB[j, 0],
                                                              dataB[j, 1])
                                        inchdis1 = abs(dataA[i - 1, 2] - dataB[j - 1, 2])
                                        inchdis2 = abs(dataA[i, 2] - dataB[j, 2])
                                        print("the distance is %d,%d\n" % (distance1, distance2))
                                        if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                            tim = (datetime.datetime.strptime(timeA[i],
                                                                              '%H:%M:%S') - datetime.datetime.strptime(
                                                timeA[i - 1], '%H:%M:%S')).seconds
                                            print("the tim is %d\n" % (tim))
                                            if flag == 0:
                                                time = tim
                                                num = num + 1
                                                print(type(num))
                                                mt[0].append(date)
                                                mt[1].append(number)
                                                mt[2].append(num)
                                                mt[3].append(time)
                                            else:
                                                time = time + tim
                                                mt[3][num - 1] = time
                                            flag = 1
                                        else:
                                            flag = 0

                                    if (dataA[i - 1, 3] > dataB[j - 1, 3] and dataA[i, 3] == dataB[j, 3]):
                                        bx1 = dataB[j - 1, 0]
                                        bx2 = dataB[j, 0]
                                        by1 = dataB[j - 1, 1]
                                        by2 = dataB[j, 1]
                                        ax = dataA[i - 1, 0]
                                        ay = dataA[i - 1, 1]
                                        distance1 = haversine(bx1, by1, ax, ay)
                                        distance2 = haversine(bx2, by2, ax, ay)
                                        inchdis1 = abs(dataA[i - 1, 2] - dataB[j - 1, 2])
                                        inchdis2 = abs(dataA[i - 1, 2] - dataB[j, 2])
                                        print("the distance is %d,%d\n" % (distance1, distance2))
                                        if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                            tim = (datetime.datetime.strptime(timeB[j],
                                                                              '%H:%M:%S') - datetime.datetime.strptime(
                                                timeB[j - 1], '%H:%M:%S')).seconds
                                            print("the tim is %d\n" % (tim))
                                            if flag == 0:
                                                time = tim
                                                num = num + 1
                                                print(type(num))
                                                mt[0].append(date)
                                                mt[1].append(number)
                                                mt[2].append(num)
                                                mt[3].append(time)
                                            else:
                                                time = time + tim
                                                mt[3][num - 1] = time
                                            flag = 1
                                        else:
                                            flag = 0

                                    if (dataA[i - 1, 3] < dataB[j - 1, 3] and dataA[i, 3] == dataB[j, 3]):
                                        ax1 = dataA[i - 1, 0]
                                        ax2 = dataA[i, 0]
                                        ay1 = dataA[i - 1, 1]
                                        ay2 = dataA[i, 1]
                                        bx = dataB[j - 1, 0]
                                        by = dataB[j - 1, 1]
                                        distance1 = haversine(ax1, ay1, bx, by)
                                        distance2 = haversine(ax2, ay2, bx, by)
                                        inchdis1 = abs(dataB[j - 1, 2] - dataA[i - 1, 2])
                                        inchdis2 = abs(dataB[j - 1, 2] - dataA[i, 2])
                                        print("the distance is %d,%d\n" % (distance1, distance2))
                                        if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                            tim = (datetime.datetime.strptime(timeA[i],
                                                                              '%H:%M:%S') - datetime.datetime.strptime(
                                                timeA[i - 1], '%H:%M:%S')).seconds
                                            print("the tim is %d\n" % (tim))
                                            if flag == 0:
                                                time = tim
                                                num = num + 1
                                                print(type(num))
                                                mt[0].append(date)
                                                mt[1].append(number)
                                                mt[2].append(num)
                                                mt[3].append(time)
                                            else:
                                                time = time + tim
                                                mt[3][num - 1] = time
                                            flag = 1
                                        else:
                                            flag = 0

                                    if dataA[i, 3] < dataB[j, 3]:
                                        bx1 = dataB[j - 1, 0]
                                        bx2 = dataB[j, 0]
                                        by1 = dataB[j - 1, 1]
                                        by2 = dataB[j, 1]
                                        ax = dataA[i, 0]
                                        ay = dataA[i, 1]
                                        distance1 = haversine(bx1, by1, ax, ay)
                                        distance2 = haversine(bx2, by2, ax, ay)
                                        inchdis1 = abs(dataA[i, 2] - dataB[j - 1, 2])
                                        inchdis2 = abs(dataA[i, 2] - dataB[j, 2])
                                        print("the distance is %d,%d\n" % (distance1, distance2))
                                        if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                            tim = (datetime.datetime.strptime(timeB[j],
                                                                              '%H:%M:%S') - datetime.datetime.strptime(
                                                timeB[j - 1], '%H:%M:%S')).seconds
                                            print("the tim is %d\n" % (tim))
                                            if flag == 0:
                                                time = tim
                                                num = num + 1
                                                print(type(num))
                                                mt[0].append(date)
                                                mt[1].append(number)
                                                mt[2].append(num)
                                                mt[3].append(time)
                                            else:
                                                time = time + tim
                                                mt[3][num - 1] = time
                                            flag = 1
                                        else:
                                            flag = 0

                                    if dataA[i, 3] > dataB[j, 3]:
                                        ax1 = dataA[i - 1, 0]
                                        ax2 = dataA[i, 0]
                                        ay1 = dataA[i - 1, 1]
                                        ay2 = dataA[i, 1]
                                        bx = dataB[j, 0]
                                        by = dataB[j, 1]
                                        distance1 = haversine(ax1, ay1, bx, by)
                                        distance2 = haversine(ax2, ay2, bx, by)
                                        inchdis1 = abs(dataB[j, 2] - dataA[i - 1, 2])
                                        inchdis2 = abs(dataB[j, 2] - dataA[i, 2])
                                        print("the distance is %d,%d\n" % (distance1, distance2))
                                        if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                            tim = (datetime.datetime.strptime(timeA[i],
                                                                              '%H:%M:%S') - datetime.datetime.strptime(
                                                timeA[i - 1], '%H:%M:%S')).seconds
                                            print("the tim is %d\n" % (tim))
                                            if flag == 0:
                                                time = tim
                                                num = num + 1
                                                print(type(num))
                                                mt[0].append(date)
                                                mt[1].append(number)
                                                mt[2].append(num)
                                                mt[3].append(time)
                                            else:
                                                time = time + tim
                                                mt[3][num - 1] = time
                                            flag = 1
                                        else:
                                            flag = 0

                                else:
                                    if dataA[i, 3] > dataB[j, 3]:
                                        ax1 = dataA[i - 1, 0]
                                        ax2 = dataA[i, 0]
                                        ay1 = dataA[i - 1, 1]
                                        ay2 = dataA[i, 1]
                                        bx = dataB[j, 0]
                                        by = dataB[j, 1]
                                        distance1 = haversine(ax1, ay1, bx, by)
                                        distance2 = haversine(ax2, ay2, bx, by)
                                        inchdis1 = abs(dataB[j, 2] - dataA[i - 1, 2])
                                        inchdis2 = abs(dataB[j, 2] - dataA[i, 2])
                                        print("the distance is %d,%d\n" % (distance1, distance2))
                                        if (distance1 <= 10 and distance2 <= 10 and inchdis1 <= 20 and inchdis2 <= 20):
                                            tim = (datetime.datetime.strptime(timeA[i],
                                                                              '%H:%M:%S') - datetime.datetime.strptime(
                                                timeA[i - 1], '%H:%M:%S')).seconds
                                            print("the tim is %d\n" % (tim))
                                            if flag == 0:
                                                time = tim
                                                num = num + 1
                                                print(type(num))
                                                mt[0].append(date)
                                                mt[1].append(number)
                                                mt[2].append(num)
                                                mt[3].append(time)
                                            else:
                                                time = time + tim
                                                mt[3][num - 1] = time
                                            flag = 1
                                        else:
                                            flag = 0

                                print("%d,%d--the time and num are %d,%d\n" % (i, j, time, num))
                                i = i + 1
                                j = j + 1
    print(mt)
    return mt


def haversine(lon1, lat1, lon2, lat2):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    return c * r * 1000

def Meet(user1, user2, path):  # 遍历提供的用户轨迹文件路径，得到用户关系表
    path1 = path+'\\'+user1+ '\\Trajectory'
    path2 = path+'\\'+user2+'\\Trajectory'
    files1 = os.listdir(path1)  # 得到文件夹下的所有文件名称
    files2 = os.listdir(path2)
    oneDay = []
    for file1 in files1:  # 遍历文件夹
        for file2 in files2:
            if not (os.path.isdir(file1) and os.path.isdir(file2)):  # 判断file1、file2是否是文件夹，不是文件夹才打开
                if cmp(file1[0:8], file2[0:8]) == 0 and cmp(file1[14:],'.csv')==0 and cmp(file2[14:],'.csv')==0:
                    s = []
                    s.append(file1)
                    s.append(file2)
                    print(s)
                    oneDay.append(s)
    #print(oneDay)  # 打印结果
    i = 0
    flagW = ''
    number = 0
    Mt = []
    for one in oneDay:
        pa1 = path1 + '\\' + one[0]
        pa2 = path2 + '\\' + one[1]
        date = one[0][0:8]
        if cmp(date, flagW) == 0:
            number = number + 1
        else:
            number = 1
            flagW = date
        i = i + 1
        print(i)
        mt = meeting(pa1, pa2, date, number)
        Mt.append(mt)

    print(Mt)
    MT = [[], [], [], []]
    for met in Mt:
        if met[0]!=None:
            for i in range(len(met[0])):
                MT[0].append(met[0][i])
                MT[1].append(met[1][i])
                MT[2].append(met[2][i])
                MT[3].append(met[3][i])
    print(MT)
    return MT

def preHandle(user,path):
    path = path + '\\' + user + '\\Trajectory'
    files = os.listdir(path)
    for file in files:
        if cmp(file[14:],'.plt')==0:
            pa = path + '\\' + file
            delete6(pa)
            noiseReduct(pa)
            Segmentation(file,pa,path)

def noiseReduct(pa):
    All = []
    reader = csv.reader(open(pa, ), delimiter=',')
    for line in list(reader):
        All.append(line)

    i = 1
    bp = []
    while (i < len(All)):
        tim = (datetime.datetime.strptime(All[i][6], '%H:%M:%S') - datetime.datetime.strptime(
            All[i - 1][6], '%H:%M:%S')).seconds
        if tim == 0:
            bp.append(i)
        i = i + 1
    print(bp)

    i = 0
    j = 0
    with open(pa, "r") as f:
        lines = f.readlines()
        # print(lines)
    with open(pa, "w") as f_w:
        for line in lines:
            for b in bp:
                if i == b:
                    j = 1
            if j == 1:
                j = 0
                i = i + 1
                continue
            i = i + 1
            f_w.write(line)


def ergo(path,user,n):
    files = os.listdir(path)
    #preHandle(user, path)
    ME = []
    i = 0
    for file in files:
        if i>n:
            # preHandle(fil, 'D:\Geolife\Geolife Trajectories 1.3\Data')
            MEET = Meet(user, file, path)
            ME.append(MEET[3])
        i = i + 1
    m = 0
    with open(path+'\\'+user+'\\meetIndicate.csv', "w") as f:
        c_write = csv.writer(f, dialect='excel')
        for mm in ME:
            m = m + 1
            print(m)
            print(mm)
            c_write.writerow(mm)

path = 'E:\\Geolife\\Geolife Trajectories 1.3\\Data'
#path是Geolife数据的用户文件夹（如000，001，002……）所在的路径
fils= os.listdir(path)
ii = 0
for fil in fils:
    if ii > 0:
        print('\n')
        print(fil)
        ergo(path, fil, ii)

    ii = ii + 1
