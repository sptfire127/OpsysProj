# coding=utf-8
from output import *

"""
Class representation of a process. This isn't going to do much, basically just
a store for meta data and a way to keep track of which process is running. If we
wanted to analyze memory footprints and such we could implement more here and
make the process more interactive.
Attributes: - Label
            - State | • READY: in the ready queue, ready to use the CPU
                    | • RUNNING: actively using the CPU
                    | • BLOCKED: blocked on I/O
                    | • FINISHED: Done executings
                =SHOULD INIT TO READY STATE????=
            - Arrived (Boolean to keep track of arrival conditions)
            - Arrival Time
            - Burst Time Total
            --Burst Time Left
            - Burst Count
            - I/O Time Total
            --I/O Time Left
            --waitTime
            --turnAround
"""


class Process():
    def __init__(self, label, arrival, burst, burstCount, IOtime):
        assert (burst != 0 and burstCount != 0)
        self.label = label
        self.state = "READY"
        self.arrived = False
        self.arrivalTime = arrival
        self.arrivalTimeLeft = self.arrivalTime
        self.burstTime = burst
        self.burstCount = burstCount
        self.executionTime = 0
        self.IOtime = IOtime
        self.burstTimeLeft = self.burstTime
        self.IOtimeLeft = self.IOtime
        self.waitTime = 0
        self.turnAround = 0

    """
    Change state of this process to param=state. Enforces state restrictions
    to the 3 recognized by simulation. Else = RuntimeError is raised
    """

    def stateChange(self, state):
        if not (state == "READY" or state == "RUNNING" or state == "BLOCKED"):
            raise RuntimeError("INVALID STATE CHANGE")
        self.state = state

    # returns whether or not this process is in the ready state
    def isReady(self):
        return self.state == "READY"

    def isArrived(self):
        return self.arrivalTimeLeft <= 0

    # Am I finished?
    def isFinished(self):
        return self.state == "FINISHED"

    # Getter for self.arrivalTime
    def getArrival(self):
        return self.arrivalTime

    """
    This should do arithmitic off the BurstTime, I/O Time
        -> Change self.state based on these times.
    NOTE: THIS IS NOT WHERE PROCESS SHOULD BE CHANGED TO A RUNNING STATE
    """

    def step(self, rTime=None):
        # Determine state and decriment accoringly
        # Only increment wait if proc has started running
        if (self.state == "READY" and self.arrived):
            self.waitTime += 1

        # Proc is waiting to arrive
        elif (self.state == "READY" and not self.arrived):
            if (self.arrivalTimeLeft == 0):
                self.arrived = True
            self.arrivalTimeLeft -= 1


        elif (self.state == "RUNNING"):
            self.executionTime += 1
            self.burstTimeLeft -= 1

        elif (self.state == "BLOCKED"):
            self.IOtimeLeft -= 1

        elif (self.state == "FINISHED"):
            self.turnAround = self.waitTime + (self.executionTime)

        else:
            raise RuntimeError("PROCESS STATE INVALID")

        # More arithmitic
        if (self.burstTimeLeft <= 0 and self.state == "RUNNING"):
            self.burstTimeLeft = self.burstTime
            self.burstCount -= 1

            if (self.burstCount == 0):
                self.state = "FINISHED"

            else:
                self.state = "BLOCKED"
        elif (self.IOtimeLeft <= 0 and self.state == "BLOCKED"):
            self.IOtimeLeft = self.IOtime
            self.state = "READY"

    def __repr__(self):
        return str(vars(self))

    def __str__(self):
        return "Label: {0} | State: {1} (burstTimeLeft: {2} | burstTime: {3} | burstCount: {4}) (IOtimeLeft: {5} | IOtime: {6}) (waitTime : {7} arrivalTime : {8})".format(
            self.label, self.state, self.burstTimeLeft, self.burstTime, self.burstCount, self.IOtimeLeft, self.IOtime,
            self.waitTime, self.arrivalTime)
