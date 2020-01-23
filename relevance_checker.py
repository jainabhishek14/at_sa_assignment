import nltk, getopt, os, sys, ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download("punkt")
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

path="articles"
outpath="output"

def main(argv):
    productName = ''
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:p:",["ifile=","product="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -p <product>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -p <product>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-p", "--product"):
            productName = arg
    checker(productName, inputfile)

def checker(product, file):
    document = open(os.path.join(path, file), 'r')
    for paragraph in document:
        paragraph_sentence_list = tokenizer.tokenize(paragraph)
        for line in range(0,len(paragraph_sentence_list)):
            if product in paragraph_sentence_list[line]:
                try:

                    sentence = paragraph_sentence_list[line-1] + paragraph_sentence_list[line] + paragraph_sentence_list[line+1]
                    if not os.path.exists(outpath):
                        os.makedirs(outpath)

                    files = file.split(".")
                    outFileName = files[0] + "_" +product + "." + files[1]
                    with open(os.path.join(outpath, outFileName), 'a') as f:
                        f.write(sentence+"\n")
                        f.close()
                except IndexError as identifier:
                    pass

if __name__ == "__main__":
    main(sys.argv[1:])