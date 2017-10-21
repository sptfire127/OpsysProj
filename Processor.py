#printeted# coding=utf-8
from workQ import *
from ProcessorPrinter import *
from ProcessorHelper import *
from ContextSwitchHandler import *
from CPUAlgorithmsHandler import *
from output import *
################################################################################
#   Project control flow should be as follows:
#       1. Create a processor
#       2. Add processes to the procPool (Either randomly in processor.__init__() Or add them manually with a method)
#           a. This involves initializing each processor
#       3. Call step in a loop until procPool and workQ are empty
#
################################################################################

"""
Processor class that simulates the running and mechanics
of running tasks on a processor.
--step() == 1 cpu PROC_CYLCE (idk if this was supposed to be one cycle of one millisecond. I left it as PROC_CYLCE)
    ->  Step should compare self.algorithm to select the correct
        step handler (SEE HANDLERS).
Attributes:
    rTime           -- Running time of the processor
    cSwitchTime     -- Context switch time overhead
    cSwitchAmt      -- Running amount of context switches
    workQ           -- Processor work Queue / ready Queue (Which is basically a stack with extra functionality)
    procPool        -- Total pool of all processors in scope
    algorithm       -- Selected scheduling algorithm
    cProc           -- Current running process (Used for logging / debugging)
    totalBurst      -- running total of burst times
    totalBurstCount -- Number of total CPU bursts
    startBurst      -- value used to keep track of the start of a cpu burst
    nBurst          -- number of total bursts
    donePool        -- pool of finished processes
    avgWait         -- average wait time
    avgTurnAround   -- average turn around time
    tSlice          -- time slice for round robin algorithm
    nxtSlice        -- Next time to pre-empt process
"""
class Processor():

    """
    Initializer for processor class
    """
    def __init__(self, cSwitchTime, algorithm, tSlice=None):
        self.rTime = 0
        self.cSwitchTime = cSwitchTime
        self.cSwitchAmt = 0.0
        self.workQ = workQ()
        self.totalBurstCount = 0
        self.totalBurst = 0
        self.procPool = []
        self.algorithm = algorithm
        self.cProc = None
        self.startBurst = 0
        self.nBurst = 0
        self.donePool = []
        self.avgWait = 0
        self.avgTurnAround = 0
        self.procPrinter = ProcessorPrinter(self)
        self.procHelper = ProcessorHelper(processor=self)
        self.cSwitcher = ContextSwitchHandler(processor=self)
        self.cpuAlgoHandler = CPUAlgorithmsHandler(processor=self)
        self.tSlice = tSlice
        if(not (tSlice is None)):
            #Init next time slice
            self.nxtSlice = self.rTime + self.tSlice + (self.cSwitchTime / 2)
        else:
            self.nxtSlice = None

    """
    Simulates one processor PROC_CYLCE in PROCESSOR
        This should entail ::=> - Log any processor state statistics if needed
                                - __step_workQ()
                                - Call correct scheduling handler
                                - Detect any errors in PROC_CYLCE
    """
    def step(self):
        #LOG SHIT HERE TODO

        #If proc is not none, step it. If it is none, will be handled in handler
        if(not (self.cProc is None)):
            self.cProc.step()

        #Step the worQ
        self.step_workQ()

        self.cpuAlgoHandler.handle_FCFS()

        #Increment running time
        self.incrementrTime()


    """
    Increment the processor counter
    """
    def incrementrTime(self):
        self.rTime += 1
        writeOutput() #Flush

    """
    This should cylce through all processors in the self.procPool and move any READY
    processors into the workQ and remove any !READY processors into procPool
    Then organize the workQ so the next processor is in front of the workQ
    based on the selected scheduling algorithm.
    I decided to do this in a seperate
    method to prevent bloating the scheduling methods.
    """
    def step_workQ(self):

        rLst = []
        #Step every process in the procPool and handle adding / removing from workQ
        for p in self.procPool:
            p.step(self.rTime)

            # Has the process arrived and is it ready?
            if ((p.getArrival() <= self.rTime) and (p.isReady())):
                # Add this to the workQ and remove it from procPool later
                self.workQ.enqueu(p)
                rLst.append(p)

                if(p.arrivalTimeLeft == -25): #Aritrary constant

                    if(not(self.cProc is None) and self.procHelper.procReady() and self.algorithm != "FCFS"):
                        # We have to deque because of the way goldS did the output.
                        # When something is going to preempt. it isn't in the workQ.
                        # Remove, Print, then re-add
                        k = self.workQ.dequeue()
                        writeOutput("time {0}ms: Process {1} completed I/O and will preempt {2} {3}\n".format(int(self.rTime), p.label, self.cProc.label, self.procPrinter.getQStr()), self.cProc.label, evenIO())
                        p.arrivalTimeLeft = -25 #Aritrary constant
                        self.workQ.enqueu(k)

                    elif(p.burstTimeLeft < p.burstTime):
                        pass

                    else:
                        writeOutput("time {0}ms: Process {1} completed I/O; added to ready queue {2}\n".format(int(self.rTime), p.label, self.procPrinter.getQStr()), p.label, evenIO())

                elif(not(self.cProc is None) and self.procHelper.procReady() and self.algorithm != "FCFS"):
                    #We have to deque because of the way goldS did the output.
                    #When something is going to preempt. it isn't in the workQ.
                    #Remove, Print, then re-add
                    k = self.workQ.dequeue()
                    writeOutput("time {0}ms: Process {1} arrived and will preempt {2} {3}\n".format(int(self.rTime), p.label, self.cProc.label, self.procPrinter.getQStr()), self.cProc.label, evenIO())

                    p.arrivalTimeLeft = -25 #Aritrary constant
                    self.workQ.enqueu(k)
                else:

                    writeOutput("time {0}ms: Process {1} arrived and added to ready queue {2}\n".format(int(self.rTime), p.label, self.procPrinter.getQStr()), p.label, evenIO())
                    p.arrivalTimeLeft = -25 #Aritrary constant
                ####################################################


            #If it is finished, then remove it all together.
            elif(p.isFinished()):
                rLst.append(p)

        #Go back and clean up procPool
        for p in rLst:
            self.procPool.remove(p)

        #####################################################################
        #Clean up List
        rLst = []
        #
        #####################################################################

        #If it is not ready, then remove it from workQ, this shouldnt happen, but just in case.
        for p in self.workQ.queue:
            p.step(self.rTime)
            if(not p.isReady()):
                rLst.append(p)
                self.procPool.append(p)

            #If finished then remove
            elif(p.isFinished()):
                rLst.append(p)

        #Go back and clean up workQ
        for p in rLst:
            self.workQ.queue.remove(p)

        #Step the workQ object
        self.workQ.step(self.algorithm)
