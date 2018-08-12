#!/usr/bin/python
# -*- coding: utf-8 -*-
#FN算法运行结果的可视化处理
import os
import csv
import datetime
from numpy import genfromtxt,zeros
from pylab import plot,show
from math import radians, cos, sin, asin, sqrt
import types
import networkx as nx
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

    print(initG.edges())
    nx.draw(initG, pos, node_size=250, alpha=0.5, edge_color='r', font_size=9, with_labels=True)
    plt.show()
    for com in set(partition.values()):
        list_nodes = [nodes for nodes in partition.keys()
                      if partition[nodes] == com]
        if len(list_nodes)<=1:
            continue
        print("Community " + str(count))
        print("Nodes: " + str(list_nodes))
        print("Size:"+str(len(list_nodes)))
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

def HandleFN():
    mod = genfromtxt("E:\\Geolife\\Geolife Trajectories 1.3" + '\\FNModmeet.csv', delimiter=',')
    clu = genfromtxt("E:\\Geolife\\Geolife Trajectories 1.3" + '\\FNCommeet.csv', delimiter=',')
    i = 0
    ma = max(mod)
    print(ma)
    for m in mod:
        if m == ma:
            be = i
        i = i + 1
    print(be)
    i = 0
    j = 0
    best = []
    for c in clu:
        i = j // 3
        if i == be:
            best = clu[j+2]
            break
        j = j + 1

    print(best)
    partition = {}
    for com in set(best):
        for node in range(len(best)):
            if best[node] == com:
                partition[int(node)+1] = int(com)

    print(partition)
    return partition

partition = HandleFN()
graph_fn = 'E:\\Geolife\\Geolife Trajectories 1.3\\meetforGN.csv'
initG = nx.Graph()
buildG(initG, graph_fn, ',')
plt.show()
showG(partition,initG)