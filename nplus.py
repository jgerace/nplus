import argparse
import codecs
import sys
import unicodedata

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, required=True,
                        help='path to file with input text')
    parser.add_argument('--n', type=int, required=True,
                        help='number of words to increment in the dictionary')
    parser.add_argument('--adjectives', action='store_true',
                        help='include adjectives for substitution')
    parser.set_defaults(adjectives=False)

    args = parser.parse_args()

    nouns = []
    adjectives = []

    with codecs.open('nouns.txt', 'r', 'utf-8') as fin:
        nouns = fin.readlines()
        nouns = [noun.strip() for noun in nouns]

    with codecs.open('adjectives.txt', 'r', 'utf-8') as fin:
        adjectives = fin.readlines()
        adjectives = [adjective.strip() for adjective in adjectives]

    text = ''
    with codecs.open(args.file, 'r', 'utf-8') as fin:
        lines = fin.readlines()

    tbl = dict.fromkeys(i for i in xrange(sys.maxunicode)
                        if unicodedata.category(unichr(i)).startswith('P'))
    
    for line in lines:
        words = line.split()

        output_line = []
        for word in words:
            word = word.lower().translate(tbl)
            if args.adjectives and word in adjectives:
                idx = adjectives.index(word)
                idx = (idx + args.n) % len(adjectives)
                output_line.append(adjectives[idx])
            elif word in nouns:
                idx = nouns.index(word)
                idx = (idx + args.n) % len(nouns)
                output_line.append(nouns[idx])
            else:
                output_line.append(word)

        print ' '.join(output_line)
        

if __name__ == '__main__':
    main()
