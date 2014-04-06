import cPickle
import pickle
import sys
from math      import log10
from argparse  import ArgumentParser
from DictEntry import dict_entry
from collections     import defaultdict
from PreprocessUtils import PreprocessUtils

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
    get_args()
    query  = get_query()
    result = search(query)
    print result

def get_args():
    parser = ArgumentParser()
    parser.add_argument('-d', help='dictionary file')
    parser.add_argument('-p', help='postings file')
    parser.add_argument('-q', help='query file')
    parser.add_argument('-o', help='output of file of results')

    global args
    args = parser.parse_args()

    if len(sys.argv) != 9:
        parser.print_help()
        sys.exit(1)

# Get the weight of each field/zone. Normally we would want the sum
# of the weights of all field/zone to be equal to 1.
def get_weight():
    weight = defaultdict()
    weight['title']       = 0.5
    weight['description'] = 0.25
    weight['category']    = 0.25
    return weight;

# Get the query title and description from the xml query file
def get_query():
    query = defaultdict()
    preprocessor = PreprocessUtils()
    query['title'], query['description'] = preprocessor.XMLQueryParser(args.q)
    return query;

def search(query):
    query_term_weights = process_query(query)

    for query_term, query_term_weight in query_term_weights.iteritems():
        postings = get_postings(query_term)

# Process the query title and description and return the weight for each query term
def process_query(query):
    preprocessor = PreprocessUtils()
    query_terms  = preprocessor.LinguisticParser(query['title'] + ' ' + query['description'])
    query_term_freqs   = get_query_term_freqs(query_terms)
    query_term_weights = get_query_term_weights(query_term_freqs)
    return query_term_weights

# Get a mapping of query_term -> frequency_in_the_query
def get_query_term_freqs(query_terms):
    query_term_freq = defaultdict(int)
    for query_term in query_terms:
        query_term_freq[query_term] += 1
    return query_term_freq

# Get a mapping of query_term -> weight (uses tf-idf)
def get_query_term_weights(query_term_freqs):
    query_term_weights    = defaultdict()
    dictionary, doc_count = get_dictionary()

    for query_term, query_term_freq in query_term_freqs.iteritems():
        if query_term not in dictionary:
            query_term_weights[query_term] = 0
        else:
            tf  = 1 + log10(query_term_freq)
            idf = log10(float(doc_count) / dictionary[query_term].doc_freq)
            query_term_weights[query_term] = tf * idf

    return query_term_weights

def get_dictionary():
    if 'dictionary' not in globals() or 'doc_count' not in globals():
        with open(args.d, 'r') as dictionary_file:
            # dictionary and doc_count are going to be reused again in search, so we set it to global
            global dictionary, doc_count
            dictionary = cPickle.load(dictionary_file)
            doc_count  = cPickle.load(dictionary_file)
    return dictionary, doc_count




# Start search.py
main()
print 'hello'