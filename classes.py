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
    workQ           -- Processor work Queue / ready Queue (Which is basically a stack with extra functionality)
    procPool        -- Total pool of all processors in scope
    algorithm       -- Selected scheduling algorithm
    cProc           -- Current running process (Used for logging / debugging)

"""
class Processor():

    """
    DECIDE HOW TO INIT PROCESSOR

    IDEA: Have self.algorithm be set on init
    """
    def __init__(self, cSwitchTime, algorithm):
        self.rTime = 0
        self.cSwitchTime = cSwitchTime
        self.workQ = workQ()
        self.procPool = []
        self.algorithm = algorithm
        self.cProc = None




    """
    Add a processor to the procPool
    """
    def addProc(self, proc):
        #Make sure proc is a process
        assert(isinstance(proc, Process))
        self.procPool.append(proc)
        return


    """
    Are we done yet? :Kappa:
    """
    def finished(self):
        return ((self.workQ.size() == 0) and (len(self.procPool) == 0) and self.cProc.state == "FINISHED")



    """
    Simulates one processor PROC_CYLCE.
        This should entail ::=> - Log any processor state statistics if needed
                                - __step_workQ()
                                - Call correct scheduling handler
                                - Detect any errors in PROC_CYLCE
    """
    def step(self):
        #LOG SHIT HERE TODO


        #Increment running time
        self.rTime += 1

        #Step the worQ
        self.__step_workQ()

        #If proc is not none, step it. If it is none, will be handled in handler
        if(not (self.cProc is None)):
            self.cProc.step()


        #Call correct handler
        if(self.algorithm == "FCFS"):
            self.__handle_FCFS()
        elif(self.algorithm == "SRT"):
            self.__handle_SRT()
        elif(self.algorithm == "RR"):
            self.__handle_RR()
        else:
            raise RuntimeError("INVALID ALGORITHM")


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

        #Step every process in the procPool and handle adding / removing from workQ
        for p in self.procPool:
            p.step()
            if ((p.getArrival() <= self.rTime) and (p.isReady())):
                self.workQ.enqueu(p)
                self.procPool.remove(p)

            #If it is finished, then remove it all together.
            elif(p.isFinished()):
                print("PROCESS '{0}' FINISHED AT EXECUTION TIME {1} !".format(p, self.rTime))
                self.procPool.remove(p)

        #If it is not ready, then remove it from workQ, this shouldnt happen, but just in case.
        for p in self.workQ.queue:
            p.step()
            if(not p.isReady()):
                self.workQ.queue.remove(p)
                self.procPool.append(p)
            #If finished then remove
            elif(p.isFinished()):
                print("PROCESS '{0}' FINISHED AT EXECUTION TIME {1} !".format(p, self.rTime))
                self.workQ.queue.remove(p)


        #Step the workQ object
        self.workQ.step(self.algorithm)


    #######SCHEDULING ALGORITHM HANDLERS BELOW THIS LINE####
    #   These should all manipulate the state of the processor
    #   based on their respective algorithms.
    #
    #   IE: Should I context switch? Pull next process from workQ?
    #       Keep track of time spent on context switches, running time, etc.
    #
    #
    ########################################################
    def __handle_FCFS(self):

        #If none then put in process
        if(self.cProc is None):
            self.cProc = self.workQ.dequeue()
            self.cProc.stateChange("RUNNING")

        
        elif(self.cProc.state == "BLOCKED"):
            self.procPool.append(self.cProc)
            self.cProc = self.workQ.dequeue()
            self.cProc.stateChange("RUNNING")

        elif(self.cProc.state == "RUNNING"):
            pass
            #Continue running process

        elif(self.cProc.isFinished()):
            print("PROCESS '{0}' FINISHED AT EXECUTION TIME {1} !".format(self.cProc, self.rTime))
            if(self.finished()):
                return
            self.cProc = self.workQ.dequeue()
            self.cProc.stateChange("RUNNING")


        else:
            raise RuntimeError("INVALID STATE ON CPROC: {0}".format(self.cProc))


    def __handle_SRT(self):
        #TODO
        pass

    def __handle_RR(self):
        #TODO
        pass
    #######SCHEDULING ALGORITHM HANDLERS ABOVE THIS LINE####

    def qprint(self):
        print("PRINTING PROCESS POOL:")
        for p in self.procPool:
            print(p)
        print()
        print("PRINTING WORKQ:")
        for p in self.workQ.queue:
            print(p)
        print()



    def __str__(self):
        s = "PROC INFO:\ncSwitchTime : {0}\nworkQ Size : {1}\n".format(self.cSwitchTime, self.workQ.size()) + \
            "procPool Size : {0}\nalgorithm : {1}\ncProc : {2}".format(len(self.procPool), self.algorithm, self.cProc)
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
                =SHOULD INIT TO READY STATE????=

            - Arrival Time

            - Burst Time Total
            --Burst Time Left
            - Burst Count

            - I/O Time Total
            --I/O Time Left

            --waitTime



"""
class Process():

    def __init__(self, label, arrival, burst, burstCount, IOtime):
        self.label = label
        self.state = "READY"
        self.arrivalTime = arrival
        self.burstTime = burst
        self.burstCount = burstCount
        self.IOtime = IOtime
        self.burstTimeLeft = self.burstTime
        self.IOtimeLeft = self.IOtime
        self.waitTime = 0


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
        if(self.state == "READY"):
            self.waitTime += 1
            #DO I PASS HERE? FIXME MAYBE COUNT WAIT TIME?
        elif(self.state == "RUNNING"):
            self.burstTimeLeft -= 1

        elif(self.state == "BLOCKED"):
            self.IOtimeLeft -= 1
        elif(self.state == "FINISHED"):
            pass
        else:
            raise RuntimeError("PROCESS STATE INVALID")
        pass


        #More arithmitic
        if(self.burstTimeLeft == 0):
            self.burstTimeLeft = self.burstTime
            self.burstCount -= 1
            if(self.burstCount == 0):
                self.state = "FINISHED"
            else:
                self.state = "BLOCKED"
        elif(self.IOtimeLeft == 0):
            self.IOtimeLeft = self.IOtime
            self.state = "READY"

    def __str__(self):
        return "Label: {0} | State: {1} (burstTimeLeft: {2} | burstCount: {3})".format(self.label, self.state, self.burstTimeLeft, self.burstCount)

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


################################################################################
# DONT SHOULD NOT BE INVOKED DIRECTLY
################################################################################
    def __qFCFS(self):
        #ENQUEUE and DEQUEUE already preserve FCFS Nature.. ? #FIXME
        pass

    def __qSRT(self):
        #TODO
        pass

    def __qRR(self):
        #TODO
        pass

################################################################################
