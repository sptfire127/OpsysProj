




simoutf = open("./output/simout.txt", "w+")
outputf = open("./output/output.txt", "w+")
debugf = open("./output/debug.txt", "w+")




def writeSimout(output=""):
    global simoutf
    simoutf.write(output)

def writeOutput(output=""):
    global outputf
    outputf.write(output)

def writeDebug(output=""):
    global debugf
    debugf.write(output)
