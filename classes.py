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
    def __init__(self):
        #TODO

    """
    Simulates one processor PROC_CYLCE.
        This should entail ::=> - Log any processor state statistics if needed
                                - __step_workQ()
                                - Call correct scheduling handler
                                - Detect any errors in PROC_CYLCE
    """
    def step(self):
        #TODO


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
        #TODO


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
        #TODO

    def __handle_SRT(self):
        #TODO

    def __handle_RR(self):
        #TODO
    #######SCHEDULING ALGORITHM HANDLERS ABOVE THIS LINE####


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

            - Arrival Time

            - Burst Time Total
            --Burst Time Left
            - Burst Count

            - I/O Time Total
            --I/O Time Left


"""
class Process():

    def __init__(self):
        #TODO


    """
    This should do arithmitic off the BurstTime, I/O Time
        -> Change self.state based on these times
    """
    def step(self):
        #TODO

################################################################################


"""
workQ class which uses a list as an underlying implemetation.

Attributes: workQ -- List representing the Queue
"""
class workQ():

    def __init__(self):
        #TODO


    """
    This should reorganize the workQ based on the algorithm passed in
    """
    def step(self, algorithm):
        #TODO

    """
    Add something to the workQ tail
    """
    def enqueu(self):
        #TODO

    """
    Remove head from the Queue
    """
    def dequeue(self):
        #TODO

################################################################################
