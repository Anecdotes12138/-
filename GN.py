#!/usr/bin/python
# -*- coding: utf-8 -*-
#GN算法运行和结果可视化处理
import networkx as nx
import math
import csv
import random as rand
import sys
import matplotlib.pyplot as plt
from numpy import genfromtxt,zeros
import datetime,time

def toDICT(Bcoms):
    i = 0
    partition = {}
    for coms in Bcoms:
        for com in coms:
            partition[com]=i
        i = i + 1
    print(partition)
    return partition

def showG(partition,initG):
    color = ["dimgrey","rosybrown","brown","tomato","chocolate",
             "gold","darkkhaki","olivedrab","yellowgreen","darkseagreen",
             "lightseagreen","cyan","deepskyblue","steelblue","mediumpurple","indigo",
            "fuchsia","mediumvioletred","crimson","darkslategrey","darkgreen"
             ]
    #size = len(set(partition.values()))
    pos = nx.random_layout(initG)
    count = 0

    print(initG.nodes())
    nx.draw(initG, pos, node_size=250, alpha=0.5, edge_color='r', font_size=9, with_labels=True)
    plt.show()
    for com in set(partition.values()):
        list_nodes = [nodes for nodes in partition.keys()
                      if partition[nodes] == com]
        if len(list_nodes)<=1:
            continue
        print("Community " + str(count))
        print("Nodes: " + str(list_nodes))
        print("Size:" + str(len(list_nodes)))
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


def buildG(G, file_, delimiter_):
    reader = csv.reader(open(file_), delimiter=delimiter_)
    for line in list(reader):
        G.add_edge(int(line[0]),int(line[1]))

def CmtyStep(G):
    init_number_comp = nx.number_connected_components(G) #
    number_comp = init_number_comp
    while number_comp <= init_number_comp:
        bw = nx.edge_betweenness_centrality(G)#计算所有边的边介数中心性
        if bw.values() == []:
            break
        else:
            max_ = max(bw.values())#将边介数中心性最大的值赋给max_
        for k, v in bw.items():#删除边介数中心性的值最大的边
            if float(v) == max_:
                G.remove_edge(k[0],k[1])
        number_comp = nx.number_connected_components(G)#计算新的社团数量

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

def UpdateDeg(A, nodes):
    deg_dict = {}
    n = len(nodes)#图中点的个数
    B = A.sum(axis = 1)#将矩阵的每一行向量相加，所得一个数组赋给B，表示与每个点相关的边数
    for i in range(n):
        deg_dict[list(nodes)[i]] = B[i,0]#将该值存到索引是i的元组中
    return deg_dict

def runGirvanNewman(G, Orig_deg, m_):
    BestQ = 0.0
    Q = 0.0
    Bestcomps = list(nx.connected_components(G))
    while True:
        CmtyStep(G)
        Q = GetModularity(G, Orig_deg, m_);
        print("Modularity of decomposed G: %f" % Q)
        if Q > BestQ:
            BestQ = Q
            Bestcomps = list(nx.connected_components(G))
            BestG = nx.Graph()
            BestG = G
            print("Components:", Bestcomps)
            #pos = nx.spring_layout(BestG)
            #nx.draw(BestG,pos,node_size = 100,alpha = 0.5,edge_color = 'b',font_size = 9,with_labels=True)
            #plt.savefig('BestG.png')
            #plt.show()
            #plt.clf()
        if G.number_of_edges() == 0:
            break
    if BestQ > 0.0:
        print("Max modularity (Q): %f" % BestQ)
        print("Graph communities:", Bestcomps)
        return Bestcomps
    else:
        print("Max modularity (Q): %f" % BestQ)


starttime = datetime.datetime.now()
#long running
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
initG = nx.Graph()  # 不能用initG = G，这样只是多添了一个指针
buildG(initG, graph_fn, ',')
endtime = datetime.datetime.now()
print endtime - starttime
#pos = nx.spring_layout(initG)
#nx.draw(initG, pos, node_size=100, alpha=0.5, edge_color='r', font_size=9, with_labels=True)
#plt.show()
# 调用算法
Bcomps = runGirvanNewman(G, Orig_deg, m_)
partition = toDICT(Bcomps)
showG(partition, initG)





