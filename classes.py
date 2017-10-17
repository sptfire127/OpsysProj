# coding=utf-8
import operator
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
        self.cSwitchAmt = 0
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

        self.tSlice = tSlice
        if(not (tSlice is None)):
            #Init next time slice
            self.nxtSlice = self.rTime + self.tSlice + (self.cSwitchTime / 2)
        else:
            self.nxtSlice = None







    """
    Run the simulation through 'cycles' amount of iterations
        NOTE: If cycles == -1, run till completion
    """
    def run(self, cycles):

        #If -1, run till completion
        if(cycles == -1):
            i = 0

            writeOutput("time {0}ms: Simulator started for {1} {2}\n".format(int(self.rTime), self.algorithm, self.getQStr()))

            while(not self.finished()):
                print("\n==============Execution {0}==============\n".format(i))
                print(self)                 #Print out processor state
                self.qprint()               #Print out processor queue's
                self.step()                 #Step the processor
                if(self.finished()):        #If we finish, then check
                    print("\n===============================\n")
                    print("Done. Looped through {0} iterations".format(i))
                    print(self)
                    self.qprint()
                    print("\n===============================\n")
                    break
                print("\n===============================\n")
                i += 1

            # CALULATE AVERAGES
            wait = 0
            turnAround = 0
            for p in self.donePool:
                wait += p.waitTime              #Increment wait time
                turnAround += p.turnAround      #Increment turnAround time

            #Extract averages
            wait = float(wait) / self.totalBurstCount
            turnAround = float(turnAround) / self.totalBurstCount
            print("Avg wait time : {0}".format(wait))
            print("Avg turnAround time : {0}".format(turnAround))
            print("cSwitchAmt : {0}".format(self.cSwitchAmt))
            writeOutput("time {0}ms: Simulator ended for {1}".format(int(self.rTime), self.algorithm))
            writeOutput("\n")
            return 0

        #Run for cycles amount of cycles
        else:
            for i in range(0, cycles):
                print("\n==============Execution {0}==============\n".format(i))
                print(self)                 #Print out processor state
                self.qprint()               #Print out processor queue's
                self.step()                 #Step the processor
                if(self.finished()):        #If we finish, then check
                    print("Done. Looped through {0} iterations".format(i))
                    self.qprint()
                    # CALULATE AVERAGES
                    wait = 0
                    turnAround = 0
                    for p in self.donePool:
                        wait += p.waitTime              #Increment wait time
                        turnAround += p.turnAround      #Increment turnAround time

                    #Extract averages
                    wait = float(wait) / self.totalBurstCount
                    turnAround = float(turnAround) / self.totalBurstCount
                    print("Avg wait time : {0}".format(wait))
                    print("Avg turnAround time : {0}".format(turnAround))
                    print("cSwitchAmt : {0}".format(self.cSwitchAmt))

                    return 0
                print("\n===============================\n")



    """
    Does arithmitic to calculate the current burst and add it to the average.
    NOTE: YOU MUST TRACK START BURST AND LOG EVERY TIME A CONTEXT SWITCH OCCURS.
    """
    def logBurst(self):
        bTime = self.rTime - self.startBurst
        self.nBurst += 1
        self.totalBurst = (self.totalBurst + bTime)




    """
    Add a processor to the procPool
    """
    def addProc(self, proc):
        #Make sure proc is a process
        assert(isinstance(proc, Process))
        self.procPool.append(proc)
        self.totalBurstCount += proc.burstCount
        return


    """
    Are we done yet? :Kappa:
    """
    def finished(self):
        return ((self.workQ.size() == 0) and (len(self.procPool) == 0) and self.cProc.state == "FINISHED")



    """
    Do I need to preempt?
    """
    def procReady(self):
        if(self.workQ.isEmpty()): return False


        if self.algorithm == "FCFS":
            #In FCFS we never prempt a proc
            return False;

        elif self.algorithm == "SRT":
            #If next proc.burst < this proc's burst
            p = self.workQ.peak()
            if(p.burstTime < self.cProc.burstTimeLeft): return True


        elif self.algorithm == "RR":
            if(self.rTime >= self.nxtSlice):
                writeOutput("time {0}ms: Time slice expired; process {1} preempted with {2}ms to go {3}\n".format(int(self.rTime), self.cProc.label, self.cProc.burstTimeLeft, self.getQStr()))
                return True

        return False




    """
    Simulates one processor PROC_CYLCE in PROCESSOR
        This should entail ::=> - Log any processor state statistics if needed
                                - __step_workQ()
                                - Call correct scheduling handler
                                - Detect any errors in PROC_CYLCE
    """
    def step(self):
        #LOG SHIT HERE TODO

        #Step the worQ
        self.__step_workQ()

        #Increment running time
        self.rTime += 1


        #If proc is not none, step it. If it is none, will be handled in handler
        if(not (self.cProc is None)):
            self.cProc.step()

        self.__handle_FCFS()
        """
        #Call correct handler
        if(self.algorithm == "FCFS"):
            self.__handle_FCFS()
        elif(self.algorithm == "SRT"):
            self.__handle_SRT()
        elif(self.algorithm == "RR"):
            self.__handle_RR()
        else:
            raise RuntimeError("INVALID ALGORITHM")
        """

    ########################################################
    #THESE SHOULD NEVER BE DIRECTLY CALLED, ONLY FROM STEP()
    ########################################################

    """
    This should cylce through all processors in the self.procPool and move any READY
    processors into the workQ and remove any !READY processors into procPool
    Then organize the workQ so the next processor is in front of the workQ
    based on the selected scheduling algorithm.
    I decided to do this in a seperate
    method to prevent bloating the scheduling methods.
    """
    def __step_workQ(self):

        rLst = []
        #Step every process in the procPool and handle adding / removing from workQ
        for p in self.procPool:
            p.step()

            #Has the process arrived and is it ready?
            if ((p.getArrival() <= self.rTime) and (p.isReady())):
                #Add this to the workQ and remove it from procPool later
                self.workQ.enqueu(p)
                rLst.append(p)

                # OUTPUT.TXT FILEV##################################
                if(p.arrivalTimeLeft == -25): #Aritrary constant
                    writeOutput("time {0}ms: Process {1} completed I/O; added to ready queue {2}\n".format(int(self.rTime), p.label, self.getQStr()))

                elif(not(self.cProc is None) and self.procReady()):
                    writeOutput("time {0}ms: Process {1} arrived and will preempy {2} {3}\n".format(int(self.rTime), p.label, self.cProc.label, self.getQStr()))
                    p.arrivalTimeLeft = -25 #Aritrary constant

                else:
                    writeOutput("time {0}ms: Process {1} arrived and added to ready queue {2}\n".format(int(self.rTime), p.label, self.getQStr()))
                    p.arrivalTimeLeft = -25 #Aritrary constant
                ####################################################


            #If it is finished, then remove it all together.
            elif(p.isFinished()):
                print("PROCESS '{0}' FINISHED AT EXECUTION TIME {1} !".format(p, self.rTime))
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
            p.step()
            if(not p.isReady()):
                rLst.append(p)
                self.procPool.append(p)

            #If finished then remove
            elif(p.isFinished()):
                print("PROCESS '{0}' FINISHED AT EXECUTION TIME {1} !".format(p, self.rTime))
                rLst.append(p)

        #Go back and clean up workQ
        for p in rLst:
            self.workQ.queue.remove(p)

        #Step the workQ object
        self.workQ.step(self.algorithm)


    """
    Handle all the wait time logic for doing a context switch
    with respect to waiting processes
    """
    def cleanCSwitch(self, time):

        #Add time to wait time in workQ
        for p in self.workQ.queue:
            p.waitTime += time

        rmList = []     #List to remove later to preserve loop iteration

        #Calculate future time values and preform logic on
        #Processes. This loop should ensure accuracy carried through
        #events occuring during a context switch
        for p in self.procPool:
            #Factor context switch into wait
            wait = p.IOtimeLeft - time

            #Factor context switch into arrivalTime
            arriv = p.arrivalTimeLeft - time

            #We are arrived and became ready mid-context switch
            if(wait <= 0 and p.isArrived()):
                #Remove from procPool
                rmList.append(p)
                #Add to workQ
                self.workQ.enqueu(p)
                #Change to ready
                p.stateChange("READY")
                #add the overflow into the waitTime, reset IOtimeLeft
                p.waitTime += abs(wait)
                p.IOtimeLeft = p.IOtime

            #We are arrived just blocked doing IO for whole contextSwitch
            elif(p.isArrived()):
                p.IOtimeLeft = wait

            #Havent arrived
            else:
                #Arrived mid context switch
                if(arriv <= 0):
                    #Remove from procPool
                    rmList.append(p)
                    #Add to workQ
                    self.workQ.enqueu(p)
                    #Change to ready
                    p.stateChange("READY")
                    #Set arrived = True
                    p.arrived = True
                    #add overflow to waitTime
                    p.waitTime += abs(arriv)

                #Still waiting to arrive
                else:
                    p.arrivalTimeLeft = arriv

        #Remove processes from procPool
        for p in rmList:
            self.procPool.remove(p)




    """
    Preform a context switch with self.cProc for newProc argument
    Handles logic for if self.cProc is None.
    NOTE: FIX THE LOGIC FOR THE CONTEXT SWITCH TIME
    """
    def contextSwitch(self, newProc):
        assert(isinstance(newProc, Process))

        #Dont log on initial context switch, Handle the calculation for cSwitchTime
        if(not (self.cProc is None) and not self.cProc.isFinished()):
            #Clean up context switch logic and wriqte output
            self.cSwitchAmt += 1                    #   Add a context switch to total
            self.rTime += (self.cSwitchTime)
            self.cleanCSwitch((self.cSwitchTime))

            self.logBurst()
            #Proc still wants to run, change to ready and put in workQ
            if(self.cProc.state == "RUNNING"):
                self.cProc.stateChange("READY")
                self.workQ.enqueu(self.cProc)
            else:
                #Our state must be blocked
                self.procPool.append(self.cProc)
                self.cProc.IOtimeLeft -= (self.cSwitchTime/2) - 1

        #Our current process is finished
        elif(not (self.cProc is None)):
            self.cSwitchAmt += 1                    #   Add a context switch to total
            self.rTime += (self.cSwitchTime)
            self.cleanCSwitch((self.cSwitchTime))
            self.logBurst()


        else:
            #Clean up context switch logic
            #Here we are just loading a process
            self.cSwitchAmt += 1/2                    #   Add a context switch to total
            self.rTime += (self.cSwitchTime / 2) - 1
            self.cleanCSwitch((self.cSwitchTime / 2) - 1)


        #Load new process, Change state, Adjust wait time
        self.cProc = newProc                    #   LOAD NEW
        self.cProc.stateChange("RUNNING")       #   CHANGE STATE
        self.startBurst = self.rTime            #   Log the start of a burst
        self.cProc.waitTime -= 1                #   Take into account proc.step() adding
                                                #     -> +1 to the wait time
        writeOutput("time {0}ms: Process {1} started using the CPU {2}\n".format(int(self.rTime), newProc.label, self.getQStr()))


    #######SCHEDULING ALGORITHM HANDLERS BELOW THIS LINE####
    #   These should all manipulate the state of the processor
    #   based on their respective algorithms.
    #
    #   THIS SHOULD BE THE ONLY PLACE A CONTEXT SWITCH HAPPENS
    #
    #
    ########################################################
    def __handle_FCFS(self):

        #If none then put in process (As long as workQ has jobs)
        #CONTEXT SWITCH
        if(self.cProc is None and (not self.workQ.isEmpty())):
            #Next time to pre-empt is now + the time slice + context switch time
            p = self.workQ.dequeue()
            self.contextSwitch(p)
            return

        #cProc is None but workQ is empty
        #Just keep cycling processor.
        elif(self.cProc is None and (self.workQ.isEmpty())):
            pass

        #If cProc became blocked (from calling cProc.step()), swap it out for new process in workQ
        #CONTEXT SWITCH
        elif(self.cProc.state == "BLOCKED" and (not self.workQ.isEmpty())):
            if(self.cProc.burstCount != 1):
                #Next time to pre-empt is now + the time slice + context switch time
                writeOutput("time {0}ms: Process {1} completed a CPU burst; {2} bursts to go {3}\n".format(int(self.rTime), self.cProc.label, self.cProc.burstCount, self.getQStr()))
            else:
                #Next time to pre-empt is now + the time slice + context switch time
                writeOutput("time {0}ms: Process {1} completed a CPU burst; {2} burst to go {3}\n".format(int(self.rTime), self.cProc.label, self.cProc.burstCount, self.getQStr()))

            writeOutput("time {0}ms: Process {1} switching out of CPU; will block on I/O until time {2}ms {3}\n".format(int(self.rTime), self.cProc.label, int(self.cProc.IOtimeLeft + (self.rTime) + (self.cSwitchTime/2)), self.getQStr()))

            self.nxtSlice = self.rTime + self.tSlice + self.cSwitchTime
            p = self.workQ.dequeue()
            self.contextSwitch(p)

        #If cProc is became blocked but next process is not ready, then set to None
        elif(self.cProc.state == "BLOCKED" and (self.workQ.isEmpty())):
            writeOutput("time {0}ms: Process {1} completed a CPU burst; {2} bursts to go {3}\n".format(int(self.rTime), self.cProc.label, self.cProc.burstCount, self.getQStr()))
            writeOutput("time {0}ms: Process {1} switching out of CPU; will block on I/O until time {2}ms {3}\n".format(int(self.rTime), self.cProc.label, self.cProc.IOtimeLeft + int(self.rTime), self.getQStr()))
            #Next time to pre-empt is now + the time slice + context switch time
            self.nxtSlice = self.rTime + self.tSlice + self.cSwitchTime
            self.procPool.append(self.cProc)
            self.rTime += self.cSwitchTime / 2
            self.cleanCSwitch(self.cSwitchTime / 2)
            self.cSwitchAmt += 1/2
            self.cProc = None


        #Process is running ... Continue
        # TODO :    WE SHOULD ADD PREMPTION LOGIC HERE TO DETERMINE IF WE NEED TO
        #           CONTEXT SWITCH, THIS SHOULD COVER ALL SUPPORTED ALGORITHMS
        #
        elif(self.cProc.state == "RUNNING"):
            if(self.procReady()):
                if(self.algorithm == "RR"):
                    #Next time to pre-empt is now + the time slice + context switch time
                    self.nxtSlice = self.rTime + self.tSlice + self.cSwitchTime
                p = self.workQ.dequeue()
                self.contextSwitch(p)

            #Continue running process

        # Process is finished
        elif(self.cProc.isFinished()):
            print("PROCESS '{0}' FINISHED AT EXECUTION TIME {1} !".format(self.cProc, self.rTime))
            self.donePool.append(self.cProc)
            writeOutput("time {0}ms: Process {1} terminated {2}\n".format(int(self.rTime), self.cProc.label, self.getQStr()))

            #Next time to pre-empt is now + the time slice + context switch time
            self.nxtSlice = self.rTime + self.tSlice + self.cSwitchTime

            #Call step even though we're done so the process can calculate final
            #average statistics
            self.cProc.step()


            #Check to see if we are finished. If so, return.
            if(self.finished()):
                self.logBurst()
                return

            #Do we have a next process ?
            elif(not self.workQ.isEmpty()):
                    p = self.workQ.dequeue()
                    self.contextSwitch(p)

            #No next proc, just pass.
            else:
                    self.rTime += self.cSwitchTime / 2
                    self.cleanCSwitch(self.cSwitchTime / 2)
                    self.cSwitchAmt += 1/2
                    self.cProc = None

        else:
            self.qprint()
            self.statprint()
            print(self)
            raise RuntimeError("ERROR IN PROCESSOR HANDLER, I HAVE PRINTED MY STATE")


    def __handle_SRT(self):
        #TODO
        pass

    def __handle_RR(self):
        #TODO
        pass
    #######SCHEDULING ALGORITHM HANDLERS ABOVE THIS LINE####
    ########################################################
    ####### PRINTING FUNCTIONS BELOW THIS LINE #############

    def getQStr(self):
        s = ""
        if(self.workQ.isEmpty()):
            s = "[Q <empty>]"
        else:
            s += "[Q"
            for p in self.workQ.queue:
                s += " "
                s += p.label
            s += "]"
        return s



    """
    Print all of the Q's
    """
    def qprint(self):
        print("PRINTING PROCESS POOL:")
        i = 0
        for p in self.procPool:
            print(str(i) + "|------>|" + str(p))
            i += 1
        print()
        print("PRINTING WORKQ:")
        i = 0
        for p in self.workQ.queue:
            print(str(i) + "|------>|" + str(p))
            i += 1
        print()
        print("PRINTING DONEPOOL:")
        i = 0
        for p in self.donePool:
            print(str(i) + "|------>|" + str(p))
            i += 1
        print()

    """
    Print out statistics for this processor
    """
    def statprint(self):
        print("===== PROC STATS =====\n")

        if(self.nBurst == 0):
            print("totalBurst : {0}\nnBurst : {1}\nAvgBursts : {2}\ncSwitchAmt : {3}".format(self.totalBurst, self.nBurst, self.totalBurst, self.cSwitchAmt))
            return

        print("totalBurst : {0}\nnBurst : {1}\nAvgBursts : {2}\ncSwitchAmt : {3}".format(self.totalBurst, self.nBurst, (self.totalBurst / self.nBurst), self.cSwitchAmt))



    def __repr__(self):
        return str(vars(self))

    def __str__(self):
        s = "PROC INFO:\ncSwitchTime : {0} ms\nRunTime : {1} ms\nworkQ Size : {2} processes\n".format(self.cSwitchTime, int(self.rTime), self.workQ.size()) + \
            "procPool Size : {0} processes\nalgorithm : {1}\ncProc : {2}\n".format(len(self.procPool), self.algorithm, self.cProc)
        if( not (self.tSlice is None)):
            s += "nxtSlice : {0} ms".format(self.nxtSlice)

        return s

################################################################################


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
        assert(burst != 0 and burstCount != 0)
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

    #returns whether or not this process is in the ready state
    def isReady(self):
        return self.state == "READY"


    def isArrived(self):
        return self.arrivalTimeLeft <= 0

    #Am I finished?
    def isFinished(self):
        return self.state == "FINISHED"

    #Getter for self.arrivalTime
    def getArrival(self):
        return self.arrivalTime


    """
    This should do arithmitic off the BurstTime, I/O Time
        -> Change self.state based on these times.
    NOTE: THIS IS NOT WHERE PROCESS SHOULD BE CHANGED TO A RUNNING STATE
    """
    def step(self):
        #Determine state and decriment accoringly
        #Only increment wait if proc has started running
        if(self.state == "READY" and self.arrived):
            self.waitTime += 1

        #Proc is waiting to arrive
        elif(self.state == "READY" and not self.arrived):
            if(self.arrivalTimeLeft == 0):
                self.arrived = True
            self.arrivalTimeLeft -= 1


        elif(self.state == "RUNNING"):
            self.executionTime += 1
            self.burstTimeLeft -= 1

        elif(self.state == "BLOCKED"):
            self.IOtimeLeft -= 1

        elif(self.state == "FINISHED"):
            self.turnAround = self.waitTime + (self.executionTime)

        else:
            raise RuntimeError("PROCESS STATE INVALID")


        #More arithmitic
        if(self.burstTimeLeft <= 0 and self.state == "RUNNING"):
            self.burstTimeLeft = self.burstTime
            self.burstCount -= 1
            if(self.burstCount == 0):
                self.state = "FINISHED"

            else:
                self.state = "BLOCKED"
        elif(self.IOtimeLeft <= 0 and self.state == "BLOCKED"):
            self.IOtimeLeft = self.IOtime
            self.state = "READY"



    def __repr__(self):
        return str(vars(self))


    def __str__(self):
        return "Label: {0} | State: {1} (burstTimeLeft: {2} | burstTime: {3} | burstCount: {4}) (IOtimeLeft: {5} | IOtime: {6}) (waitTime : {7} arrivalTime : {8})".format(self.label, self.state, self.burstTimeLeft, self.burstTime, self.burstCount, self.IOtimeLeft, self.IOtime, self.waitTime, self.arrivalTime)
################################################################################


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

        #Call right handler
        if(algorithm == "FCFS"):
            return self.__qFCFS()

        elif(algorithm == "SRT"):
            return self.__qSRT()

        elif(algorithm == "RR"):
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
        assert(isinstance(proc, Process))
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
        #ENQUEUE and DEQUEUE already preserve FCFS Nature.. ? #FIXME
        pass

    def __qSRT(self):
        self.queue.sort(key=operator.attrgetter("burstTimeLeft"))


    def __qRR(self):
        #TODO
        pass

################################################################################
