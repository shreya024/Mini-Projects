from collections import deque


def bfs(graph, source):
    # Discuss the advantages and disadvantages of writing directly on the graph
    # structure. It is less intuitive but doesn't have to be overwritten and
    # allows for parallelization.

    is_reachable = {node: False for node in graph.nodes}
    predecessor = {node: None for node in graph.nodes}
    order = {node: None for node in graph.nodes}
    bfs_edges = []

    is_reachable[source] = True
    order[source] = 1
    order_counter = 1
    queue = deque([source])

    while queue:
        u = queue.popleft()
        for v in graph.adj[u]:
            if not is_reachable[v]:
                is_reachable[v] = True
                predecessor[v] = u
                order_counter += 1
                order[v] = order_counter
                bfs_edges.append((u, v))
                queue.append(v)

    return is_reachable, predecessor, order, bfs_edges


def dfs(graph, source):
    is_reachable = {node: False for node in graph.nodes}
    predecessor = {node: None for node in graph.nodes}
    order = {node: None for node in graph.nodes}
    dfs_edges = []

    is_reachable[source] = True
    order[source] = 1
    order_counter = 1
    stack = [source]

    iters = {u: iter(graph.adj[u]) for u in graph.nodes}
    print(iters)

    while stack:
        u = stack[-1]
        try:
            v = next(iters[u])
            if not is_reachable[v]:
                is_reachable[v] = True
                predecessor[v] = u
                order_counter += 1
                order[v] = order_counter
                dfs_edges.append((u, v))
                stack.append(v)
        except StopIteration:
            stack.pop()

    return is_reachable, predecessor, order, dfs_edges
