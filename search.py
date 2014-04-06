import cPickle
import pickle
import sys
from math import log10
from math import sqrt
from math import pow
from operator  import itemgetter
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
    global args
    args    = get_args()
    query   = get_query()
    scores  = search(query)

    for score_tuple in scores:
        print '{: <19}({})'.format(score_tuple[0], score_tuple[1])
    print '{} matches found.'.format(len(scores))

    # To print without scores
    # -----------------------
    # for score_tuple in scores:
    #     print score_tuple[0]


# Get the weight of each field/zone. Normally we would want the sum
# of the weights of all field/zone to be equal to 1.
def get_zone_weights():
    weight = defaultdict()
    weight['title']       = 0.40
    weight['description'] = 0.40
    weight['category']    = 0.20
    return weight;

# Get and validate command line arguments
def get_args():
    parser = ArgumentParser()
    parser.add_argument('-d', help='dictionary file')
    parser.add_argument('-p', help='postings file')
    parser.add_argument('-q', help='query file')
    parser.add_argument('-o', help='output of file of results')

    args = parser.parse_args()
    if len(sys.argv) != 9:
        parser.print_help()
        sys.exit(1)

    return args

# Get the query title and description from the xml query file
def get_query():
    query = defaultdict()
    preprocessor = PreprocessUtils()
    query['title'], query['description'] = preprocessor.XMLQueryParser(args.q)
    return query;

# Search for matching doc_ids using dictionary and postings and return scores for each document
# that match at least one query term
def search(query):
    scores = defaultdict(float)
    query_term_weights, query_normalization = process_query(query)
    doc_weights_squared = defaultdict(float)

    for query_term, query_term_weight in query_term_weights.iteritems():
        postings = get_postings(query_term)

        # Calculate score for each pair (query_term, doc_id)
        # and update the scores[doc_id] accumulator
        for doc_id, zone_frequencies in postings.iteritems():
            doc_weight      = get_doc_weight(query_term, zone_frequencies)
            scores[doc_id] += query_term_weight * doc_weight
            doc_weights_squared[doc_id] += pow(doc_weight, 2)

    doc_normalization = {doc_id: sqrt(sum) for doc_id, sum in doc_weights_squared.iteritems()}
    normalized_scores = normalize_score(scores, query_normalization, doc_normalization)
    sorted_scores     = sorted(normalized_scores.iteritems(), key = itemgetter(1), reverse=True)

    return sorted_scores;

# Process the query title and description and return the weight for each query term
def process_query(query):
    preprocessor = PreprocessUtils()
    # Concatenate the title and description in query. We may want to treat it differently though.
    query_terms  = preprocessor.LinguisticParser(query['title'] + ' ' + query['description'])
    query_term_freqs    = get_query_term_freqs(query_terms)
    query_term_weights  = get_query_term_weights(query_term_freqs)
    query_normalization = get_normalization_factor(query_term_weights)
    return query_term_weights, query_normalization

def get_doc_weight(query_term, zone_frequencies):
    weights    = get_zone_weights()
    doc_weight = get_tf_idf(query_term, zone_frequencies.get('title', 0))       * weights['title'] + \
                 get_tf_idf(query_term, zone_frequencies.get('description', 0)) * weights['description'] + \
                 get_tf_idf(query_term, zone_frequencies.get('category', 0))    * weights['category']
    return doc_weight


# Get a mapping of query_term -> frequency_in_the_query
# To be used for tf normalization
def get_query_term_freqs(query_terms):
    query_term_freq = defaultdict(int)
    for query_term in query_terms:
        query_term_freq[query_term] += 1
    return query_term_freq

# Get a mapping of query_term -> weight (uses tf-idf)
def get_query_term_weights(query_term_freqs):
    query_term_weights = dict()
    for query_term, query_term_freq in query_term_freqs.iteritems():
        query_term_weights[query_term] = get_tf_idf(query_term, query_term_freq)
    return query_term_weights

# Get (tf * idf) value for the term
def get_tf_idf(term, term_freq):
    dictionary, doc_count = get_dictionary()

    if term not in dictionary or term_freq < 1:
        return 0

    tf  = 1 + log10(term_freq)
    idf = log10(float(doc_count) / dictionary[term].doc_freq)
    return tf * idf

# Get the cosine normalization factor
def get_normalization_factor(weights):
    sum_of_squares = 0
    for weight in weights.itervalues():
        sum_of_squares += pow(weight, 2)
    return sqrt(sum_of_squares)

def normalize_score(scores, query_normalization, doc_normalization):
    normalized_scores = defaultdict(float)
    for doc_id, score in scores.iteritems():
        if query_normalization > 0 and doc_normalization[doc_id] > 0:
            normalized_scores[doc_id] = score / doc_normalization[doc_id] / query_normalization
        else:
            normalized_scores[doc_id] = score
    return normalized_scores


# Get the dictionary and doc_count from dictionary.txt
def get_dictionary():
    if 'dictionary' not in globals() or 'doc_count' not in globals():
        with open(args.d, 'r') as dictionary_file:
            # dictionary and doc_count are going to be reused again in search, so we set it to global
            global dictionary, doc_count
            dictionary = cPickle.load(dictionary_file)
            doc_count  = cPickle.load(dictionary_file)
    return dictionary, doc_count

def get_postings(query_term):
    dictionary, doc_count = get_dictionary()

    if query_term not in dictionary:
        return dict()

    with open(args.p, 'r') as postings_file:
        seek_location = dictionary[query_term].posting_pointer
        postings_file.seek(seek_location)
        return cPickle.load(postings_file)

# Start search.py
main()