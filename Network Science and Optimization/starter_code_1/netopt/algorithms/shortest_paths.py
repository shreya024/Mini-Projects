from collections import deque
from math import inf


def bellman_ford():
    pass

def dijkstra():
    pass

def reverse_dijkstra(graph,target):
    dist = {node: float('inf') for node in graph.nodes}
    dist[target]=0
    successor = {node: -1 for node in graph.nodes}

    #set S for all nodes whose labels are set
    s=set()
    #set S' for all nodes whose labels are not set
    sbar=set(graph.nodes)
 
    while sbar:
        # pick u with lowest dist label
        lowest=float('inf')
        v=-1
        for d in sbar:
            #print(d.dtype)
        
            if dist[d]<=lowest:
                lowest=dist[d]
                v=d

        #if v==-1:
            #print('sbar',sbar)
      
        # add u to S
        s.add(v)
        # remove u from sbar
        sbar.remove(v)

        for u in graph.nodes:
            if v in graph.adj[u]:
                if(dist[u]>dist[v]+graph.adj[u][v]["length"]):
                    dist[u]=dist[v]+graph.adj[u][v]["length"]
                    successor[u]=v
        
    return dist
def bidirectional_dijkstra():
    pass


def floyd_warshall():
    pass