#Test suite for project
from classes import *
from pprint import pprint



def main():
    myProccessor = Processor(cSwitchTime=10, algorithm="FCFS")

    for i in range(0, 10):
        #Set up initial
        q = Process(label=i, arrival=0, burst=i*2, burstCount=2, IOtime= i*2 + 12)
        myProccessor.addProc(q)

    print(myProccessor)
    for i in range(0, 100000):
        print("\n==============Execution {0}==============\n".format(i))
        myProccessor.step()
        if(myProccessor.finished()):
            print("Done.")
            break

        if(True):#i % 10 == 0): <- Change this to print every 10 executions
            print("RAN INTERATION {0}".format(i))
            print(myProccessor)
            myProccessor.qprint()

        print("\n===============================\n")












if __name__ == "__main__":
    main()
