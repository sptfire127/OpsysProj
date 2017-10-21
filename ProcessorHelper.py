from Process import *
from output import *


class ProcessorHelper():
    """
    Does arithmitic to calculate the current burst and add it to the average.
    NOTE: YOU MUST TRACK START BURST AND LOG EVERY TIME A CONTEXT SWITCH OCCURS.
    """
    processor = None
    process = None

    def __init__(self, processor):
        self.processor = processor
        self.process = self.processor.cProc

    """
    Run the simulation through 'cycles' amount of iterations
        NOTE: If cycles == -1, run till completion
    """
    def run(self, cycles):

        #If -1, run till completion
        if(cycles == -1):
            i = 0

            writeOutput("time {0}ms: Simulator started for {1} {2}\n".format(int(self.processor.rTime), self.processor.algorithm, self.processor.procPrinter.getQStr()), self.processor.rTime, evenCPU())

            while(not self.processor.procHelper.finished()):
                #self.procPrinter.qPrint()               #Print out processor queue's
                self.processor.step()                    #Step the processor go to disc
                i += 1

            return 0

    def finalize(self):
        # CALULATE AVERAGES
        wait = 0
        turnAround = 0
        for p in self.processor.donePool:
            wait += p.waitTime              #Increment wait time
            turnAround += p.turnAround

        # This is the final context switch
        self.processor.cSwitchAmt += .5
        # Account for last context switch and for the last step
        self.processor.rTime += self.processor.cSwitchTime / 2
        # Extract averages
        self.processor.avgWait = float(wait) / self.processor.totalBurstCount
        self.processor.avgTurnAround = float(turnAround) / self.processor.totalBurstCount

        # simout
        writeSimout("Algorithm {0}\n".format(self.processor.algorithm))
        #writeSimout("-- Total runtime: {0}ms\n".format(self.processor.rTime))
        #writeSimout("-- Total burst time: {0}ms\n".format(self.processor.totalBurst))
        #writeSimout("-- Total wait time: {0}ms\n".format(wait))
        writeSimout("-- average CPU burst time: {0} ms\n".format(round(self.processor.totalBurst / self.processor.totalBurstCount, 2)))
        writeSimout("-- average wait time: {0} ms\n".format(round(self.processor.avgWait),2 ))
        writeSimout("-- average turnaround time: {0} ms\n".format(round(self.processor.avgTurnAround, 2)))
        writeSimout("-- total number of context switches: {0}\n".format(int(self.processor.cSwitchAmt)))
        writeSimout("-- total number of preemptions: 0\n")
        writeOutput("time {0}ms: Simulator ended for {1}\n".format(int(self.processor.rTime), self.processor.algorithm), self.processor.rTime, evenCPU())
        writeOutput()



    def logBurst(self):
        # Calculate the current burst time
        if (self.processor.rTime > self.processor.cProc.lastLogged):
            bTime = self.processor.rTime - self.processor.startBurst
            # Account for waitTime increasing an extra time
            self.processor.cProc.waitTime -= 1
            print("time {0}ms: Process {1} my wait time is {2}."
                  .format(self.processor.rTime, self.processor.cProc.label, self.processor.cProc.waitTime))
            print("time {0}: Process {1} should have burst time {2}, and has actual burst time {3}\n".format(self.processor.rTime, self.processor.cProc.label, self.processor.cProc.burstTime, bTime))
            self.processor.nBurst += 1
            print("time {0}: I started bursting at {1}".format(self.processor.rTime, self.processor.startBurst))
            print("time {0}:Total burst time = {1}, ".format(self.processor.rTime,self.processor.totalBurst))
            self.processor.totalBurst = (self.processor.totalBurst + bTime)
            print("is now = {0}\n".format(self.processor.totalBurst))
            self.processor.cProc.lastLogged = self.processor.rTime

    """
    Add a processor to the procPool
    """

    def addProc(self, proc):
        # Make sure proc is a process
        assert (isinstance(proc, Process))
        self.processor.procPool.append(proc)
        self.processor.totalBurstCount += proc.burstCount
        return

    """
    Are we done yet? :Kappa:
    """

    def finished(self):
        if (self.processor.cProc is not None):
            return ((self.processor.workQ.size() == 0) and (
            len(self.processor.procPool) == 0) and self.processor.cProc.state == "FINISHED")
        return False

    """
    Do I need to Context switch
    NOTE: if this returns none, simulation has ended
    """
    def procReady(self):
        self.processor.workQ.step(self.processor.algorithm)
        # If cProc is None and:
        #       WorkQ empty  -> False
        #       WorkQ !empty -> True
        if (self.processor.cProc is None and not self.processor.workQ.isEmpty()):
            return True
        if (self.processor.cProc is None):
            return False

        ############################################
        #   These should be the same no matter the algorithm
        #
        # if current proc is done or finished
        if (self.processor.cProc.state == "FINISHED"):
            # append to donePool
            self.processor.donePool.append(self.processor.cProc)
            writeOutput(
                "time {0}ms: Process {1} terminated {2}\n".format(int(self.processor.rTime), self.processor.cProc.label, self.processor.procPrinter.getQStr()), self.processor.rTime, evenCPU())
            print("FINISHED: time {0}ms: I'm about to start my burst bro".format(self.processor.rTime))
            self.processor.procHelper.logBurst()
            # Call step even though we're done so the process can calculate final
            # average statistics
            self.processor.cProc.step()
            #print(self.processor.cProc.turnAround)
            # Check to see if we are finished. If so, return None
            if (self.processor.procHelper.finished()):
                return None

            # Not ended, return true
            return True

        # If its blocked we always context switch
        elif (self.processor.cProc.state == "BLOCKED"):

            if (self.processor.cProc.burstCount != 1):
                # Next time to pre-empt is now + the time slice + context switch time
                writeOutput(
                    "time {0}ms: Process {1} completed a CPU burst; {2} bursts to go {3}\n".format(
                        int(self.processor.rTime),
                        self.processor.cProc.label,
                        self.processor.cProc.burstCount,
                        self.processor.procPrinter.getQStr()), self.processor.rTime, evenCPU())

            else:
                # Next time to pre-empt is now + the time slice + context switch time
                writeOutput(
                    "time {0}ms: Process {1} completed a CPU burst; {2} burst to go {3}\n".format(
                        int(self.processor.rTime),
                        self.processor.cProc.label,
                        self.processor.cProc.burstCount,
                        self.processor.procPrinter.getQStr()), self.processor.rTime, evenCPU())
            print("BLOCKED: time {0}ms: I'm about to start my burst bro".format(self.processor.rTime))
            self.processor.procHelper.logBurst()


            return True
        #
        #
        #
        ############################################


        elif self.processor.algorithm == "FCFS":
            # NEVER, only time is either finished or blocked cProc
            return False

        elif self.processor.algorithm == "SRT":
            if (not self.processor.workQ.isEmpty()):
                # If next proc.burst < this proc's burst
                p = self.processor.workQ.peak()
                if (p.burstTimeLeft < self.processor.cProc.burstTimeLeft):
                    if (self.processor.cProc.burstTimeLeft < self.processor.cProc.burstTime):
                        # For some reason the SRT algorithm is 1MS off on burstTime left... you know what to do
                        if (self.processor.algorithm == "SRT"):
                            writeOutput(
                                "time {0}ms: Process {1} started using the CPU with {2}ms remaining {3}\n".format(
                                    int(self.processor.rTime), self.processor.cProc.label,
                                    self.processor.cProc.burstTimeLeft,
                                    self.processor.procPrinter.getQStr()), self.processor.rTime, evenCPU())
                        else:
                            writeOutput(
                                "time {0}ms: Process {1} started using the CPU with {2}ms remaining {3}\n".format(
                                    int(self.processor.rTime), self.processor.cProc.label,
                                    self.processor.cProc.burstTimeLeft,
                                    self.processor.procPrinter.getQStr()), self.processor.rTime, evenCPU())
                    else:
                        # This is to ensure that the workQ is in its updated state before printing.
                        # it has no actual affect on the running since we will step it before
                        # any calculations are done
                        self.processor.workQ.step(self.processor.algorithm)
                        writeOutput(
                            "time {0}ms: Process {1} started using the CPU {2}\n".format(int(self.processor.rTime),
                                                                                         self.processor.cProc.label,
                                                                                         self.processor.procPrinter.getQStr()), self.processor.rTime, evenCPU())
                    return True



        elif self.processor.algorithm == "RR":
            if (self.processor.rTime >= self.processor.nxtSlice):
                if (not self.processor.workQ.isEmpty()):
                    writeOutput("time {0}ms: Time slice expired; process {1} preempted with {2}ms to go {3}\n".format(
                        int(self.processor.rTime), self.processor.cProc.label, self.processor.cProc.burstTimeLeft, self.processor.procPrinter.getQStr()), self.processor.rTime, evenCPU())
                return True

        return False
