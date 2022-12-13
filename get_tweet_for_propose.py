from TwitterAPI import TwitterAPI
from extract_noun import extract_noun_from_list,extract_noun_from_text
from collections import Counter
from extract_topicword import ExtractTopicWord
from record_userdata import record_tweetList
from read import read_w2v_model

#vocabを取得
w2v = read_w2v_model()
vocab = w2v.getVocab()


#名詞の出現頻度順
def get_interest_keywords_from_tweets(tweetList,size=1):
    count = Counter()
    for tweet in tweetList:
        count = count + Counter(extract_noun_from_text(tweet))

    return [x[0] for x in count.most_common(size) if x[0] in vocab]


#話題抽出後に出現頻度順に並べる
def extract_topic_from_tweets(etw,tweetList,size=1):
    count = Counter()
    interest_word_list = []
    for tweet in tweetList:
        count = count + Counter([etw.getTopicWord(tweet)])
    for x in count.most_common():
        if x[0] is not None:
            if x[0] in vocab:
                interest_word_list.append(x[0])
                if len(interest_word_list) == size:
                    break

    return interest_word_list


#3.4節のユーザの単語を取り除く前までの工程
def get_tweetList_for_propose(screen_name='MrSakaikun',keywordSize=10,interestSize=5):
    api = TwitterAPI(screen_name=screen_name)
    #screen_nameとTweetListを取得
    user_name = api.get_screen_name()
    user_tweetList = api.get_tweet_from_usertimeline()
    user_nounList = extract_noun_from_list(user_tweetList)


    if keywordSize < interestSize:
        keywordSize = interestSize


    #直接ユーザに興味を聞く方法
    #if how_to_get_input == 'directly':
    interestFilePath = './Record/interest_word_'+user_name+'.txt'

    interest_word_list_directly = []
    keywordsList_directly = []
    with open(interestFilePath,'r') as f:
        interest_word_list = f.read().split()
    for word in interest_word_list:
        if word in vocab:
            if len(interest_word_list_directly) < interestSize:
                interest_word_list_directly.append(word)
            if len(keywordsList_directly) < keywordSize:
                keywordsList_directly.append(word)




    #話題抽出後の出現頻度順
    #elif how_to_get_input == 'extract_topic':
    etw = ExtractTopicWord(corpus_choice='wikipedia',conditional_noun='name',format='binaryfile')
    interest_word_list_extractTopic = extract_topic_from_tweets(etw,user_tweetList,size=interestSize)
    keywordsList_extractTopic = extract_topic_from_tweets(etw,user_tweetList,size=keywordSize)

    #名詞の出現頻度順
    #else:
    interest_word_list_counter = get_interest_keywords_from_tweets(user_tweetList,size=interestSize)
    keywordsList_counter = get_interest_keywords_from_tweets(user_tweetList,size=keywordSize)


    #dict型で格納
    tweetList = {'user_name':user_name,
                 'keywordsList_directly':keywordsList_directly,
                 'interest_word_list_directly':interest_word_list_directly,
                 'keywordsList_extractTopic':keywordsList_extractTopic,
                 'interest_word_list_extractTopic':interest_word_list_extractTopic,
                 'keywordsList_counter':keywordsList_counter,
                 'interest_word_list_counter':interest_word_list_counter,
                 'user_tweetList':user_tweetList,
                 'user_nounList':user_nounList}

    #キーワード検索を行い，その結果をTweetListに格納
    keywordsSearch_nounList_counter = set()
    keywordsSearch_nounList_extractTopic = set()
    keywordsSearch_nounList_directly_counter = set()
    keywordsSearch_nounList_directly_extractTopic = set()

    #for keyword in keywordsList:
    for keyword in list(set(keywordsList_counter)|set(keywordsList_directly)|set(keywordsList_extractTopic)):
        #キーワード検索
        tweetList[keyword] = api.get_tweet_from_keyword(keyword)
        #検索結果を集合に追加
        #extract_topic
        if keyword in keywordsList_extractTopic:
            for tweet in tweetList[keyword]:
                if etw.getTopicWord(tweet):
                    keywordsSearch_nounList_extractTopic = keywordsSearch_nounList_extractTopic.union([etw.getTopicWord(tweet)])
        #counter
        if keyword in keywordsList_counter:
            keywordsSearch_nounList_counter = keywordsSearch_nounList_counter.union(extract_noun_from_list(tweetList[keyword]))

        #directly
        if keyword in keywordsList_directly:
            for tweet in tweetList[keyword]:
                if etw.getTopicWord(tweet):
                    keywordsSearch_nounList_directly_extractTopic = keywordsSearch_nounList_directly_extractTopic.union([etw.getTopicWord(tweet)])
            keywordsSearch_nounList_directly_counter = keywordsSearch_nounList_directly_counter.union(extract_noun_from_list(tweetList[keyword]))


    #キーワード検索結果の単語集合も追加
    tweetList['keywordSearch_nounList_counter'] = list(keywordsSearch_nounList_counter)
    tweetList['keywordSearch_nounList_extractTopic'] = list(keywordsSearch_nounList_extractTopic)
    tweetList['keywordSearch_nounList_directly_counter'] = list(keywordsSearch_nounList_directly_counter)
    tweetList['keywordSearch_nounList_directly_extractTopic'] = list(keywordsSearch_nounList_directly_extractTopic)


    #TweetListを記録
    record_tweetList(tweetList,screen_name,keywordSize,interestSize)

    #tweetListを返す
    return tweetList



if __name__ == '__main__':
    #print(get_tweetList_for_propose().keys())
    """
    api = TwitterAPI(screen_name='MrSakaikun')
    user_tweetList = api.get_tweet_from_usertimeline()
    etw = ExtractTopicWord(corpus_choice='wikipedia',conditional_noun='name',format='binaryfile')
    print(extract_topic_from_tweets(etw,user_tweetList,size=25))
    print(get_interest_keywords_from_tweets(user_tweetList,size=25))
    """
    tweetList = get_tweetList_for_propose()
    print(tweetList['keywordSearch_nounList_extractTopic'])
    print(tweetList['keywordSearch_nounList_directly_extractTopic'])
