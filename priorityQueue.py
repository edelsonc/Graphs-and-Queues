#!/usr/bin/python
"""
A simple priority queue for use with Dijkstra's algorithm.

author: edelsonc
created: 10/09/2016
"""

class BinaryHeap(object):
    """
    Implements a binary heap as a priority que for use in graphing algorithms.
    This heap design uses the base unit of a vertex tuple, which is composed of
    three elements:

    (distance, "name")

    Methods
    ------
    percUp -- helper function for tree order. Moves small items up.
    insert -- inserts new vertex into tree
    percDown -- helper function for tree order. Moves large items down.
    minChild -- returns the min child of a branch
    delMin -- pops the min vertex off the tree
    buildHeap -- contructs a heap from a list
    isEmpty -- returns boolean for whether the heap contains entries
    editHeap -- updates an entry with a new version, searches by name
    display -- returns a vertex. Search is by name    
    """

    def __init__(self):
        """
        Initializes the BinaryHeap with a heapList and a size. The heapList has
        a single entry, a tuple of (0, "0"). This is used as the pase of the
        heap for integer division purposes. Additionally, this is selected as
        it is the form that will be used with a graph algorithm, where the
        positions are (distance, "name").
        
        >>> heap = BinaryHeap()
        >>> print(heap.heapList)
        [(0, '0')]
        >>> print(heap.currentSize)
        0
        """
        self.heapList = [(0, "0")]
        self.currentSize = 0

    def percUp(self, i):
        """
        Helper function that maintains heap order during insertions. Working by
        making sure that no child is less than a parent, and then for any case
        where a child is less, moving them up the tree.
        """
        while i // 2 > 0:
            if self.heapList[i] < self.heapList[i//2]:
                self.heapList[i//2], self.heapList[i] = self.heapList[i], \
                self.heapList[i//2]
            i = i // 2

    def insert(self, k):
        """
        Inserts an item into the aray. In this case the items are tuples which
        represent a vertex in a graph. The helper function percUp is used to
        maintain heap order.
        
        >>> heap = BinaryHeap()
        >>> heap.insert((10, "a"))
        >>> heap.insert((2, "b"))
        >>> heap.insert((6, "c"))
        >>> print(heap.heapList)
        [(0, '0'), (2, 'b'), (10, 'a'), (6, 'c')]
        
        """
        self.heapList.append(k)
        self.currentSize += 1
        self.percUp(self.currentSize)

    def percDown(self, i):
        """
        Helper function used in the minChild, delMin, and buildHeap methods.
        Used to move an item down a list if it is greater than any child item.
        """
        while (i * 2) <= self.currentSize:
            mc = self.minChild(i)
            if self.heapList[i] > self.heapList[mc]:
                self.heapList[i], self.heapList[mc] = self.heapList[mc], \
                self.heapList[i]
            i = mc

    def minChild(self, i=1):
        """
        Returns the index of the minimum child. For graph tuples, this would be
        the tuple with the smallest distance.
        
        >>> heap = BinaryHeap()
        >>> heap.insert((7, "a"))
        >>> heap.insert((4, "c"))
        >>> heap.insert((9, "f"))
        >>> print(heap.heapList)
        [(0, '0'), (4, 'c'), (7, 'a'), (9, 'f')]
        >>> print(heap.minChild())
        2
        """
        if i * 2 + 1 > self.currentSize:
            return i * 2
        else:
            if self.heapList[i*2] < self.heapList[i*2+1]:
                return i * 2
            else:
                return i * 2 + 1

    def delMin(self):
        """
        Pops the first item off of the heap (the minimum item) and re-orders
        the tree to maintain structure and heap order.
        
        >>> heap = BinaryHeap()
        >>> heap.insert((3, 'g'))
        >>> heap.insert((2, 'a'))
        >>> heap.insert((4, 'r'))
        >>> print(heap.heapList)
        [(0, '0'), (2, 'a'), (3, 'g'), (4, 'r')]
        >>> print(heap.delMin())
        (2, 'a')
        >>> print(heap.heapList)
        [(0, '0'), (3, 'g'), (4, 'r')]
        """
        retval = self.heapList[1]
        self.heapList[1] = self.heapList[self.currentSize]
        self.currentSize -= 1
        self.heapList.pop()
        self.percDown(1)
        return retval

    def buildHeap(self, alist):
        """
        Builds a heap from a list. For the graph the list should be a list of
        tuples. Each tuple should be as follows:

        (distance, "name")

        where distance is either the Euclidean distance or another distance
        derived from the X and Y position of the vertex and the name is the letter name of the vertex.
        
        >>> vertex_list = [(1, "a"), (4, "b"), (2, "d")]
        >>> heap = BinaryHeap()
        >>> heap.buildHeap(vertex_list)
        >>> print(heap.heapList)
        [(0, '0'), (1, 'a'), (4, 'b'), (2, 'd')]
        """
        i = len(alist) // 2
        self.currentSize = len(alist)
        self.heapList = [(0, '0')] + alist[:]
        while (i > 0):
            self.percDown(i)
            i -= 1

    def isEmpty(self):
        """
        Checks if heap is empty and returns boolean. Simply checks if list only
        has init value.
        
        >>> heap = BinaryHeap()
        >>> print(heap.isEmpty())
        True
        >>> heap.insert((2, 'a'))
        >>> print(heap.isEmpty())
        False
        """
        if self.heapList == [(0, '0')]:
            return True
        else:
            return False

    def editHeap(self, name, update):
        """
        Updates a current tuple. Necessary for the graph algorithms
        
        >>> heap = BinaryHeap()
        >>> heap.insert((2, 'a'))
        >>> print(heap.heapList)
        [(0, '0'), (2, 'a')]
        >>> heap.editHeap('a', (2, 'b'))
        >>> print(heap.heapList)
        [(0, '0'), (2, 'b')]
        """
        for i, tuple in enumerate(self.heapList):
            if tuple[1] == name:
                del self.heapList[i]
                self.currentSize -= 1
                self.insert(update)
                return
        # insert it if the name wasn't already in the list
        self.insert(update)

    def display(self, name):
        """
        Find a vertex by name in the heap and display it. For looking at
        content of a particular vertex.

        >>> heap = BinaryHeap()
        >>> heap.insert((2, 'a'))
        >>> heap.display('a')
        (2, 'a')
        """
        for i, tuple in enumerate(self.heapList):
            if tuple[1] == name:
                return tuple

    def __contains__(self, item):
        """
        Overloading the in operator in python in order to check if a name
        appears in the heap.

        >>> heap = BinaryHeap()
        >>> heap.insert((1, 'a'))
        >>> 'a' in heap
        True
        >>> 'k' in heap
        False
        """
        return any([ item in tuple for tuple in self.heapList ])

if __name__ == '__main__':
    import doctest
    doctest.testmod()