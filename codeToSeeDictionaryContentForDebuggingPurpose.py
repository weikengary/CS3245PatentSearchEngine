import cPickle

#define custom class for the entry in dictionary
class dict_entry:
    doc_freq = None
    posting_pointer = None
    
dictionary_stream = file('dictionary.txt','r')
dictionary = cPickle.load(dictionary_stream)
for key in dictionary:
    entry = dictionary[key]
    print 'key: ' + key
    print '\tdocument frequency: ' + str(entry.doc_freq) +   ', posting pointer: ' + str(entry.posting_pointer)
    print '---------------------------------------------------------------------------------'
dictionary_stream.close()
