from collections import deque
#from math import inf
import heapq


def bellman_ford():
    pass

def dijkstra(graph,source):
    dist={node: float('inf') for node in graph.nodes}
    dist[source]=0

    predecessor={node:-1 for node in graph.nodes}

    #set S for all nodes whose labels are set
    s=set()
    #set S' for all nodes whose labels are not set
    sbar=set(graph.nodes)

    while sbar:
        # pick u with lowest dist label
        lowest=float('inf')
        u=-1
        for d in sbar:
            #print(d.dtype)
        
            if dist[d]<=lowest:
                lowest=dist[d]
                u=d

        # add u to S
        s.add(u)
        # remove u from sbar
        sbar.remove(u)

        for v in graph.adj[u]:
            if(dist[u]>dist[v]+graph.adj[u][v]["length"]):
                    dist[u]=dist[v]+graph.adj[u][v]["length"]
                    predecessor[u]=v

        return dist
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

def reverse_dijkstra_using_heap(graph,target):
    dist = {node: float('inf') for node in graph.nodes}
    dist[target]=0
    successor = {node: -1 for node in graph.nodes}

    #set S for all nodes whose labels are set
    s=set()
    #set S' for all nodes whose labels are not set
    sbar=set(graph.nodes)

    # min-heap: (distance, node)
    heap = [(0, target)]
 
    while sbar:
      
        curr_dist, v = heapq.heappop(heap)
        # add u to S
        s.add(v)
        # remove u from sbar
        sbar.remove(v)

        for u in graph.nodes:
            if v in graph.adj[u]:
                if(dist[u]>dist[v]+graph.adj[u][v]["length"]):
                    dist[u]=dist[v]+graph.adj[u][v]["length"]
                    successor[u]=v
                    heapq.heappush(heap, (dist[u], u))
        
    return dist

def bidirectional_dijkstra():
    pass


def floyd_warshall():
    pass