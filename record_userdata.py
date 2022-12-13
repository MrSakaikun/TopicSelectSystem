"""
ユーザのデータ記録用プログラム
"""
import pickle


def record_tweetList(tweetList,screen_name,keywordSize,interestSize):
    filePathTop = './Record/tweetList_'+screen_name+'_'+str(keywordSize)+'_'+str(interestSize)

    #バイナリファイルから
    with open(filePathTop+'.binaryfile','wb') as fwb:
        pickle.dump(tweetList,fwb)

    #テキストファイル
    with open(filePathTop+'.txt',mode='w',encoding='utf_8') as fw:
        for k,v in tweetList.items():
            fw.write(k+":"+'\n')
            if type(v) == type([0]):
                fw.write(str(v)+'\n')
            else:
                fw.write(v+'\n')




def record_output(output,screen_name):
    filePathTop = './Record/output_'+screen_name

    #バイナリファイルから
    with open(filePathTop+'.binaryfile','wb') as fwb:
        pickle.dump(output,fwb)


    #テキストファイル
    with open(filePathTop+'.txt',mode='w',encoding='utf_8') as fw:
        #再帰用
        def write_dict(dict_value):
            for k,v in dict_value.items():
                fw.write(str(k)+":"+'\n')
                if type(v) == type(dict()):
                    write_dict(v)
                elif type(v) == type(list()):
                    write_list(v)
                elif type(v) == type(float(0.0)):
                    fw.write(str(v)+'\n')
                else:
                    fw.write(v+'\n')

        #単語等の出力用
        def write_list(list_value):
            for value in list_value:
                for k,v in value.items():
                    fw.write(str(k)+":"+'\n')
                    if type(v) == type(str('猫')):
                        fw.write(v+'\n')
                    else:
                        fw.write(str(float(v))+'\n')

        #書き込み開始
        write_dict(output)
