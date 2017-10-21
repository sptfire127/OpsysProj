from Processor import *


class ProcessorPrinter:
    ########################################################
    ####### PRINTING FUNCTIONS BELOW THIS LINE #############
    proc = None

    def __init__(self, processor):
        self.proc = processor

    def getQStr(self):
        s = ""
        if (self.proc.workQ.isEmpty()):
            s = "[Q <empty>]"
        else:
            s += "[Q"
            for p in self.proc.workQ.queue:
                s += " "
                s += p.label
            s += "]"
        return s

    def __repr__(self):
        return str(vars(self.proc))

    def __str__(self):
        s = "PROC INFO:\ncSwitchTime : {0} ms\nRunTime : {1} ms\nworkQ Size : {2} processes\n".format(
            self.proc.cSwitchTime,
            int(self.proc.rTime),
            self.proc.workQ.size()) + \
            "procPool Size : {0} processes\nalgorithm : {1}\ncProc : {2}\n".format(self.proc.len(self.proc.procPool),
                                                                                   self.proc.algorithm,
                                                                                   self.proc.cProc)
        if (not (self.proc.tSlice is None)):
            s += "nxtSlice : {0} ms".format(self.proc.nxtSlice)

        return s
