#Test suite for project
from classes import *
from pprint import pprint



def main():
    myProccessor = Processor(cSwitchTime=10, algorithm="FCFS")

    for i in range(0, 5):
        #Set up initial
        q = Process(label=i, arrival=0, burst=5, burstCount=1, IOtime= 5)
        myProccessor.addProc(q)

    myProccessor.run(-1)



    print(myProccessor)
    myProccessor.statprint()









if __name__ == "__main__":
    main()
