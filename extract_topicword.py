from read_wordcount_corpus import read_wordcount_corpus
from extract_noun import format_text,exclude_emoji_in_text
import MeCab


#mecab_parse用
m = MeCab.Tagger ('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')

#mecabFormatを作成
def mecab_parse(text):
    mecabFormat = []
    for txt in m.parse(text).split('\n'):
        t = txt.split('\t')
        if len(t)==2:
            xt = t[1].split(',')
            mecabFormat.append([t[0],xt])
    return mecabFormat


class ExtractTopicWord():
    #読み込み
    def __init__(self,corpus_choice='dialogue',conditional_noun='all',format='binaryfile'):
        #コーパスを何にしたかの記録
        self.corpus_choice = corpus_choice

        #抽出条件
        self.conditional_noun = conditional_noun

        #指定したコーパスからwordCounterの読み込み
        self.wordCounter = read_wordcount_corpus(corpus=corpus_choice,format=format)


    #抽出判定(True or Falseを返す関数)
    def judge_condition(self,word_format):
        conditional_noun = self.conditional_noun
        #wordCounterに入ってなければ抽出しない
        if word_format[0] in self.wordCounter.keys():
            #名詞ならばTrue
            if conditional_noun == 'all':
                if word_format[1][0] == '名詞':
                    return True
            #一般名詞か固有名詞ならTrue
            if conditional_noun == 'name':
                if (word_format[1][0] == '名詞') and (word_format[1][1] in ['一般','固有名詞']):
                    return True
            #一般名詞か固有名詞かサ変接続ならTrue
            if conditional_noun == 'sahen':
                if (word_format[1][0] == '名詞') and (word_format[1][1] in ['一般','固有名詞','サ変接続']):
                    return True
        #条件を満たさなければFalse
        return False

    #テキストから話題語を抽出する
    def getTopicWord(self,text):
        nounList = []
        #絵文字等の処理
        text = exclude_emoji_in_text(format_text(text))
        mecabFormat = mecab_parse(text)
        #テキスト中の名詞でwordCounterに入っている名詞を対象とする
        for word_format in mecabFormat:
            if self.judge_condition(word_format):
                nounList.append(word_format[0])

        #候補となる名詞がなければNoneを返す
        if nounList == []:
            return None

        #出現頻度の低い順に並び替えて話題語を出力
        rank = list(zip(nounList,map(self.wordCounter.get,nounList)))
        rank.sort(key=lambda x:x[1])
        return rank[0][0]
        #テスト用
        #return rank
