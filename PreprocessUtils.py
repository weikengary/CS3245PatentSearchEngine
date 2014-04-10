import nltk
from xml.dom import minidom
import csv
import re
from nltk.stem.snowball import SnowballStemmer

class PreprocessUtils():

    def __init__(self):
        self.porterStemmer = nltk.PorterStemmer()
        self.stopwordsList = nltk.corpus.stopwords.words("english")
        self.wordNetLemmatizer = nltk.WordNetLemmatizer()
        
    def XMLQueryParser(self,fileName):
        xmldoc = minidom.parse(fileName)
        title = xmldoc.getElementsByTagName('title')[0].firstChild.data.encode('utf-8')
        description = xmldoc.getElementsByTagName('description')[0].firstChild.data.encode('utf-8')
        return self.POSTagger(title.strip().split()), self.POSTagger(description.strip().split())

    def XMLPatentDocParser(self,fileName):
        xmldoc = minidom.parse(fileName)
        docZoneList = {}
        docWordList = []
        for node in xmldoc.getElementsByTagName('str'):
            if node.firstChild is not None:
                tagName = str(node.attributes.item(0).value.encode('utf-8')) # get the attribute name for str
                tagValue = str(node.firstChild.nodeValue.encode('utf-8')).strip() # get the value of the attribute
            docZoneList[tagName] = tagValue
            docWordList.append(tagValue)
        return docZoneList, docWordList

    def LinguisticParser(self, sentence):
        ls = re.split('\W',sentence)
        #ls = nltk.pos_tag(ls)
        cleanup = []
        for l in ls:
            if l not in self.stopwordsList:
                if len(l)>3:
                    l = self.wordNetLemmatizer.lemmatize(self.porterStemmer.stem(l.lower()))
                if len(l)>2:
                    cleanup.append(l)
        return cleanup
    
    def IPCCodeCategoryParser(self):
        IPCCodeDictionary = {}
        with open('IPC-codes/codes.csv', 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for r in reader:
                if len(r[0]) > 1 and len(r[1])>1:
                    IPCCodeDictionary[r[0]] = (r[1]).strip()
        return IPCCodeDictionary 
    
    
    def POSTagger(self, list):
        ls = nltk.pos_tag(list)
        nonVerbSet = []
        verbSet = []
        for w in ls:
            # tags from https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
            if w[1] != 'VBG' and w[1] != 'VBN' and w[1]!= 'V' and w[1]!='VB' and w[1]!='VBD' and w[1]!='VBP' and w[1]!= 'VBZ':
                nonVerbSet.append(w[0])
            else:
                verbSet.append(w[0])
        if len(nonVerbSet) != 0:
            return " ".join(nonVerbSet)
        else:
            return " ".join(verbSet)

#print(SnowballStemmer("porter").stem("washer"))
#preprocessor = PreprocessUtils()
#preprocessor.POSTagger(['car','feed', 'are', 'doing','run'])
#preprocessor.IPCCodeCategoryParser()
#title, description = preprocessor.XMLQueryParser('query/q1.xml')
#print "title: " + title
#print "description: " + description
#preprocessor.XMLPatentDocParser('patsnap-corpus/EP0049154B2.xml')
#preprocessor.LinguisticParser(list)
