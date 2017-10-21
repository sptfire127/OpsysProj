import sys
from operator import itemgetter

simoutf = open(sys.argv[2], "w+")

outputf = open("./output/output.txt", "w+")
outBuf = []


def writeSimout(output=""):
    global simoutf
    simoutf.write(output)


#          0      1
#Event : "IO" | "CPU" |
def writeOutput(output=None, label=None, event=None):
    global outBuf
    #Will always be ordered to label
    #### FLUSH THE BUFFER #################
    if(output is None):
        lst = []
        rmLst = []
        for t in outBuf:
            if(t[2] == 0):
                lst.append(t)
                rmLst.append(t)
        for t in rmLst:
            outBuf.remove(t)

        if(len(outBuf) != 0):
            #print("out: " + str(outBuf))
            #print("lst: " + str(lst))
            pass

        #Sort bsed on the second element of tup
        outBuf.sort(key=itemgetter(1), reverse=False)
        lst.sort(key=itemgetter(1), reverse=False)

        if(len(outBuf) != 0):
            #print("out: " + str(outBuf))
            #print("lst: " + str(lst))
            pass

        outBuf.extend(lst)
        if(len(outBuf) != 0):
            #print("out: " + str(outBuf))
            pass
        out = ""
        for tup in outBuf:
            out += tup[0]
        __writeOutput(out)
        outBuf = []
        return
    ################################
    # PUT NEW DATA INTO BUFFER
    if(len(outBuf) == 0):
        outBuf = [(output, label, event)]
        return
    t = (output, label, event)
    if not t in outBuf: #PRESERVE UNIQUE OUTPUT
        outBuf.append((output, label, event))


def __writeOutput(output=""):
    global outputf
    #if(output != ""):
    #    #print(output)
    outputf.write(output)


def evenCPU():
    return 1


def evenIO():
    return 0
