'''
This module expands the given patent query with the terms collected from
the top 10 of Google patent search.
'''

import nltk
import json
import urllib
import urllib2
import HTMLParser
import string

def expand(query):
    url = 'https://ajax.googleapis.com/ajax/services/search/patent?v=1.0&rsz=3&q=' + urllib.quote(query)
    response = json.load(urllib2.urlopen(url))
    results  = response['responseData']['results']

    for result in results:
        output = result['titleNoFormatting'].encode('ascii', 'ignore')
        output = ''.join(ch for ch in output if ch not in string.punctuation)
        query += ' ' + output

    return query

def get_nouns(sentence):
    nouns = []
    results = nltk.pos_tag(sentence.strip().split())

    for result in results:
        if result[1][:1] == 'N' and result[0] != 'documents':
            nouns.append(result[0])

    return ' '.join(nouns)

#print get_nouns('Washers that clean laundry with bubbles elevant documents will describe washing technologies that clean or induce using bubbles, foam, by means of vacuuming, swirling, inducing flow or other mechanisms')