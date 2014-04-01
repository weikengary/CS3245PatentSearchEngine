import glob
import getopt
import sys
import os
from PreprocessUtils import PreprocessUtils
from collections import Counter
'''
TASKS
-----
1. Read the documents
2. XML Parser
3. Linguistic Parsing of the documents
4 Indexers
    4a. Metadata in zone and field indexes
    4b. Inexact top K retrieval
    4c. Tiered inverted positional index
    4d. k-gram
5. Cache
'''
def extendCurrentTokenSet(tokenSet, docWordList, docID):
    docWordList.sort();
    counts = Counter(docWordList)
    tokenisedDoc = list(set(docWordList))
    for token in tokenisedDoc:
        tokenSet.append((token, int(docID), int(counts[token]))) # term, DocID, TermFreq in each Doc
    return tokenSet
'''
This function reads, call the process function, finally writes to respective file.
'''
def main(file_i,file_d,file_p):
    files = glob.glob(file_i)
    p = PreprocessUtils()
    tokenSet = []
    for singleFile in files:
        docID = os.path.basename(os.path.splitext(singleFile)[0])
        docZoneList, docWordList = p.XMLPatentDocParser(singleFile)
        docWordList = p.LinguisticParser(docWordList)
        tokenSet = extendCurrentTokenSet(tokenSet, docWordList, docID)
        print tokenSet
        break
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
