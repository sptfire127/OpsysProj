#Test suite for project
from classes import *
from pprint import pprint
import random



def main():
    myProccessor = Processor(cSwitchTime=10, algorithm="FCFS")

    for i in range(0, 5):
        #Set up initial
        q = Process(label=i, arrival=random.randint(0, 25), burst=random.randint(1, 25), burstCount=random.randint(1, 25), IOtime= random.randint(0, 0))
        print(q)
        myProccessor.addProc(q)

    myProccessor.run(-1)












if __name__ == "__main__":
    main()
