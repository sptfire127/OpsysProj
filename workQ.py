import operator
from Process import *

"""
workQ class which uses a list as an underlying implemetation.
Attributes: workQ -- List representing the Queue
"""


class workQ():
    def __init__(self):
        self.queue = []

    def size(self):
        return len(self.queue)

    """
    This should reorganize the workQ based on the algorithm passed in
    """

    def step(self, algorithm):

        # Call right handler
        if (algorithm == "FCFS"):
            return self.__qFCFS()

        elif (algorithm == "SRT"):
            return self.__qSRT()

        elif (algorithm == "RR"):
            return self.__qRR()
        else:
            raise RuntimeError("BAD SCHEDULING ALGORITHM")
            exit()

    def isEmpty(self):
        return len(self.queue) <= 0

    def peak(self):
        return self.queue[0]

    """
    Add process to the workQ tail
    """

    def enqueu(self, proc):
        assert (isinstance(proc, Process))
        self.queue.append(proc)

    """
    Remove head from the Queue
    """

    def dequeue(self):
        return self.queue.pop(0)

    def __repr__(self):
        return str(vars(self))

    ################################################################################
    # DONT SHOULD NOT BE INVOKED DIRECTLY
    ################################################################################
    def __qFCFS(self):
        # ENQUEUE and DEQUEUE already preserve FCFS Nature.. ? #FIXME
        pass

    def __qSRT(self):
        self.queue.sort(key=operator.attrgetter("burstTimeLeft"))

    def __qRR(self):
        # TODO
        pass

        ################################################################################
