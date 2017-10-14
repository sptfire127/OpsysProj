#Test suite for project
from classes import *
from pprint import pprint
import random



def main():
    myProccessor = Processor(cSwitchTime=10, algorithm="SRT")


    for i in range(1, 6):
        #Set up initial
        q = Process(label=i, arrival=i, burst=random.randint(25, 30), burstCount=5, IOtime=10)
        print(q)
        myProccessor.addProc(q)
    q = Process(label=9, arrival=0, burst=5, burstCount=5, IOtime=10)
    myProccessor.addProc(q)
    
    myProccessor.run(-1)












if __name__ == "__main__":
    main()
