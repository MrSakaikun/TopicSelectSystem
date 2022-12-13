import MeCab
import re


def format_text(text):
    '''
    MeCabに入れる前のツイートの整形方法例
    '''

    text=re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", text)
    text=re.sub('RT', "", text)
    text=re.sub('お気に入り', "", text)
    text=re.sub('まとめ', "", text)
    text=re.sub(r'[!-~]', "", text)#半角記号,数字,英字
    text=re.sub(r'[︰-＠]', "", text)#全角記号
    text=re.sub('\n', " ", text)#改行文字
    text=re.sub('　'," ", text)

    return text

def include_emoji(word):
    """
    引数は1文字
    返り値は絵文字等が含まれていたら1，そうでなければ0を返す
    """
    unicodeList = [(0x0080,0x2fff),(0x3100,0x31ef),(0x3200,0x4dff),(0xa000,0xf8ff),(0xfb00,0xfeff),(0x10000,0x1ffff),(0x2ff80,0x10ffff)]
    unicodeWord = int(hex(ord(word)),0)
    for uList in unicodeList:
        if uList[0] <= unicodeWord and unicodeWord <= uList[1]:
            return 1
    return 0

def exclude_emoji_in_text(text):
    """
    引数はテキスト1文
    返り値は絵文字等を取り除いたテキスト1文
    """
    exclude_emoji_text = ''
    for character in text:
        if not include_emoji(character):
            exclude_emoji_text += character
    return exclude_emoji_text


#MeCab
#m = MeCab.Tagger ()
#必要があれば（MeCab辞書を変える場合）以下のように随時コードに変えてください
m = MeCab.Tagger ('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')

#形態素解析
def mecab_parse(text):
    #引数はテキスト（文）
    #返り値はMeCabで形態素解析した結果を3次配列の形式にしたもの
    mecabFormat = []
    for txt in m.parse(text).split('\n'):
        t = txt.split('\t')
        if len(t)==2:
            xt = t[1].split(',')
            mecabFormat.append([t[0],xt])
    #形態素解析の形式で返す
    return mecabFormat

#文章から一般名詞・固有名詞を抽出
def extract_noun_from_text(text):
    #絵文字等の処理をここで行う
    text = format_text(text)
    text = exclude_emoji_in_text(text)
    #名詞を入れる場所
    nounList = []
    #形態素解析のフォーマットを取得
    mecabFormat = mecab_parse(text)
    #名詞だったら追加して返す
    for word_format in mecabFormat:
        if (word_format[1][0] == '名詞') and (word_format[1][1] in ["一般","固有名詞"]):
            nounList.append(word_format[0])
    return nounList


def extract_noun_from_list(textList):
    nounDict = set()
    for text in textList:
        nounDict = nounDict.union(extract_noun_from_text(text))
    return list(nounDict)
