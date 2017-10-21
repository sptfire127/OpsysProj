from Processor import *
from Process import *
from pprint import pprint
import random
from output import *
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
            t = Process(myProcessor, label, arrivalTime, burst, bCount, ioTime)
            myProcessor.procHelper.addProc(t)
    myProcessor.procHelper.run(-1)

if __name__ == "__main__":
    main(8, "FCFS", 0)
    writeOutput("\n", 0, 0)
    main(8, "SRT", 0)
    #writeOutput("\n\n", 0, 0)
    #main(8, "RR", 70)
