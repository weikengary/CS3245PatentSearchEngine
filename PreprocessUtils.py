import nltk
from xml.dom import minidom

class PreprocessUtils():

    def __init__(self):
        self.porterStemmer = nltk.PorterStemmer()
        self.stopwordsList = nltk.corpus.stopwords.words("english")
        self.wordNetLemmatizer = nltk.WordNetLemmatizer()
        
    def XMLQueryParser(self,fileName):
        xmldoc = minidom.parse(fileName)
        title = xmldoc.getElementsByTagName('title')[0].firstChild.data
        description = xmldoc.getElementsByTagName('description')[0].firstChild.data
        return title.strip(), description.strip()
    
    def XMLPatentDocParser(self,fileName):
        xmldoc = minidom.parse(fileName)
        docZoneList = {}
        docWordList = []
        for node in xmldoc.getElementsByTagName('str'):
            if node.firstChild is not None:
                tagName = str(node.attributes.item(0).value) # get the attribute name for str
                tagValue = str(node.firstChild.nodeValue).strip() # get the value of the attribute
            docZoneList[tagName] = tagValue
            docWordList.append(tagValue)
        return docZoneList, docWordList
    
    '''
    Takes in a list and returns a normalized list:
         - porter stemming
         - lemmatize
         - and remove stopwords, 
         - remove words with len less than 3
    '''
    def LinguisticParser(self, ls):
        ls = nltk.word_tokenize(" ".join(ls))
        cleanup = []
        for l in ls:
            if l not in self.stopwordsList:
                if len(l)>3:
                    l = self.wordNetLemmatizer.lemmatize(self.porterStemmer.stem(l.lower()))
                if len(l)>2:
                    cleanup.append(l)
        return cleanup
    
preprocessor = PreprocessUtils()
title, description = preprocessor.XMLQueryParser('query/q1.xml')
print "title: " + title
print "description: " + description
#preprocessor.XMLPatentDocParser('patsnap-corpus/EP0049154B2.xml')
#preprocessor.LinguisticParser(list)