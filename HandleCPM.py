#!/usr/bin/python
# -*- coding: utf-8 -*-
#CPM算法运行结果的可视化处理
import os
import csv
import datetime
from numpy import genfromtxt,zeros
from pylab import plot,show
from math import radians, cos, sin, asin, sqrt
import types
import networkx as nx
import numpy as np
import math
import random as rand
import sys
import matplotlib.pyplot as plt
from numpy import genfromtxt,zeros


def buildG(G, file_, delimiter_):
    reader = csv.reader(open(file_), delimiter=delimiter_)
    for line in list(reader):
        G.add_edge(int(line[0]),int(line[1]))

def showG(partition,initG):
    color = ["dimgrey","rosybrown","brown","tomato","chocolate",
             "gold","darkkhaki","olivedrab","yellowgreen","darkseagreen",
             "lightseagreen","cyan","deepskyblue","steelblue","mediumpurple","indigo",
            "fuchsia","mediumvioletred","crimson","darkslategrey","darkgreen"
             ]
    #size = len(set(partition.values()))
    pos = nx.random_layout(initG)
    count = 0

    nx.draw(initG, pos, node_size=250, alpha=0.5, edge_color='r', font_size=12, with_labels=True)
    plt.show()
    for com in set(partition.values()):
        list_nodes = [nodes for nodes in partition.keys()
                      if partition[nodes] == com]
        print("Community "+str(count))
        print("Nodes: "+str(list_nodes))
        print("Size:"+str(len(list_nodes)))
        print(initG.edges(list_nodes))
        #   list_edges = []
        #   for node in list_nodes:
        #       for edge in initG.edges():
        #           if node == edge[0]:
        #               for nod in list_nodes:
        #                   if nod == edge[1]:
        #                       list_edges.append(edge)
        nx.draw_networkx_nodes(initG, pos, list_nodes, node_size=250,
                               node_color=color[count])
        #    nx.draw_networkx_edges(initG, pos, list_edges, with_labels=True, alpha=0.5)
        #    nx.draw_networkx_labels(initG, pos)
        #    plt.show()
        #    plt.clf()
        count = count + 1

    nx.draw_networkx_edges(initG, pos, with_labels=True, alpha=0.5)
    nx.draw_networkx_labels(initG, pos)
    plt.show()

def resultG(partition,G):
    #size = len(set(partition.values()))
    pos = nx.random_layout(G)
    count = 0
    for com in set(partition.values()):
        list_nodes = [nodes for nodes in partition.keys()
                      if partition[nodes] == com]
        list_edges = []
        for node in list_nodes:
          for edge in G.edges():
                if node==edge[0]:
                   for nod in list_nodes:
                       if nod==edge[1]:
                            continue
                       list_edges.append(edge)
                   continue
                else:
                    if node==edge[1]:
                        for nod in list_nodes:
                            if nod==edge[0]:
                                continue
                            list_edges.append(edge)
                        continue
                list_edges.append(edge)
        G.remove_edges_from(list_edges)
        print(G.edges())
        #print(list_edges)
        #nx.draw_networkx_nodes(G, pos, list_nodes, node_size=250,
        #                       node_color=color[count], label=True)
        #nx.draw_networkx_edges(G, pos, list_edges,with_labels=True, alpha=0.5)
        #plt.show()
        #plt.clf()

    #nx.draw_networkx_nodes(G, pos, node_size=250, label=True)
    #plt.show()
    return G

def UpdateDeg(A, nodes):
    deg_dict = {}
    n = len(nodes)#图中点的个数
    B = A.sum(axis = 1)#将矩阵的每一行向量相加，所得一个数组赋给B，表示与每个点相关的边数
    for i in range(n):
        deg_dict[list(nodes)[i]] = B[i,0]#将该值存到索引是i的元组中
    return deg_dict

def GetModularity(G, deg_, m_):
    New_A = nx.adj_matrix(G)#建立一个表示边的邻接矩阵
    New_deg = {}
    New_deg = UpdateDeg(New_A, G.nodes())
    #计算Q值
    print('Number of communities in decomposed G: %d' % nx.number_connected_components(G))
    Mod = 0#设定社团划分的模块化系数并设初始值为0
    for c in sorted(nx.connected_components(G), key=len, reverse=True):
        AVW = 0  # 两条边在邻接矩阵中的值
        K = 0  # 两条边的度值
        for u in c:
            AVW += New_deg[u]
            K += deg_[u]
        Mod += (float(AVW) - float(K * K) / float(2 * m_))  # 计算出Q值公式累加符号后的值
    Mod = Mod/float(2*m_)#计算出模块化Q值
    return Mod

def HandleCPM():
    with open("E:\\Geolife\\Geolife Trajectories 1.3" + '\\CPMCommeet.csv', "r") as f:
        lines = f.readlines()
        # print(lines)
    with open("E:\\Geolife\\Geolife Trajectories 1.3" + '\\CPMCommeet.csv', "w") as f_w:
        for line in lines:
            if "components_1" in line:
                continue
            f_w.write(line)
    com = genfromtxt("E:\\Geolife\\Geolife Trajectories 1.3" + '\\CPMCommeet.csv', delimiter=',')

    where_are_nan = np.isnan(com)
    com[where_are_nan] = -1
    print(com)
    for a in com:
        for b in a:
            if b == -1:
                continue
            b = int(b)

    print(com)

    partition = {}
    i = 0
    for a in com:
        for b in a:
            if b==-1:
                continue
            partition[b] = i
        i = i + 1

    print(partition)
    return partition

partition = HandleCPM()
graph_fn = 'E:\\Geolife\\Geolife Trajectories 1.3\\meetforGN.csv'
G = nx.Graph()
buildG(G, graph_fn, ',')
n = G.number_of_nodes()  # 顶点数量
A = nx.adj_matrix(G)  # 邻接矩阵
m_ = 0.0  # 计算边的数量
for i in range(0, n):
    for j in range(0, n):
        m_ += A[i, j]
m_ = m_ / 2.0
# 计算点的度
Orig_deg = {}
Orig_deg = UpdateDeg(A, G.nodes())
# 最初图
G = resultG(partition,G)
Q = GetModularity(G,Orig_deg,m_)
print(Q)
initG = nx.Graph()
buildG(initG, graph_fn, ',')
#plt.show()
showG(partition,initG)