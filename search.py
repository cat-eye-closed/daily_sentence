import import_text

#读取句子文本文件
textdic = import_text.read_file_to_dict('sentence.md')
#句子总数
SENTENCE_NUM = len(textdic)
#找到的句子序号序列
searched_list = []

def search(textdic,search_str,searched_list):
    for key in textdic:
        if textdic[key].find(search_str) != -1:
            searched_list.append(key)
            print('第{}句：{}'.format(key,textdic[key]))