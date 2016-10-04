import re
import os
import glob
import logging

log = logging.getLogger('cophi_toolbox.convert_corpusfile')
log.addHandler(logging.NullHandler())

# To enable logger, uncomment the following three lines.
#logging.basicConfig(level=logging.INFO,
#                    format='%(asctime)s %(levelname)s %(name)s: %(message)s',
#                    datefmt='%d-%b-%Y %H:%M:%S')

def makeCorpusFile(inDir : str,  outFileName : str) -> None:
    
    """Converts a folder of text documents to a single text file with one document per line
    
    Keyword arguments:
    inDir -- directory containing text documents
    outFileName -- prefered name of the output corpusfile
    """
    
    log.info('writing corpusfile ...')
    
    mastercorpus = os.path.join(os.getcwd(), outFileName)
    
    with open(mastercorpus, 'w', encoding = "utf-8") as data:
        inPath = os.path.join(os.getcwd(), inDir)
        folder = glob.glob(os.path.join(inPath, "*.txt"))
        filenames = []
        for i, text in enumerate(folder):
            with open(text, 'r', encoding = "utf-8") as content:
                textline = [re.sub(r'\\n\\r', '', document) for document in ' '.join(content.read().split())]
                filenames.append(os.path.splitext(os.path.basename(text))[0])
                if i != len(folder) - 1:
                    data.write("".join(textline) + "\n")
                else:
                    data.write("".join(textline) + "\n" + ",".join(filenames))
    
    log.info('corpusfile written successfully')
    
def readFromCorpusFile(corpusfile : str, outfolder : str) -> None:
    
    """Reads from a corpus file with one document per line and writes a folder with one text per document
    
    Keyword arguments:
    corpusfile -- name of the input corpusfile
    outfolder -- prefered name of the output folder
    """
    
    log.info('reading from corpus file ...')
    
    mastercorpus = os.path.join(os.getcwd(), corpusfile)
    outfolderpath = os.path.join(os.getcwd(), outfolder)
    filenames = list(open(corpusfile, 'r', encoding = "utf-8"))[-1].split(",")
    
    if not os.path.exists(outfolderpath):
        log.info('creating output folder ...')
        os.makedirs(outfolder)
    
    with open(mastercorpus, 'r', encoding = "utf-8") as f:
        for name, line in zip(filenames, f):
            contentPath = os.path.join(outfolderpath, name + ".txt")
            log.info('%s %s %s %s', writing', os.path.basename(contentPath) , 'from corpusfile to ', outfolder)
            
            with open(contentPath, 'w', encoding = "utf-8") as file:
                file.write(line)
    log.info('reading successfull')
    log.info('files from corpus written successfully')
     
'''
#
#Uncomment one of the following to use or call from console or other script
#
'''

#makeCorpusFile("swcorp_off", "smallcorpusfile.txt")
#readFromCorpusFile("smallcorpusfile.txt", "tesoutfolder")
