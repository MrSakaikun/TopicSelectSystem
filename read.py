from gensim import models
import networkx as nx
import sqlite3
import pandas as pd
import pandas.io.sql as psql
import MeCab

m = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')


def isNoun(word):
    format = m.parse(word).split('\n')
    if len(format)==3:
        posinfo = format[0].split('\t')
        pos = posinfo[1].split(',')[0]
        if pos == '名詞':
            return True
    return False





class read_w2v_model:
    def __init__(self):
        path = './DataBase/jawiki.word_vectors.300d.binaryfile'
        self.model = models.KeyedVectors.load_word2vec_format(path,binary=True)

    def getVector(self,word):
        if word in self.model.vocab:
            return self.model.get_vector(word)
        else:
            return None

    def getVocab(self):
        return self.model.vocab

    def getSimilarity(self,source,target):
        if source in self.model.vocab and target in self.model.vocab:
            return self.model.similarity(source,target)
        else:
            return -1

    #基準となる単語に対してcos類似度の高い順に出力(thresholdは閾値)
    def get_lanking_from_wordList(self,set_word,wordList,threshold=0):
        similar_list = []
        if set_word in self.model.vocab:
            #類似度を計算
            for word in wordList:
                if word in self.model.vocab:
                    similar = self.model.similarity(set_word,word)
                    #閾値超えてたら出力対象とする
                    if similar >= threshold:
                        similar_list.append([word,similar])
            #類似度の高い順にsort
            similar_list.sort(key=lambda x:x[1],reverse=True)
        #出力
        return similar_list


class WordNetAllGraph():
    def __init__(self,onlyNoun=False):
        dbname = './DataBase/wnjpn.db'
        #SQL接続
        conn = sqlite3.connect(dbname)
        cur  = conn.cursor()
        #SQLコマンドをそのまま入力
        synlink_data = cur.execute("SELECT synset1,synset2 FROM synlink")
        synlink_listData = list(synlink_data)
        sence_data = cur.execute("SELECT synset,wordid FROM sense WHERE lang = 'jpn'")
        sence_listData = list(sence_data)
        #wordid_data = cur.execute("SELECT wordid,lemma FROM word WHERE lang = 'jpn' AND wordid IN (SELECT wordid FROM sense WHERE lang = 'jpn')")
        wordid_data = cur.execute("SELECT wordid,lemma FROM word WHERE lang = 'jpn'")
        wordid_listData = list(wordid_data)
        #単語リスト
        wordAllList = [x[1] for x in wordid_listData]
        if onlyNoun:
            self.wordList = list(filter(isNoun,wordAllList))
        else:
            self.wordList = wordAllList
        #接続解除
        cur.close()
        conn.close()
        #Graph作成
        self.G = nx.Graph()
        self.G.add_edges_from(synlink_listData)
        self.G.add_edges_from(sence_listData)
        self.G.add_edges_from(wordid_listData)
        print('WordNetGraph is completed.')

    def get_word_list(self):
        return self.wordList

    def get_shotest_path_length(self,source,target):
        if source in self.G.nodes and target in self.G.nodes:
            try:
                if source == target:
                    return 0
                return nx.shortest_path_length(self.G, source=source, target=target) - 3
            except nx.exception.NetworkXNoPath or nx.exception.NodeNotFound:
                return -1
        else:
            return -1

    def get_lanking_from_wordList(self,source,targetList,minDistance=1,maxDistance=20):
        distanceList = []
        for target in targetList:
            distance = self.get_shotest_path_length(source,target)
            #距離が指定範囲内であれば出力
            #None扱いのものを取り除くために2重ifを使用
            if distance:
                if distance >= minDistance and distance <= maxDistance:
                    distanceList.append([target,distance])
        #距離の長い順にsort
        distanceList.sort(key=lambda x:x[1],reverse=True)
        #出力
        return distanceList
