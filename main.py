from classes import *
from pprint import pprint
import random



def main():
    myProccessor = Processor(cSwitchTime=8, algorithm="RR", tSlice=70)


    f = "test1.txt"#input("Enter a file name: ./tests/")

    test = open("./tests/" + f, "r+")

    for line in test:
        if(line[0] != "#"):
            line = line.replace("\n", "")
            line = line.split(sep="|")
            label = line[0]
            arrivalTime = int(line[1])
            burst = int(line[2])
            bCount = int(line[3])
            ioTime = int(line[4])
            t = Process(label, arrivalTime, burst, bCount, ioTime)
            print(t)
            myProccessor.addProc(t)




    myProccessor.run(-1)


if __name__ == "__main__":
    main()
