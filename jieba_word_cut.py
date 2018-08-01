import logging
import jieba
import os
import DataModel, DBConnector

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)


def init_user_word_list():
    word_list_dir = os.listdir('wordlist')
    for file_name in word_list_dir:
        user_word_file_name = 'wordlist/{0}'.format(file_name)
        words = open(user_word_file_name, 'r', encoding='utf-8').readlines()
        open('user_dict.txt', 'a', encoding='utf-8').writelines(words)


def get_stop_word_list():
    words = open('stoplist-最终使用版.txt', 'r', encoding='utf-8').readlines()
    stop_words = []
    for word in words:
        stop_words.append(word.replace('\n', ''))
    return stop_words


def jieba_cut():
    count_reader = open('T_Weibo_cleanfinish.txt', 'r', encoding='gbk', errors='ignore')
    total_count = len(count_reader.readlines())
    count_reader.close()

    reader = open('T_Weibo_cleanfinish.txt', 'r', encoding='gbk', errors='ignore')
    stop_list = get_stop_word_list()
    jieba.load_userdict('user_dict.txt')
    count = 0
    while True:
        line = reader.readline()
        if not line:
            break
        weibo_content = line.split('\t')[3]
        sid = line.split('\t')[0]
        words = jieba.lcut(weibo_content, cut_all=False)
        no_stop_line_list = []
        for word in words:
            if word not in stop_list:
                no_stop_line_list.append(word)
        no_stop_line = sid + ':' + '\t'.join(no_stop_line_list) + '\n'
        print(no_stop_line)
        open('no_stop_weibo.txt', 'a',encoding='gbk').write(no_stop_line)
        count = count + 1
        print('共有{0}条，已完成{1}条。'.format(str(total_count), str(count)))
    reader.close()


jieba_cut()
