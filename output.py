"""
作成中
3.5節からの内容
"""


from get_tweet_for_propose import get_tweetList_for_propose
from read import read_w2v_model
from read import WordNetAllGraph
import keras
import numpy as np
from scipy.stats import rankdata
import csv
from record_userdata import record_output


thresholdList = [(4,7),(3,8),(2,9)]
distanceMAX = 16
top = 5

#概念距離測定モデル
print('loading_WNmodels')
modelPath = './WNModels/batch_trained_model_'
modelNameList = ['20_to_20','100_to_20','200_to_100','300_to_300']
models = [keras.models.load_model(modelPath+modelName) for modelName in modelNameList]

#モデル準備
print('reading_w2v_model')
w2v = read_w2v_model()
print('reading_wordnet')
wn  = WordNetAllGraph(onlyNoun=False)



#出力選定
def select_topic(interestWordList,candidateNounList,evaluation_method,threshold=None):
    #出力選定用
    selectTopic = dict()

    #各interestWordに対して実行
    for interestWord in interestWordList:
        #cos類似度
        cos_similarity_scores = [w2v.getSimilarity(interestWord,target) for target in candidateNounList]
        #cos類似度のランキング
        #desc = list(rankdata(-np.array(cos_similarity_scores)))
        desc = sorted(cos_similarity_scores,reverse=True)
        #概念距離（実際の値）
        distance_real = [wn.get_shotest_path_length(interestWord,target) for target in candidateNounList]
        #概念距離（推定値）
        if evaluation_method in modelNameList:
            interestWordVector = w2v.getVector(interestWord)
            candidateNounVectorList = list(map(w2v.getVector,candidateNounList))
            model = models[modelNameList.index(evaluation_method)]
            distance_predict = [model.predict([[interestWordVector],[vector]]) * distanceMAX for vector in candidateNounVectorList]

        #選定開始
        output_topic_index = []
        for i in range(len(candidateNounList)):
            if len(output_topic_index) >= top:
                break
            #出力候補の何番目の話？
            candidateIndex = cos_similarity_scores.index(desc[i])
            #閾値設定があるとき
            if threshold:
                #概念距離の確認
                if evaluation_method == 'wordnet':
                    distance = distance_real[candidateIndex]
                else:
                    distance = distance_predict[candidateIndex]
                #distanceが0だったりNoneだったら飛ばす
                if not distance:
                    continue
                #概念距離が閾値内じゃないときは飛ばす
                if distance < threshold[0] or threshold[1] < distance:
                    continue
            #出力候補に追加
            output_topic_index.append(candidateIndex)

        #出力形式に整形
        output_topics = []
        for index in output_topic_index:
            #出力形式
            format = {'word':candidateNounList[index],
                      'cos_similarity_score':cos_similarity_scores[index],
                      'distance_real':distance_real[index]}
            #概念距離測定モデルの場合
            if evaluation_method in modelNameList:
                format['distance_predict'] = distance_predict[index]
            #出力形式に追加
            output_topics.append(format)

        #selectTopicに追加
        selectTopic[interestWord] = output_topics
    #selectTopicを返す
    return selectTopic



#output
def get_output_topics(tweetList):
    #ユーザ名取得
    screen_name = tweetList['user_name']
    #出力用変数
    output = dict()
    output['user_name'] = screen_name

    #input取得方法での比較
    for how_to_get_input in ['extractTopic','counter','directly_extractTopic','directly_counter']:
        print(how_to_get_input)
        output[how_to_get_input] = dict()
        #ユーザの興味のある単語の読み込み
        if 'directly' in how_to_get_input:
            interestWordList = tweetList['interest_word_list_directly']
        else:
            interestWordList = tweetList['interest_word_list_'+how_to_get_input]
        #出力候補の読み込み
        keywordsSearch_nounList = tweetList['keywordSearch_nounList_'+how_to_get_input]
        #ユーザの呟いた単語は取り除く
        if 'directly' in how_to_get_input:
            #アンケートで聞いた単語を取り除く
            candidateNounList_A = list(set(keywordsSearch_nounList)-set(interestWordList))
        else:
            #ユーザが呟いた単語を取り除く
            candidateNounList_A = list(set(keywordsSearch_nounList)-set(tweetList['user_nounList']))

        #ベクトル化できない単語は取り除く
        vocab = w2v.getVocab()
        candidateNounList = [candidateNoun for candidateNoun in candidateNounList_A if candidateNoun in vocab]


        #評価方法と選定
        for evaluation_method in ['only_cos','wordnet','20_to_20','100_to_20','200_to_100','300_to_300']:
            print(evaluation_method)
            if evaluation_method == 'only_cos':
                output[how_to_get_input][evaluation_method] = select_topic(interestWordList,candidateNounList,evaluation_method)
            else:
                output[how_to_get_input][evaluation_method] = dict()
                for threshold in thresholdList:
                    output[how_to_get_input][evaluation_method][threshold] = select_topic(interestWordList,candidateNounList,evaluation_method,threshold)


    #output変数を保存
    print('saving...')
    record_output(output,screen_name)

    #outputを返す
    return output




if __name__ == '__main__':
    import pickle
    with open('./Record/tweetList_MrSakaikun_10_5.binaryfile','rb') as f:
        tweetList = pickle.load(f)
    output = output(tweetList)
