from classes import *
from pprint import pprint
import random

def main():

    myProccessor = Processor(cSwitchTime=4, algorithm="FCFS")

    test = open("test.txt", "r+")

    for line in test:
        if(line[0] != "#"):
            line = line.replace("\n", "")
            line = line.split("|")
            label = line[0]
            arrivalTime = int(line[1])
            burst = int(line[2])
            bCount = int(line[3])
            ioTime = int(line[4])
            t = Process(label, arrivalTime, burst, bCount, ioTime)
            myProccessor.addProc(t)
            myProccessor.totalBurstCount += bCount

    print(myProccessor.totalBurst)


    myProccessor.run(-1)


if __name__ == "__main__":
    main()
