#!/usr/bin/python
"""
Implementation of a graph class and a shortest path algorithm.

author: edelsonc
created: 10/08/2016
"""
import priorityQueue as pQ


class Graph(object):
    """
    A simple implementation of a directed unweighted graph
    """
    def __init__(self):
        """
        Initializes an empty graph object

        Create New Graph
        ----------------
        >>> graph = Graph()
        >>> graph.vertexList
        []
        >>> graph.connections
        {}
        """
        self.vertexList = []
        self.connections = {}

    def addVertex(self, vertex):
        """
        Adds a vertex to the graph object. Makes sure that the vertex is not
        already a part of the graph

        Arguments
        ---------
        vertex -- new graph vertex

        Adding New Vertex
        -----------------
        >>> graph = Graph()
        >>> graph.addVertex("A")
        >>> graph.vertexList
        ['A']
        >>> graph.connections
        {'A': []}

        Adding Pre-existing Vertex
        --------------------------
        >>> graph.addVertex("A")
        >>> graph.vertexList
        ['A']
        """
        if vertex in self.vertexList:
            return

        self.vertexList.append(vertex)
        self.connections[vertex] = []

    def addConn(self, v1, v2):
        """
        Adds a connection (edge) to the graph, making sure that both vertices
        are in the graph. If a vertex isn't in the graph, it is added first.

        Arguments
        ---------
        v1, v2 -- vertices connected via an edge; edge goes from v1 -> v2

        Adding Connection for Two Existing Vertices
        -------------------------------------------
        >>> graph = Graph()
        >>> graph.addVertex("A")
        >>> graph.addVertex("B")
        >>> graph.addConn("A", "B")
        >>> graph.connections['B']
        []

        Adding Edge for One Missing Vertex
        ----------------------------------
        >>> graph.addConn("A", "C")
        >>> graph.vertexList
        ['A', 'B', 'C']
        >>> graph.connections['A']
        ['B', 'C']
        """
        if v1 not in self.vertexList:
            self.addVertex(v1)
        if v2 not in self.vertexList:
            self.addVertex(v2)

        if v2 in self.connections[v1]:
            return

        self.connections[v1].append(v2)

    def hasVert(self, vert):
        """
        Checks if a vertex is in the graph vertex list. Returns a boolean.

        Arguments
        ---------
        vert -- vertex that is checked for in graph

        Check Inserted Vertex
        ---------------------
        >>> graph = Graph()
        >>> graph.addVertex("A")
        >>> graph.hasVert("A")
        True

        Check Missing Vertex
        --------------------
        >>> graph.hasVert("K")
        False
        """
        return vert in self.vertexList

    def getConns(self, vert):
        """
        Lists all the connection of a given vertex as a list. Returns None if
        the vertex is not in the list

        Arguments
        ---------
        vert -- vertex whose connections are returned

        List Connections
        ----------------
        >>> graph = Graph()
        >>> graph.addVertex("A")
        >>> graph.addConn("A", "B")
        >>> graph.addConn("A", "C")
        >>> graph.addConn("B", "C")
        >>> graph.getConns("A")
        ['B', 'C']
        >>> graph.getConns("B")
        ['C']
        >>> graph.getConns("C")
        []

        Connections of Vertex Not in Graph
        ----------------------------------
        >>> graph.getConns("K")
        """
        if not self.hasVert(vert):
            return

        return self.connections[vert]

    def getNodes(self):
        """
        Returns all the nodes in the graph object.

        Get List of All Nodes
        ---------------------
        >>> graph = Graph()
        >>> for vert in ['A', 'B', 'C', 'F']:
        ...     graph.addVertex(vert)
        >>> graph.getNodes()
        ['A', 'B', 'C', 'F']
        """
        return self.vertexList

    def __iter__(self):
        """
        Allows the user to iterate over the keys of the graph (vertexList)
        
        Use with For Loops
        ------------------
        >>> graph = Graph()
        >>> vertices = ["A", "B", "C"]
        >>> for vert in vertices:
        ...     graph.addVertex(vert)
        >>> for vert in graph:
        ...     print(vert)
        A
        B
        C
        """
        return iter(self.vertexList)


def find_shortest_path(graph, start, end, path=[]):
    """
    Recursive search for shortest path in a directed unweighted graph. Returns
    the actual path connecting the start and end. For the path lenght, just
    take the len() of the return.

    Arguments
    ---------
    graph -- object of the Graph class
    start -- starting vertex; must be in graph
    end -- ending vertex; must be in graph
    path -- starting path; defaults to empty list

    Shortest Path for Existing Vertices
    -----------------------------------
    >>> graph = Graph()
    >>> graph.addVertex("A")
    >>> conns = [ ("A", "B"), ("A", "C"), ("B", "C"), ("C", "D") ]
    >>> for va, vb in conns:
    ...     graph.addConn(va, vb)
    >>> find_shortest_path(graph, "A", "D")
    ['A', 'C', 'D']
    >>> graph.addConn("A", "D")
    >>> find_shortest_path(graph, "A", "D")
    ['A', 'D']

    Shortest Path Missing Vertex
    ----------------------------
    >>> find_shortest_path(graph, "A", "K")
    """
    path = path + [start]

    if start == end:
        return path

    if not graph.hasVert(start) or not graph.hasVert(end):
        return None

    shortest = None

    for node in graph.getConns(start):
        if node not in path:
            newpath = find_shortest_path(graph, node, end, path)

            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath

    return shortest


def Dijkstra(graph, source):
    """
    Dijkstra's algorithm for shortest path between two vertices on a graph.

    Arguments
    ---------
    graph -- directed graph; object of Graph class
    source -- start vertex

    >>> graph = Graph()
    >>> graph.addVertex("A")
    >>> conns = [ ("A", "B"), ("A", "C"), ("B", "C"), ("C", "D") ]
    >>> for va, vb in conns:
    ...     graph.addConn(va, vb)    
    >>> dists = Dijkstra(graph, 'A')
    >>> dists['D']
    2
    """
    dist = {}
    pq = pQ.BinaryHeap()
    for node in graph:
        if node != source:
            dist[node] = float('inf')
        else:
            dist[node] = 0

        pq.insert((dist[node], node))
    
    while not pq.isEmpty():
        current = pq.delMin()
        for next_node in graph.getConns(current[1]):
            new_dist = current[0] + 1
            if new_dist < dist[next_node]:
                dist[next_node] = new_dist
                pq.editHeap(next_node, (dist[next_node], next_node))
                
    return dist


def check_cycles(graph):
    """
    Checks graph object for a cycle. Algorithm adapted from:
    http://codereview.stackexchange.com/questions/86021/check-if-a-directed-graph-contains-a-cycle

    Arguments
    ---------
    graph -- an object of the Graph class
    start -- a vertex in graph

    Cycle Present
    -------------
    >>> graph = Graph()
    >>> graph.addConn('A', 'B')
    >>> graph.addConn('B', 'A')
    >>> check_cycles(graph)
    True

    No Cycle Present
    ----------------
    >>> graph = Graph()
    >>> graph.addConn('A', 'B')
    >>> graph.addConn('A', 'C')
    >>> check_cycles(graph)
    False
    """
    path = set()
    visited = set()

    return any(visit(vert, path, visited, graph) for vert in graph)


def visit(vertex, visited, path, graph):
    """
    Fuction that is part of check_cycle. Acts to iterare through the path for
    a single vertex, and find if it ever repeats. If it does, it returns True.
    Otherwise, it will return Flase.

    Arguments
    ---------
    vertex -- vertex whose children will be searched
    visited, path -- sets created in the check_cycle function
    graph -- graph being checked for a cycle
    """
    if vertex in visited:
        return False
    visited.add(vertex)
    path.add(vertex)
    for neighbour in graph.getConns(vertex):
        if neighbour in path or visit(neighbour, visited, path, graph):
            return True
    path.remove(vertex)
    return False

if __name__ == '__main__':
    import doctest
    doctest.testmod()