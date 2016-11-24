#!/Users/edelsonc/miniconda3/bin/python
"""
An implementation of a simple python queue object. Created for use in
Stochastic Gradient Descent Method for NCF graduate program.

author: edelsonc
created: 11/23/2016
"""

class SimpleQueue(object):
    """
    Implementation of a simple queue in python. Queue is fixed at a maximum
    length specified upon instantiation.

    Methods
    -------
    append -- appends a new item to the queue
    dequeue -- removes and returns the first item off of the queue
    listAppend -- appends the items of a list to the queue
    """

    def __init__(self, maxlen):
        """
        Creates a queue object

        Arguments
        ---------
        maxlen -- maximum length of the queue

        >>> sq = SimpleQueue(3)
        >>> sq.maxlen
        3
        >>> sq.list
        []
        """
        self.maxlen = maxlen
        self.list = []

    def append(self, item):
        """
        Appends an object to the queue

        Arguments
        ---------
        item -- the object to be appended to the queue

        >>> sq = SimpleQueue(5)
        >>> for i in range(5):
        ...     sq.append(i)
        >>> sq.list
        [0, 1, 2, 3, 4]
        >>> sq.append(33)
        >>> sq.list
        [1, 2, 3, 4, 33]
        """
        self.list.append(item)
        if len(self.list) > self.maxlen:
            self.list.pop(0)


    def dequeue(self):
        """
        Returns the first item off of the queue

        >>> sq = SimpleQueue(5)
        >>> for i in range(5):
        ...     sq.append(i)
        >>> sq.dequeue()
        0
        >>> sq.list
        [1, 2, 3, 4]
        """
        return self.list.pop(0)

    def listAppend(self, alist):
        """
        >>> sq = SimpleQueue(5)
        >>> sq.listAppend([0, 1, 2, 3, 4])
        >>> sq.list
        [0, 1, 2, 3, 4]

        >>> sq.listAppend([5, 6, 7 ,8])
        Traceback (most recent call last):
            ...
        ValueError: List too long for current queue
        """
        if len(alist) + len(self.list) <= self.maxlen:
            for item in alist:
                self.append(item)
        else:
            raise ValueError('List too long for current queue')

    def __iter__(self):
        """
        Allows proper iteration through the queue

        >>> sq = SimpleQueue(5)
        >>> for i in range(5):
        ...     sq.append(i)
        >>> for item in sq:
        ...     print(item)
        0
        1
        2
        3
        4
        """
        return iter(self.list)

    def __getitem__(self, i):
        """
        Allows proper indexing of the queue

        >>> sq = SimpleQueue(5)
        >>> for i in range(5):
        ...     sq.append(i)
        >>> sq[2]
        2
        """
        return self.list.__getitem__(i)

    def __str__(self):
        """
        Allows for printing of the queue object

        >>> sq = SimpleQueue(5)
        >>> for i in range(5):
        ...     sq.append(i)
        >>> print(sq)
        Current Queue: [0, 1, 2, 3, 4]
        """
        return "Current Queue: {}".format(self.list)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
