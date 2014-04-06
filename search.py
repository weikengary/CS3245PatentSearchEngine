import cPickle
import pickle
import sys
from PreprocessUtils import PreprocessUtils
from argparse        import ArgumentParser
from DictEntry       import dict_entry

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

def main():
    init()

def get_args():
    parser = ArgumentParser()
    parser.add_argument('-d', help = 'dictionary file')
    parser.add_argument('-p', help = 'postings file')
    parser.add_argument('-q', help = 'query file')
    parser.add_argument('-o', help = 'output of file of results')
    args = parser.parse_args()

    if len(sys.argv) != 9:
        parser.print_help()
        sys.exit(1)

    return args

def init():
    args = get_args()

    dict_file     = open(args.d, 'r')
    postings_file = open(args.p, 'r')
    query_file    = open(args.q, 'r')
    output_file   = open(args.o, 'w')

    dictionary = pickle.load(dict_file)
    print 'hello'

# Start search.py
main()