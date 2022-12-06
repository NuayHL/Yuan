import os

def getext(name):
    return os.path.splitext(name)[1]

def getbase(name):
    return os.path.basename(name)

def getori(name):
    return os.path.splitext(os.path.basename(name))[0]

def abspath(name):
    return os.path.abspath(name)