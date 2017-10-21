from Processor import *
from Process import *
from pprint import pprint
import random
from output import *
from output import __writeOutput
import sys

def main(cs, algo, time):
    myProcessor = Processor(cSwitchTime=cs, algorithm=algo, tSlice=time)

    test = open(sys.argv[1], "r+")

    for line in test:
        if (line[0] != "#" and len(line) != 1):
            line = line.replace("\n", "")
            line = line.split("|")
            label = line[0]
            arrivalTime = int(line[1])
            burst = int(line[2])
            bCount = int(line[3])
            ioTime = int(line[4])
            t = Process(label, arrivalTime, burst, bCount, ioTime)
            myProcessor.procHelper.addProc(t)
    myProcessor.procHelper.run(-1)

if __name__ == "__main__":
    main(8, "FCFS", 0)
    __writeOutput("\n")
    main(8, "SRT", 0)
    __writeOutput("\n")
    #main(8, "RR", 70)
