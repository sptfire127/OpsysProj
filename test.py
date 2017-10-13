#Test suite for project
from classes import *
from pprint import pprint
import random



def main():
    myProccessor = Processor(cSwitchTime=10, algorithm="SRT")

    for i in range(0, 5):
        #Set up initial
        q = Process(label=i, arrival=0, burst=random.randint(1, 25) * 5, burstCount=5, IOtime=i)
        print(q)
        myProccessor.addProc(q)

    myProccessor.run(-1)












if __name__ == "__main__":
    main()
