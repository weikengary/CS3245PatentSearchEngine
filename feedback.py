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

def write_result(file_path, index):
    preprocessor = PreprocessUtils()
    tagValues, words = preprocessor.XMLPatentDocParser(file_path)
    codeValues = preprocessor.IPCCodeCategoryParser()

    with open(args.o, 'a') as output_file:
        output_file.write(str(index) + '. ')
        for tagName, content in tagValues.iteritems():

            tagName = tagName.strip()
            content = content.strip()

            if tagName == 'Patent Number':
                output_file.write(content)
                output_file.write('\n')
            elif tagName == 'Title':
                output_file.write('Title    :' + content)
                output_file.write('\n')
            elif tagName == 'Abstract':
                output_file.write('Abstract :' + content)
                output_file.write('\n')
            elif tagName == 'IPC Subclass':
                output_file.write('Subclass :' + content + ' - ' + codeValues.get(content, ''))
                output_file.write('\n')

        output_file.write('\n')




get_args()
if os.path.isfile(args.o):
    os.remove(args.o)

with open(args.r) as result_file:
    i = 1
    for doc_id in result_file:
        doc_id_path = os.path.join('patsnap-corpus', doc_id.strip() + '.xml')
        write_result(doc_id_path, i)
        i += 1
