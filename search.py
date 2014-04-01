#!/usr/bin/python
import getopt
import sys
import string
import nltk
import heapq
import math
import linecache

import math

'''
TASKS
-----
1. Read the Query
2. Query XML Parser
3. Query Linguistic Parser
4. Spell Correction, Query Expansion
5. Scoring and Ranking
6. Results
'''


'''
This function reads, call the process function, finally writes to respective file.
'''
def main(file_d,file_p,file_q,file_o):
    return True
    
def usage():
    print "usage: " + sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results"

file_d = file_p = file_q = file_o = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-d':
        file_d = a
    elif o == '-p':
        file_p = a
    elif o == '-q':
        file_q = a
    elif o == '-o':
        file_o = a
    else:
        assert False, "unhandled option"
if file_d == None or file_p == None or file_q == None or file_o == None:
    usage()
    sys.exit(2)

main(file_d,file_p,file_q,file_o)
