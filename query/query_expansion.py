'''
This module expands the given patent query with the terms collected from
the top 10 of Google patent search.
'''

import json
import urllib
import urllib2

query = urllib.quote('Biological Waste Water Treatment')
response = json.load(urllib2.urlopen('https://ajax.googleapis.com/ajax/services/search/patent?v=1.0&rsz=8&q=' + query))
results = response['responseData']['results']
for result in results:
    print result
