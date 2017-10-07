#Test suite for project
from classes import *
from pprint import pprint



def main():
    myProccessor = Processor(cSwitchTime=10, algorithm="FCFS")

    for i in range(0, 10):
        q = Process(label=1, arrival=i+2, burst=i*2, burstCount=10, IOtime= 13)
        myProccessor.addProc(q)
    print(myProccessor)











if __name__ == "__main__":
    main()
