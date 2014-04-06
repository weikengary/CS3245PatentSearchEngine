import cPickle

posting_stream = file('postings.txt','r')
while True:
    try:
        posting = cPickle.load(posting_stream)
        for key in posting:
            print 'docID: ' + key
            for zone in posting[key]:
                print '\t' + zone + ' : ' + str(posting[key][zone])
        print '------------------------------------------------------------------'
    except (EOFError):
        break
    
posting_stream.close()
