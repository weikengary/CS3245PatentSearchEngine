import nltk
from xml.dom import minidom
import csv
import re

class PreprocessUtils():

    def __init__(self):
        self.porterStemmer = nltk.PorterStemmer()
        self.stopwordsList = nltk.corpus.stopwords.words("english")
        self.wordNetLemmatizer = nltk.WordNetLemmatizer()
        
    def XMLQueryParser(self,fileName):
        xmldoc = minidom.parse(fileName)
        title = xmldoc.getElementsByTagName('title')[0].firstChild.data.encode('utf-8')
        description = xmldoc.getElementsByTagName('description')[0].firstChild.data.encode('utf-8')
        return title.strip(), description.strip()
    
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
    
#preprocessor = PreprocessUtils()
#preprocessor.IPCCodeCategoryParser()
#title, description = preprocessor.XMLQueryParser('query/q1.xml')
#print "title: " + title
#print "description: " + description
#preprocessor.XMLPatentDocParser('patsnap-corpus/EP0049154B2.xml')
#preprocessor.LinguisticParser(list)
