from output import *
from Process import *

"""
    Handle all the wait time logic for doing a context switch
    with respect to waiting processes
"""


class ContextSwitchHandler():
    processor = None

    def __init__(self, processor):
        self.processor = processor


        """
    Should simulate a context switch and provide a way of abstraction

    ASSUMES THE WORKQ IS NOT EMPTY
    """
    def contextSwitch(self):

        #Calculate the new time slice if its RR
        if(self.processor.algorithm == "RR"):
            self.nxtSlice = self.processor.rTime + self.processor.tSlice + self.processor.cSwitchTime

        old = self.processor.cProc      # Assign old proc to this
        factor = None                   # Init this to None, must change or error

        # What kind of switch are we doing?
        if(self.processor.cProc is None):
            # Loading a new process
            factor = 1/2    # We're doing half a cSwitchTime
            time = self.processor.cSwitchTime / 2
        else:
            # Make sure IO does not start right away, stall it for half a context switch
            # self.processor.cProc.IOtimeLeft += self.processor.cSwitchTime / 2
            if(self.processor.cProc.state == "BLOCKED"):
                self.processor.procHelper.logBurst()
                writeOutput("time {0}ms: Process {1} switching out of CPU; will block on I/O until time {2}ms {3}\n".format(
                    int(self.processor.rTime), self.processor.cProc.label,
                    int(self.processor.cProc.IOtimeLeft + (self.processor.rTime) + (self.processor.cSwitchTime / 2)),
                    self.processor.procPrinter.getQStr()), self.processor.cProc.label, evenCPU())

            # potentially doing either first half, or full depending on state of
            # workQ
            factor = 1      # We're doing a full cSwitchTime
            time = self.processor.cSwitchTime


        # Simulate time cycles.
        for i in range(1, int(time) + 1):

            self.processor.incrementrTime()   # Increment time
            self.processor.step_workQ() # step_workQ to ensure workQ is in valid state

            # We swap out processes
            if(i == self.processor.cSwitchTime / 2):
                if not old is None:
                    #old.IOtimeLeft -= self.processor.cSwitchTime / 2 #FIXME
                    if(old.state == "RUNNING"):
                        old.stateChange("READY")
                    self.processor.procPool.append(old)

                # The workQ is empty
                if(self.processor.workQ.isEmpty()):

                    # Half of context switch so if we're just removing a process, where do we add it to the procPool?
                    self.processor.cProc = None
                    break

                # Add new proc to self
                newProc = self.processor.workQ.dequeue()
                newProc.waitTime -= i
                self.processor.cProc = newProc
                self.processor.cProc.stateChange("RUNNING")


        # Increment the context switch counter.
        # Here we have completed the context switch
        if(self.processor.cProc is not None):
            if (self.processor.cProc.burstTimeLeft < self.processor.cProc.burstTime):
                writeOutput(
                    "time {0}ms: Process {1} started using the CPU with {2}ms remaining {3}\n".format(
                        int(self.processor.rTime), self.processor.cProc.label,
                        self.processor.cProc.burstTimeLeft,
                        self.processor.procPrinter.getQStr()), self.processor.rTime, evenCPU())

            else:
                writeOutput("time {0}ms: Process {1} started using the CPU {2}\n".format(self.processor.rTime, self.processor.cProc.label, self.processor.procPrinter.getQStr()), self.processor.cProc.label, evenCPU())

        self.processor.cSwitchAmt += factor
