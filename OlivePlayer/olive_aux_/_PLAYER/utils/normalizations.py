#utils normalizations file
import sys


#remove trailing 0s
def removeLeading0s(string):
    return int(string.lstrip("0"))