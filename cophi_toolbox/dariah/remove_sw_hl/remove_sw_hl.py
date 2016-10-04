from collections import Counter
import logging

log = logging.getLogger('cophi_toolbox.dariah.remove_sw_hl')
log.addHandler(logging.NullHandler())

# To enable logger, uncomment the following three lines.
#logging.basicConfig(level=logging.INFO,
#                    format='%(asctime)s %(levelname)s %(name)s: %(message)s',
#                    datefmt='%d-%b-%Y %H:%M:%S')

#path = "mycorpusfile.txt"

def makeCounter(path):
    with open(path, 'r', encoding='utf-8') as f:
        count = Counter(f.read().split())
    log.info('Detected word frequency.')
    return count

#mycounter = makeCounter(path)

def makeRemoveLists(mycounter):

    countersum = 0.01 * sum(mycounter.values())

    hapax = set([hapx for hapx, value in mycounter.items() if value == 1])

    stopwords = set([stopw for stopw, value in mycounter.items() if value > countersum])

    log.info('%s %s', len(hapax), 'hapax legomena detected.')
    log.info('%s %s', len(stopwords), 'stopwords detected.')
    return hapax, stopwords


def removestuff(inpath, outpath):
    
    mycounter = makeCounter(inpath)
    
    hapax, stopwords = makeRemoveLists(mycounter)

    with open(inpath, 'r', encoding="utf-8") as tmp:
        last = len(list(tmp)) -2 
    with open(inpath, 'r', encoding='utf-8') as g:
        with open(outpath, 'w', encoding='utf-8') as f:
            for i, line in enumerate(g):
                if i != last:
                    log.info('%s %s', 'working on ...', i)
                    f.write(' '.join([word for word in line.split() if word not in hapax or stopwords]) + "\n")
                
                else:
                    log.info('%s %s', 'working on ...', i)
                    f.write(' '.join([word for word in line.split() if word not in hapax or stopwords]))
                    log.info('Hapax legomena and stopwords removed.')
                    break

#removestuff(path, "mycorpusremoved.txt", hapax, stopwords)
