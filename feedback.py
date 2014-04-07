from PreprocessUtils import PreprocessUtils
from argparse import ArgumentParser
from xml.dom import minidom
import os
import sys

# Get and validate command line arguments
def get_args():
    global args
    parser = ArgumentParser()
    parser.add_argument('-r', help = 'result file')
    parser.add_argument('-o', help = 'output')
    args = parser.parse_args()
    if len(sys.argv) != 5:
        parser.print_help()
        sys.exit(1)

def write_result(file_path):
    preprocessor = PreprocessUtils()
    tagValues, words = preprocessor.XMLPatentDocParser(file_path)
    codeValues = preprocessor.IPCCodeCategoryParser()

    with open(file_path, 'a') as output_file:
        for tagName, content in tagValues.iteritems():
            tagName = tagName.strip()
            content = content.strip()

            if tagName == 'Patent Number':
                output_file.write(content)
                output_file.write(os.linesep)
            elif tagName == 'Title':
                output_file.write('Title    :' + content)
                output_file.write(os.linesep)
            elif tagName == 'Abstract':
                output_file.write('Abstract :' + content)
                output_file.write(os.linesep)
            elif tagName == 'IPC Subclass':
                output_file.write('Subclass :' + content)
                output_file.write(os.linesep)

get_args()
query_file_path = os.path.join('query', args.r)
with open(query_file_path) as result_file:
    for doc_id in result_file:
        doc_id_path = os.path.join('patsnap-corpus', doc_id.strip() + '.xml')
        write_result(doc_id_path)
