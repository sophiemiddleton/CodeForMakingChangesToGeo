import os, sys, subprocess

# root macro run format
# root -l "macro.C+(arg1,arg2,arg3,...,argn)"

def argConversion(arg):
    if type(arg) in [float, int]:
        return str(arg)
    elif type(arg) in [str]:
        return '"' + arg + '"'
    else:
        return '"' + str(arg) + '"'

def argConnection(arglist=[]):
    if not (arglist is [] or arglist is None):
        shellargv = list(arglist) 
        arglist_conv = list()
        for arg in arglist:
            arglist_conv.append(argConversion(arg))
        return '('+','.join(arglist_conv)+')'
    else:
        return ''

def runMacro(macroName, arglist=None, splash=False, interprete=False, batch=True):
    shellCommand = ['root']
    if interprete is False:
        shellCommand.append("-q")
    if splash is False:
        shellCommand.append("-l")
    if batch is True:
        shellCommand.append("-b")
    shellCommand.append(macroName+argConnection(arglist))
    print("Run Macro", shellCommand)
    a = subprocess.Popen(shellCommand)
    return a

def main():
    for i in range(1):
    a = runMacro('.C', arglist=[1,"test"])
    a.wait()


if __name__ == "__main__":
    main()
