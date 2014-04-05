import glob
import getopt
import sys
import os
import cPickle
from PreprocessUtils import PreprocessUtils
from collections import Counter
intermediate_directory_name = 'intermediate_posting_list' #place to store intermediate(individual) posting list


#define custom class for the entry in dictionary
class dict_entry:
    doc_freq = None
    posting_pointer = None

def index_document(dictionary_file, posting_file, preprocess_utils, filepath, docZoneList):
    docID = os.path.basename(os.path.splitext(filepath)[0])
    dictionary = {} #dictionary to be stored later in dictionary.txt with cPickle
    temp_posting_list = {} #store temporary posting list in the following format {term: "docID1.title\tdocID2.title\tdocID2.description ...", ...} later it will be dumped to a temp file
    #traverse all tag names
    for tag_name in docZoneList:
        #however, we only concern for title, description(abstract), and category
        if(tag_name.lower() == 'title' or tag_name.lower() == 'abstract' or tag_name.lower() == 'category'):
            content = docZoneList[tag_name]
            word_list = preprocess_utils.LinguisticParser(content)
            for term in word_list:
                if not temp_posting_list.has_key(term):
                    #create entry in dictionary
                    dictionary[term] = dict_entry()
                    #create entry in temp_posting_list
                    temp_posting_list[term] = docID.tag_name
                else:
                    #add entry to temp_posting_list
                    temp_posting_list[term] += '\t' + docID.tag_name
                    
    #write temp file
    for term in temp_posting_list:
        f = file(intermediate_directory_name+'/'+term,'a')
        cPickle(temp_posting_list[term], f)
        f.close()
            
'''
This function reads, call the process function, finally writes to respective file.
'''
def main(file_i,file_d,file_p):
    files = glob.glob(file_i+"*")
    p = PreprocessUtils()
    tokenSet = []
    for singleFile in files:
        docID = os.path.basename(os.path.splitext(singleFile)[0])
        #parse single document
        docZoneList, docWordList = p.XMLPatentDocParser(singleFile)
        docWordList = p.LinguisticParser(docWordList)
        #index single document
        index_document(file_d, file_p, p, singleFile, docZoneList)
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
