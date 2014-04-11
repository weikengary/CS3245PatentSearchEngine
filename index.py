import glob
import getopt
import sys
import os
import cPickle
import math
import shutil
from collections import defaultdict
from DictEntry import dict_entry
from PreprocessUtils import PreprocessUtils
from collections import Counter
intermediate_directory_name = 'intermediate_posting_list' #place to store intermediate(individual) posting list



def translate_ipc(ipc_subclass_number, ipc_dict):
    if ipc_dict.has_key(ipc_subclass_number):
        return ipc_dict[ipc_subclass_number]
    elif ipc_dict.has_key(ipc_subclass_number[0:3]):
        return ipc_dict[ipc_subclass_number[0:3]] #if we don't find the corresponding entry for the ipc subclass number, check for the ipc class number
    else:
        return None

def get_zone_name(tag_name):
    if(tag_name.lower() == 'title'):
        return 'title'
    elif(tag_name.lower() == 'abstract'):
        return 'description'
    elif(tag_name.lower() == 'ipc subclass'):
        return 'category'
    else:
        return ""
    
def index_document(dictionary, preprocess_utils, filepath, docZoneList, ipc_dict, doc_length_dict):
    docID = os.path.basename(os.path.splitext(filepath)[0])
    temp_posting_list = {} #store temporary posting list in the following format {term: "docID1.title\tdocID2.title\tdocID2.description ...", ...} later it will be dumped to a temp file
    term_freq_list = defaultdict(int) #store temp term freq for calculating the document length
    #traverse all tag names
    for tag_name in docZoneList:
        #however, we only concern for title, description(abstract), and category
        if(tag_name.lower() == 'title' or tag_name.lower() == 'abstract' or tag_name.lower() == 'ipc subclass'):
            #translate the value of ipc number to its description
            if(tag_name.lower() == 'ipc subclass'):
                content = translate_ipc(docZoneList[tag_name], ipc_dict)
            #if it is title/abstract, no need for translation here, just use its value for the content
            else:
                content = docZoneList[tag_name]
            #content will be none for ipc number translation, if we can not find the corresponding mapping, checking here for safety reason
            if(content != None):
                word_list = preprocess_utils.LinguisticParser(content)
                zone_name = get_zone_name(tag_name)
                for term in word_list:
                    term_freq_list[term+zone_name] += 1 #add term freq to term freq list for each term,zone_name pairs (later will be used to calculate the document length)
                    if not temp_posting_list.has_key(term):
                        #create entry in dictionary if it isn't in the dictionary yet
                        if not dictionary.has_key(term):
                           dictionary[term] = dict_entry()
                        #create entry in temp_posting_list
                        temp_posting_list[term] = docID+'.'+zone_name + ' '
                    else:
                        #add entry to temp_posting_list
                        temp_posting_list[term] += docID+'.'+zone_name + ' '
    #write temp file
    for term in temp_posting_list:
        filepath = intermediate_directory_name+'/'+term
        temp_file = file(filepath,'a')
        temp_file.write(temp_posting_list[term])
        temp_file.close()

    #calculate the document length 
    doc_length = 0
    for key in term_freq_list:
        doc_length += pow(term_freq_list[key],2)
    doc_length = math.sqrt(doc_length)
    doc_length_dict[docID] = doc_length

def format_posting_list(filepath, doc_length_dict):
    f = open(filepath, 'r')
    formatted_posting_list = {} #our posting list format will be {docID1 : {title : title_weight, description : description_weight, category : category_weight}, docID2 : ..., ...}
    #weight in our case is tf*idf/doc_length
    docID_list = (f.read()).split(' ')
    f.close()
    docID_list.remove('') #remove any extra element (empty string)
    for docIDWithZone in docID_list:
        docID = docIDWithZone.split('.')[0]
        zone_name = docIDWithZone.split('.')[1]
        #case when the new posting list doesn't have any corresponding entry, create new entry
        if(not formatted_posting_list.has_key(docID)):
            formatted_posting_list[docID] = {}
            formatted_posting_list[docID][zone_name] = 1 #assign the tf to docID.zone_name
        #case when the new posting list has the corresponding entry, update the entry
        else:
            #case when the corresponding zone name (title/description/category) hasn't exist in the new posting list
            if not formatted_posting_list[docID].has_key(zone_name):
                formatted_posting_list[docID][zone_name] = 1 #assign the tf value
            else:
                formatted_posting_list[docID][zone_name] += 1 #update the tf value

    #calculate the weight for each docID, zone_name
    doc_freq = len(formatted_posting_list)
    for docID in formatted_posting_list:
        for zone_name in formatted_posting_list[docID]:
            term_freq = formatted_posting_list[docID][zone_name]
            formatted_posting_list[docID][zone_name] = get_tf_idf(term_freq, doc_freq) #calculate tf-idf
            formatted_posting_list[docID][zone_name] /= doc_length_dict[docID] #normalize it
    return formatted_posting_list

def get_tf_idf(term_freq, doc_freq):
    tf = 1 + math.log10(term_freq)
    idf = math.log10(float(collection_size) / doc_freq)
    return tf * idf

def merge_posting_list(dictionary, posting_file, doc_length_dict):
    print 'merging'
    postings_stream = file(posting_file,'w')
    list_of_intermediate_posting_list = os.listdir(intermediate_directory_name)
    for filename in list_of_intermediate_posting_list:
        print 'merging ' + filename + ' with postings.txt'
        if (not(filename == '.DS_Store')):
            filepath = intermediate_directory_name + '/' + filename
            posting_list = format_posting_list(filepath, doc_length_dict)

            #update the dictionary with writing location (pointer) and the document frequency
            dictionary[filename].posting_pointer = postings_stream.tell()
            dictionary[filename].doc_freq = len(posting_list)

            #dump the posting list to the postings.txt using cPickle
            cPickle.dump(posting_list, postings_stream)
    shutil.rmtree(intermediate_directory_name)
    postings_stream.close()
            
'''
This function reads, call the process function, finally writes to respective file.
'''
def main(file_i,file_d,file_p):
    files = glob.glob(file_i+"*")
    global collection_size
    collection_size = len(files)
    p = PreprocessUtils()
    ipc_dict = p.IPCCodeCategoryParser()

    dictionary = {} #dictionary that later will be stored to dictionary.txt with cPickle
    doc_length_dict = {} #dictionary to store the length of each document for length normalization later
    if not os.path.exists(intermediate_directory_name):
            os.makedirs(intermediate_directory_name) #temp directory to store temporary posting list
    for singleFile in files:
        docID = os.path.basename(os.path.splitext(singleFile)[0])
        #parse and index single document
        print 'parsing ' + docID
        docZoneList, docWordList = p.XMLPatentDocParser(singleFile)
        index_document(dictionary, p, singleFile, docZoneList, ipc_dict, doc_length_dict)

    #merge temporary posting list together
    merge_posting_list(dictionary, file_p, doc_length_dict)

    #dump dictionary to dictionary.txt
    dictionary_stream = open(file_d, 'w')
    cPickle.dump(dictionary, dictionary_stream)
    doc_count = collection_size
    cPickle.dump(doc_count, dictionary_stream)
    dictionary_stream.close()

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
