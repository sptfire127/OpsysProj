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
"""
        # I removed that earlier idk if I was supposed to

        # If cProc became blocked (from calling cProc.step()), swap it out for new process in workQ
        # CONTEXT SWITCH
        elif(self.processor.cProc.state == "BLOCKED"):
            if (self.processor.cProc.burstCount != 1):
                # Next time to pre-empt is now + the time slice + context switch time
                writeOutput(
                    "time {0}ms: Process {1} completed a CPU burst; {2} bursts to go {3}\n".format(int(self.processor.rTime),
                                                                                                   self.processor.cProc.label,
                                                                                                   self.processor.cProc.burstCount,
                                                                                                   self.processor.procPrinter.getQStr()))
            else:
                # Next time to pre-empt is now + the time slice + context switch time
                writeOutput(
                    "time {0}ms: Process {1} completed a CPU burst; {2} burst to go {3}\n".format(int(self.processor.rTime),
                                                                                                  self.processor.cProc.label,
                                                                                                  self.processor.cProc.burstCount,
                                                                                                  self.processor.procPrinter.getQStr()))
            self.processor.procHelper.logBurst()

            # Make sure IO does not start right away, stall it for half a context switch
            #self.processor.cProc.IOtimeLeft += self.processor.cSwitchTime / 2
            writeOutput("time {0}ms: Process {1} switching out of CPU; will block on I/O until time {2}ms {3}\n".format(
                int(self.processor.rTime), self.processor.cProc.label, int(self.processor.cProc.IOtimeLeft + (self.processor.rTime) + (self.processor.cSwitchTime / 2)),
                self.processor.procPrinter.getQStr()))

            #self.cSwitcher.contextSwitch() #Wut idk LOL
            self.processor.cSwitcher.contextSwitch()


        # Process is running ... Continue
        # TODO :    WE SHOULD ADD PREMPTION LOGIC HERE TO DETERMINE IF WE NEED TO
        #           CONTEXT SWITCH, THIS SHOULD COVER ALL SUPPORTED ALGORITHMS
        #
        # Process is running ... Continue
        # TODO :    WE SHOULD ADD PREMPTION LOGIC HERE TO DETERMINE IF WE NEED TO
        #           CONTEXT SWITCH, THIS SHOULD COVER ALL SUPPORTED ALGORITHMS
        #
        elif (self.processor.cProc.state == "RUNNING"):
            if (self.processor.procHelper.procReady()):
                if (self.processor.algorithm == "RR"):
                    #self.processor.nxtSlice = self.processor.rTime + self.processor.tSlice + self.processor.cSwitchTime
                    if (self.processor.workQ.isEmpty()):
                        self.processor.nxtSlice = self.processor.rTime + self.processor.tSlice
                        writeOutput(
                            "time {0}ms: Time slice expired; no preemption because ready queue is empty {1}\n".format(
                                int(self.processor.rTime), self.processor.procPrinter.getQStr()))
                    else:
                       # self.processor.nxtSlice = self.processor.rTime + self.processor.tSlice + self.processor.cSwitchTime
                        self.processor.cSwitcher.contextSwitch()
                if (self.processor.algorithm != "RR"):
                    self.cSwitcher.contextSwitch()

                    # Continue running process

        # Process is finished
        elif (self.processor.cProc.isFinished()):
            self.processor.donePool.append(self.processor.cProc)
            writeOutput("time {0}ms: Process {1} terminated {2}\n".format(int(self.processor.rTime), self.processor.cProc.label,
                                                                          self.processor.procPrinter.getQStr()))
            self.processor.procHelper.logBurst()

           # Next time to pre-empt is now + the time slice + context switch time
            #self.processor.nxtSlice = self.processor.rTime + self.processor.tSlice + self.processor.cSwitchTime

            # Call step even though we're done so the process can calculate final
            # average statistics
            self.processor.cProc.step()

            # Check to see if we are finished. If so, return.
            if (self.processor.procHelper.finished()):
                return

            # Do we have a next process ?
            elif (not self.processor.workQ.isEmpty()):
                self.cSwitcher.contextSwitch()

            # No next proc, just pass.
            else:
                self.processor.cProc = None

        else:
            raise RuntimeError("ERROR IN PROCESSOR HANDLER, I HAVE PRINTED MY STATE")

    def handle_SRT(self): disc
        # TODO
        pass

    def handle_RR(self):
        # TODO
        pass
        #######SCHEDULING ALGORITHM HANDLERS ABOVE THIS LINE####
"""
