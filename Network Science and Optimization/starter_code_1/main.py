import netopt as no
import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
import pyproj
import time

def no2nx(graph):
    """
    Convert a custom directed graph into a NetworkX DiGraph.

    This function creates a new `networkx.DiGraph` and copies all nodes and
    edges, including their attribute dictionaries.

    Args:
        graph (object): A graph-like object exposing node and edge interfaces
            compatible with NetworkX-style access. Must provide:
            - `graph.nodes` (iterable of node IDs)
            - `graph.nodes[n]` (node attribute dict)
            - `graph.adj[u][v]` (edge attribute dict)

    Returns:
        networkx.DiGraph: A directed NetworkX graph containing all nodes and
        edges from `graph`, with node and edge attributes preserved.

    Raises:
        TypeError: If `graph` does not have the required `nodes` or `adj` attributes.
    """

    G = nx.DiGraph()

    # Copy nodes
    for u in graph.nodes:
        G.add_node(u, **graph.nodes[u])

    # Copy edges
    for u in graph.nodes:
        for v, attr in graph.adj[u].items():
            G.add_edge(u, v, **attr)

    return G


def nx2no(G):
    """
    Convert a NetworkX DiGraph into a custom directed graph.

    This function creates a new `netopt.Graph` and copies all nodes and
    edges, including their attribute dictionaries.

    Args:
        G (networkx.DiGraph): A directed NetworkX graph.

    Returns:
        netopt.Graph: A directed graph containing all nodes and edges from `G`,
        with node and edge attributes preserved.
    """

    graph = no.Graph()

    # Copy nodes
    for u in G.nodes:
        graph.add_node(u, **G.nodes[u])

    # Copy edges
    for u, v, attr in G.edges(data=True):
        graph.add_edge(u, v, **attr)

    return graph


def visualize_traversal(G, is_reachable, predecessor, order, traversed_edges,
                        title="Traversal Visualization"):
    """
    Visualize the traversal of a graph using Matplotlib.
    Args:
        G (networkx.DiGraph): The graph to visualize.
        is_reachable (dict): A dictionary mapping node IDs to boolean values
            indicating if the node was reached during traversal.
        predecessor (dict): A dictionary mapping node IDs to their predecessor
            in the traversal.
        order (dict): A dictionary mapping node IDs to their order of
            visitation.
        traversed_edges (list): A list of edges (tuples) that were traversed
            during the traversal.
        title (str): The title for the visualization plot.

    Returns:
        None
    """
    pos = nx.get_node_attributes(G, 'pos')
    node_colors = ['lightblue' if is_reachable[n] else 'white' for n in
                   G.nodes]
    labels = {n: f"{n}\n[order: {order[n]}]\n[predecessor: {predecessor[n]}]"
              for n in G.nodes}

    edge_color = ['gray' for _ in G.edges]
    for u, v in traversed_edges:
        edge_color[list(G.edges).index((u, v))] = 'red'

    nx.draw_networkx(G, pos, labels=labels, node_color=node_colors,
                     edge_color=edge_color)

    plt.title(f"{title}")
    plt.axis("off")
    plt.savefig(f"{title}.png")
    plt.show()


def download_osmnx_network():
    """
    Download a street network from OpenStreetMap using OSMnx.

    Args:
        None

    Returns:
        networkx.MultiDiGraph: The downloaded street network graph.
    """
    # Example: Download a street network with a fixed bounding box
    place_name = "Bangalore, Karnataka, India"
    G = ox.graph_from_point((12.9629, 77.5775),
                            network_type='drive',
                            simplify=True,
                            dist=16000,
                            retain_all=False,
                            truncate_by_edge=False)

    # Print the number of nodes and edges
    print(f"Number of nodes: {len(G.nodes)}")
    print(f"Number of edges: {len(G.edges)}")

    # Write the edges to a file
    ox.save_graphml(G, filepath="./data/shortest_paths/blr_16000.graphml")

    # Display the graph with white background and black edges
    # fig, ax = ox.plot_graph(G, bgcolor='white', node_size=0,
    #                         edge_color='black', edge_alpha=0.3)

    # plt.show()
    return G


if __name__ == "__main__":
    graph = no.Graph()
    graph.add_node(1, pos=(0, 0))
    graph.add_node(2, pos=(4, -2))
    graph.add_node(3, pos=(4, 2))
    graph.add_node(4, pos=(12, -2))
    graph.add_node(5, pos=(12, 2))
    graph.add_node(6, pos=(16, 0))
    #
    # Add edges between nodes
    graph.add_edge(1, 2, length=6)
    graph.add_edge(1, 3, length=4)
    graph.add_edge(2, 3, length=2)
    graph.add_edge(2, 4, length=2)
    graph.add_edge(3, 4, length=1)
    graph.add_edge(3, 5, length=2)
    graph.add_edge(4, 6, length=7)
    graph.add_edge(5, 4, length=1)
    graph.add_edge(5, 6, length=3)
    
    #G = no2nx(graph)
    #
    # # Plot the graph G using networkx
    # pos = nx.get_node_attributes(G, 'pos')
    # nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray')
    # edge_labels = nx.get_edge_attributes(G, 'weight')
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    # plt.show()
    #
    # is_reachable, predecessor, order, bfs_edges = no.bfs(graph, 1)
    # visualize_traversal(G, is_reachable, predecessor, order, bfs_edges,
    #                     title="BFS_Traversal")
    #
    # is_reachable, predecessor, order, dfs_edges = no.dfs(graph, 4)
    # visualize_traversal(G, is_reachable, predecessor, order, dfs_edges,
    #                     title="DFS_Traversal")

    # Download OSMnx network and perform BFS
    # G = download_osmnx_network()
    # G = ox.load_graphml("./data/traversal/blr_16000.graphml")
    # graph = nx2no(G)
    # start_time = time.time()
    # is_reachable, predecessor, order, bfs_edges = no.bfs(graph,
    #                                                      list(graph.nodes)[0])
    # end_time = time.time()
    # print("BFS Time taken: ", end_time - start_time)
    # node_colors = ["lightblue" if is_reachable[n] else "red" for n in
    #                graph.nodes]
    # node_sizes = [0 if is_reachable[n] else 20 for n in graph.nodes]

    # # Visualize the graph using osmnx functions
    # G = nx.MultiDiGraph(no2nx(graph))
    # G.graph["crs"] = pyproj.CRS("EPSG:4326")
    # fig, ax = ox.plot_graph(G, node_color=node_colors,
    #                         bgcolor='white',
    #                         node_size=node_sizes,
    #                         edge_color='black',
    #                         edge_alpha=0.3,
    #                         save=True,
    #                         filepath="BFS_Traversal_OSMnx.png")

    #G = download_osmnx_network()
    G = ox.load_graphml("./data/shortest_paths/blr_1000.graphml")
    graph = nx2no(G)
    dist=no.reverse_dijkstra(graph,list(graph.nodes)[0])
    #dist=no.reverse_dijkstra(graph,6)
    avgSum=0
    count=0
    for d in dist:
        if dist[d]!=float('inf'):
            avgSum+=dist[d]
            count+=1
    print(count,avgSum/count)

