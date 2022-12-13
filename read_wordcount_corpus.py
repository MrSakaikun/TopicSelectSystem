import csv
import pickle


#名詞の出現頻度データコーパスを読み込む
def read_wordcount_corpus(corpus,format):
    #ファイル名を指定
    if corpus == 'dialogue':
        fileName = './WordCountCorpus/wordcount_corpus_from_dialogue_corpus.'+format
    elif corpus == 'wikipedia':
        fileName = './WordCountCorpus/wordcount_corpus_from_wikipedia_txt.'+format
    elif corpus == 'for_test':
        fileName = './word_count.'+format
    else:
        return None

    #binaryfile形式のファイルの読み込み
    if format == 'binaryfile':
        with open(fileName,'rb') as f:
            return pickle.load(f)

    #csv形式で読み込み
    if format == 'csv':
        wordList = []
        with open(fileName,'r') as f:
            reader = csv.reader(f)
            for row in reader:
                wordList.append(row)
        return dict(wordList)
