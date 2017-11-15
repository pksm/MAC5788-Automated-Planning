import heapq
import inspect
import sys


"""
 Data structures useful for implementing Best-First Search
"""
class Stack:
    "A container with a last-in-first-out (LIFO) queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "Push 'item' onto the stack"
        self.list.append(item)

    def pop(self):
        "Pop the most recently pushed item from the stack"
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the stack is empty"
        return len(self.list) == 0

class Queue:
    "A container with a first-in-first-out (FIFO) queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "Enqueue the 'item' into the queue"
        self.list.insert(0,item)

    def pop(self):
        """
          Dequeue the earliest enqueued item still in the queue. This
          operation removes the item from the queue.
        """
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the queue is empty"
        return len(self.list) == 0

class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def __init__(self):
        self.heap = []
        self.count = 0

    def __contains__(self, item):
        for (_, _, i) in self.heap:
            if i == item:
                return True
        return False

    def __len__(self):
        return len(self.heap)

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)

    def __str__(self):
        return str([(p, str(item)) for (p, _, item) in self.heap])


    def __getitem__(self, key):
        for _, _, item in self.heap:
            if item == key:
                return item

    def __delitem__(self, key):
        for i, (value, item) in enumerate(self.heap):
            if item == key:
                self.heap.pop(i)


# class PriorityQueueWithFunction(PriorityQueue):
#     """
#     Implements a priority queue with the same push/pop signature of the
#     Queue and the Stack classes. This is designed for drop-in replacement for
#     those two classes. The caller has to provide a priority function, which
#     extracts each item's priority.
#     """
#     def __init__(self, priorityFunction):
#         "priorityFunction (item) -> priority"
#         self.priorityFunction = priorityFunction      # store the priority function
#         PriorityQueue.__init__(self)        # super-class initializer

#     def push(self, item):
#         "Adds an item to the queue with priority from the priority function"
#         PriorityQueue.push(self, item, self.priorityFunction(item))


# def raiseNotDefined():
#     fileName = inspect.stack()[1][1]
#     line = inspect.stack()[1][2]
#     method = inspect.stack()[1][3]
#     print("*** Method not implemented: `%s` at line %s of %s" % (method, line, fileName))
#     sys.exit(1)
