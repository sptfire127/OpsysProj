import sys

simoutf = open(sys.argv[2], "w+")

outputf = open("./output/output.txt", "w+")
outBuf = []


def writeSimout(output=""):
    global simoutf
    simoutf.write(output)


#          0      1
# Event : "IO" | "CPU" |
def writeOutput(output=None, label=None, event=None):
    global outBuf
    # Will always be ordered to label
    if (output is None):
        lst = []
        for t in outBuf:
            if (t[2] == 0):
                lst.append(t)
                outBuf.remove(t)
        outBuf.extend(lst)
#        print(outBuf)

        out = ""
        for tup in outBuf:
            out += tup[0]
        __writeOutput(out)
        outBuf = []
        return

    if (len(outBuf) == 0):
        outBuf = [(output, label, event)]
        return

    t = (output, label, event)

    if not t in outBuf:
        outBuf.append((output, label, event))

    return


def __writeOutput(output=""):
    global outputf
    outputf.write(output)


def evenCPU():
    return 1


def evenIO():
    return 0
