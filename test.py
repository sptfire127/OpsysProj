#Test suite for project
from classes import *
from pprint import pprint
import random



def main():
    myProccessor = Processor(cSwitchTime=10, algorithm="FCFS")

    for i in range(0, 3):
        #Set up initial
        q = Process(label=i, arrival=random.randint(0, 5), burst=random.randint(5, 5), burstCount=random.randint(3, 3), IOtime= random.randint(5,10))
        print(q)
        myProccessor.addProc(q)

    myProccessor.run(-1)












if __name__ == "__main__":
    main()
