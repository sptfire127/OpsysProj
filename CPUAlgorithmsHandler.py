from output import *

# Helps processor handle all scheduling algorithms
# (FCFS, SRT, RR)
# TODO:
# Create a generic stepping helper function
# Implement FCFS, SRT, and RR separate using helper function


class CPUAlgorithmsHandler():
    cSwitcher = None
    processor = None

    def __init__(self, processor):
        self.processor = processor
        self.cSwitcher = processor.cSwitcher
        pass

    #######SCHEDULING ALGORITHM HANDLERS BELOW THIS LINE####
    #   These should all manipulate the state of the processor
    #   based on their respective algorithms.
    #
    #   THIS SHOULD BE THE ONLY PLACE A CONTEXT SWITCH HAPPENS
    #
    #
    ########################################################
    def step(self):

        return

    def handle_FCFS(self):

        if (self.processor.cProc is None and (self.processor.workQ.isEmpty())):
            pass

        #Go to discord if u rhere
        rc = self.processor.procHelper.procReady()
        if( rc == True):
            self.processor.cSwitcher.contextSwitch()

        elif(rc == False):
            return
        else:
            #Simulation ended so idrk what's
            self.processor.procHelper.finalize()
            return
