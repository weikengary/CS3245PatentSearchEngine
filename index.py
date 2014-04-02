import glob
import getopt
import sys
import os
from PreprocessUtils import PreprocessUtils
from collections import Counter

'''
This function reads, call the process function, finally writes to respective file.
'''
def main(file_i,file_d,file_p):
    files = glob.glob(file_i+"/*")
    p = PreprocessUtils()
    tokenSet = []
    for singleFile in files:
        docID = os.path.basename(os.path.splitext(singleFile)[0])
        docZoneList, docWordList = p.XMLPatentDocParser(singleFile)
        docWordList = p.LinguisticParser(docWordList)
    print docWordList
    return True

def usage():
    print "usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file"

file_i = file_d = file_p = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-i':
        file_i = a
    elif o == '-d':
        file_d = a
    elif o == '-p':
        file_p = a
    else:
        assert False, "unhandled option"
if file_i == None or file_d == None or file_p == None:
    usage()
    sys.exit(2)

main(file_i, file_d, file_p)
