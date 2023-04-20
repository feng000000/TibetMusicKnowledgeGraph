import os
import jieba
import jieba.posseg

ProjectHome = "/home/feng/Code/dachuang"
FileDir = f"{ProjectHome}/data/txt"
StopWordsPath = f"{ProjectHome}/getwords/stop_words.txt"
UserDicrPath = f"{ProjectHome}/getwords/user_dict.txt"
FileList = os.listdir(FileDir)
jieba.load_userdict(UserDicrPath)

for FileName in FileList:
    with open(f"{FileDir}/{FileName}", "r", encoding="utf-8") as f:
        content = f.read()
    words = jieba.posseg.cut(content)
    # words = jieba.cut(content)

    # for word in words:
    #     print(word, end=",")

    with open(StopWordsPath, 'r', encoding='utf-8') as f:
        stopwords = [line.strip() for line in f.readlines()]

    ch_nums = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '零', '百', '千', '万']
    res = {}

    def check(x):
        '''
            判断词x是否满足条件
            Args:
                str: 检查词
            Returns:
                bool: 判断结果
        '''
        # 过滤停止词
        if x in stopwords:
            return False
        # 必须包含中文,过滤汉语数字
        for i in x:
            if i < u'\u4e00' or i > u'\u9fff' or i in ch_nums:
                return False
        return True

    for word, flag in words:
        if flag == 'n' and check(word):
            if word in res.keys():
                res[word] += 1
            else:
                res[word] = 1
    res = sorted(res.items(), key=lambda x:x[1], reverse=True)

    print('title:', FileName)
    print(res[:10])
    # break
