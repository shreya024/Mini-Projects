from collections.abc import Mapping

# -----------------------
# NodeView
# -----------------------
class NodeView:
    """Dynamic view of graph nodes.

    Provides iteration, membership testing, and attribute access.

    Examples:
        >>> graph = Graph()
        >>> graph.add_node(1, name='A')  # __init__ via Graph
        >>> list(graph.nodes)  # __iter__
        [1]
        >>> len(graph.nodes)  # __len__
        1
        >>> 1 in graph.nodes  # __contains__
        True
        >>> graph.nodes[1]  # __getitem__
        {'name': 'A'}
        >>> repr(graph.nodes)  # __repr__
        '[1]'
    """
    def __init__(self, graph):
        # Initialize NodeView with a graph
        self._graph = graph

    def __iter__(self):
        # Iterate over nodes
        return iter(self._graph._adj)

    def __len__(self):
        # Return number of nodes
        return len(self._graph._adj)

    def __contains__(self, n):
        # Check if node exists
        return n in self._graph._adj

    def __getitem__(self, n):
        # Return attribute dict for node n
        return self._graph._node[n]

    def __repr__(self):
        # String representation of nodes
        return repr(list(self))


# -----------------------
# EdgeView
# -----------------------
class EdgeView:
    """Dynamic view of graph edges.

    Provides iteration, membership testing, and supports len().

    Examples:
        >>> graph = Graph()
        >>> graph.add_edge(1, 2, weight=5)  # __init__ via Graph
        >>> list(graph.edges)  # __iter__
        [(1, 2)]
        >>> len(graph.edges)  # __len__
        1
        >>> (1, 2) in graph.edges  # __contains__
        True
        >>> (2, 1) in graph.edges
        False
        >>> repr(graph.edges)  # __repr__
        '[(1, 2)]'
    """
    def __init__(self, graph):
        # Initialize EdgeView with a graph
        self._graph = graph

    def __iter__(self):
        # Iterate over edges as (u, v)
        for u in self._graph._adj:
            for v in self._graph._adj[u]:
                yield (u, v)

    def __len__(self):
        # Return number of edges
        return sum(len(self._graph._adj[u]) for u in self._graph._adj)

    def __contains__(self, edge):
        # Check if edge exists
        u, v = edge
        return u in self._graph._adj and v in self._graph._adj[u]

    def __repr__(self):
        # String representation of edges
        return repr(list(self))


# -----------------------
# AdjacencyView
# -----------------------
class AdjacencyView(Mapping):
    """Read-only view of the adjacency structure.

    Examples:
        >>> graph = Graph()
        >>> graph.add_edge(1, 2, weight=3)  # __init__ via Graph
        >>> graph.add_edge(2, 3, weight=5)
        >>> graph.adj[1]  # __getitem__
        {2: {'weight': 3}}
        >>> list(graph.adj)  # __iter__
        [1, 2, 3]
        >>> len(graph.adj)  # __len__
        3
        >>> repr(graph.adj)  # __repr__
        "AdjacencyView({1: {2: {'weight': 3}}, 2: {3: {'weight': 5}}})"
    """
    __slots__ = ("_adj",)

    def __init__(self, adj):
        # Initialize AdjacencyView with adjacency dict
        self._adj = adj

    def __getitem__(self, u):
        # Return neighbors of node u
        return self._adj[u]

    def __iter__(self):
        # Iterate over nodes
        return iter(self._adj)

    def __len__(self):
        # Return number of nodes
        return len(self._adj)

    def __repr__(self):
        # String representation of adjacency mapping
        return f"{self.__class__.__name__}({dict(self._adj)})"


# -----------------------
# Graph
# -----------------------
class Graph:
    """Directed graph with nodes, edges, and adjacency views."""

    def __init__(self):
        self._adj = {}  # successors: u -> {v: attrs}
        self._pred = {}  # predecessors: v -> {u: attrs}
        self._node = {}  # node attribute dict
        self.nodes = NodeView(self)
        self.edges = EdgeView(self)
        self.adj = AdjacencyView(self._adj)

    # -----------------------
    # Node Operations
    # -----------------------
    def add_node(self, n, **attr):
        """
        Add a node with optional attributes.

        Args:
            n: Node identifier.
            **attr: Arbitrary keyword attributes for the node.

        Returns:
            None

        Examples:
            >>> graph = Graph()
            >>> graph.add_node(1, name='A')
            >>> graph.nodes[1]['name']
            'A'
        """
        if n not in self._adj:
            self._adj[n] = {}
            self._pred[n] = {}
            self._node[n] = {}
        self._node[n].update(attr)

    def remove_node(self, n):
        """
        Remove a node and all its incident edges.

        Args:
            n: Node identifier to remove.

        Returns:
            None

        Raises:
            KeyError: If the node n is not in the graph.

        Examples:
            >>> graph = Graph()
            >>> graph.add_node(1)
            >>> graph.remove_node(1)
            >>> graph.has_node(1)
            False
        """
        if n not in self._adj:
            raise KeyError(f"Node {n} not in graph")

        for v in list(self._adj[n]):
            del self._pred[v][n]
        for u in list(self._pred[n]):
            del self._adj[u][n]

        del self._adj[n]
        del self._pred[n]
        del self._node[n]

    def __getitem__(self, u):
        """
        Return the adjacency dictionary for a node.

        Args:
            u: Node identifier.

        Returns:
            dict: Dictionary mapping neighbor nodes to edge attribute dicts.

        Raises:
            KeyError: If the node u is not in the graph.

        Examples:
            >>> graph = Graph()
            >>> graph.add_edge(1, 2, weight=5)
            >>> graph[1]
            {2: {'weight': 5}}
        """
        return self._adj[u]

    # -----------------------
    # Edge Operations
    # -----------------------
    def add_edge(self, u, v, **attr):
        """
        Add a directed edge u → v with optional attributes.

        Args:
            u: Source node.
            v: Target node.
            **attr: Arbitrary keyword attributes for the edge.

        Returns:
            None

        Examples:
            >>> graph = Graph()
            >>> graph.add_edge(1, 2, weight=5)
            >>> graph[1][2]
            {'weight': 5}
        """
        if u not in self._adj:
            self.add_node(u)
        if v not in self._adj:
            self.add_node(v)

        self._adj[u][v] = attr
        self._pred[v][u] = attr

    def remove_edge(self, u, v):
        """
        Remove a directed edge u → v.

        Args:
            u: Source node.
            v: Target node.

        Returns:
            None

        Raises:
            KeyError: If the edge (u, v) does not exist.

        Examples:
            >>> graph = Graph()
            >>> graph.add_edge(1, 2)
            >>> graph.remove_edge(1, 2)
            >>> graph.has_edge(1, 2)
            False
        """
        try:
            del self._adj[u][v]
            del self._pred[v][u]
        except KeyError:
            raise KeyError(f"Edge ({u}, {v}) not in graph")


    # -----------------------
    # Queries
    # -----------------------
    def has_node(self, n):
        """
        Check if a node exists in the graph.

        Args:
            n: The node identifier to check.

        Returns:
            bool: True if the node exists, False otherwise.

        Examples:
            >>> graph = Graph()
            >>> graph.add_node(3)
            >>> graph.has_node(3)
            True
            >>> graph.has_node(4)
            False
        """
        return n in self._adj

    def has_edge(self, u, v):
        """
        Check if an edge exists from node u to node v.

        Args:
            u: The source node.
            v: The target node.

        Returns:
            bool: True if the edge (u, v) exists, False otherwise.

        Examples:
            >>> graph = Graph()
            >>> graph.add_edge(1, 2)
            >>> graph.has_edge(1, 2)
            True
            >>> graph.has_edge(2, 1)
            False
        """
        return u in self._adj and v in self._adj[u]

    def successors(self, n):
        """
        Return an iterator over the successors of a node.

        Args:
            n: The node whose successors are requested.

        Returns:
            iterator: An iterator over successor nodes.

        Raises:
            KeyError: If the node n is not in the graph.

        Examples:
            >>> graph = Graph()
            >>> graph.add_edge(1, 2)
            >>> list(graph.successors(1))
            [2]
        """
        if n not in self._adj:
            raise KeyError(f"Node {n} not in graph")
        return iter(self._adj[n])

    def predecessors(self, n):
        """
        Return an iterator over the predecessors of a node.

        Args:
            n: The node whose predecessors are requested.

        Returns:
            iterator: An iterator over predecessor nodes.

        Raises:
            KeyError: If the node n is not in the graph.

        Examples:
            >>> graph = Graph()
            >>> graph.add_edge(1, 2)
            >>> list(graph.predecessors(2))
            [1]
        """
        if n not in self._pred:
            raise KeyError(f"Node {n} not in graph")
        return iter(self._pred[n])

    # -----------------------
    # Degree Functions
    # -----------------------
    def out_degree(self, n):
        """
        Return the out-degree of a node (number of outgoing edges).

        Args:
            n: The node whose out-degree is requested.

        Returns:
            int: The number of outgoing edges.

        Raises:
            KeyError: If the node n is not in the graph.

        Examples:
            >>> graph = Graph()
            >>> graph.add_edge(1, 2)
            >>> graph.add_edge(1, 3)
            >>> graph.out_degree(1)
            2
        """
        if n not in self._adj:
            raise KeyError(f"Node {n} not in graph")
        return len(self._adj[n])

    def in_degree(self, n):
        """
        Return the in-degree of a node (number of incoming edges).

        Args:
            n: The node whose in-degree is requested.

        Returns:
            int: The number of incoming edges.

        Raises:
            KeyError: If the node n is not in the graph.

        Examples:
            >>> graph = Graph()
            >>> graph.add_edge(1, 2)
            >>> graph.add_edge(3, 2)
            >>> graph.in_degree(2)
            2
        """
        if n not in self._pred:
            raise KeyError(f"Node {n} not in graph")
        return len(self._pred[n])

    def degree(self, n):
        """
        Return the total degree of a node (in-degree + out-degree).

        Args:
            n: The node whose total degree is requested.

        Returns:
            int: The sum of the in-degree and out-degree.

        Raises:
            KeyError: If the node n is not in the graph.

        Examples:
            >>> graph = Graph()
            >>> graph.add_edge(1, 2)
            >>> graph.add_edge(3, 2)
            >>> graph.degree(2)
            2
            >>> graph.degree(1)
            1
        """
        return self.in_degree(n) + self.out_degree(n)

    # -----------------------
    # Edge Iterators
    # -----------------------
    def out_edges(self, n):
        """
        Return all outgoing edges from a node.

        Args:
            n: The source node.

        Returns:
            list[tuple]: A list of edges in the form `(n, v)` for each successor `v`.

        Raises:
            KeyError: If the node n is not in the graph.

        Examples:
            >>> graph = Graph()
            >>> graph.add_edge(1, 2)
            >>> graph.add_edge(1, 3)
            >>> graph.out_edges(1)
            [(1, 2), (1, 3)]
        """
        if n not in self._adj:
            raise KeyError(f"Node {n} not in graph")
        return [(n, v) for v in self._adj[n]]

    def in_edges(self, n):
        """
        Return all incoming edges to a node.

        Args:
            n: The target node.

        Returns:
            list[tuple]: A list of edges in the form `(u, n)` for each predecessor `u`.

        Raises:
            KeyError: If the node n is not in the graph.

        Examples:
            >>> graph = Graph()
            >>> graph.add_edge(1, 2)
            >>> graph.add_edge(3, 2)
            >>> graph.in_edges(2)
            [(1, 2), (3, 2)]
        """
        if n not in self._pred:
            raise KeyError(f"Node {n} not in graph")
        return [(u, n) for u in self._pred[n]]


