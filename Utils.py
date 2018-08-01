import logging
import requests
import json
import time

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)


def get_access_token_str():
    api_key = 'VcI6kj211iHVwbSkCcUctPaK'
    secret_key = 'ewTduLnYpTbfKs5ZdvqEDDaCTBBjhwum'
    token_request_url = 'https://aip.baidubce.com/oauth/2.0/token'
    token_request_params = dict(grant_type='client_credentials', client_id=api_key, client_secret=secret_key)
    token_request = requests.get(url=token_request_url, params=token_request_params)
    open('baiduyun_access_token.json', 'w').write(token_request.text)
    print('【access_token完整json已写入文件baiduyun_access_token.txt】')
    return token_request.text


def word_cut_baiduyun(process_str: str):
    process_str.encode('gbk')
    post_data_dict = dict(text=process_str)
    post_data = json.dumps(post_data_dict)
    token_json_line = open('baiduyun_access_token.json', 'r').readline()
    format_json = json.loads(token_json_line)
    post_url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/lexer'
    post_params = dict(access_token=format_json['access_token'])
    r = requests.post(post_url, params=post_params, data=post_data)
    time.sleep(0.2)
    return r.text


def get_stop_word_list():
    words = open('stoplist-最终使用版.txt', 'r', encoding='utf-8').readlines()
    stop_words = []
    for word in words:
        stop_words.append(word.replace('\n', ''))
    return stop_words


def word_cut():
    count_reader = open('T_Weibo_cleanfinish.txt', 'r', encoding='gbk', errors='ignore')
    total_count = len(count_reader.readlines())
    count_reader.close()

    reader = open('T_Weibo_cleanfinish.txt', 'r', encoding='gbk', errors='ignore')
    stop_list = get_stop_word_list()
    count = 0
    while True:
        line = reader.readline()
        if not line:
            break
        weibo_content = line.split('\t')[3]
        sid = line.split('\t')[0]
        no_stop_line_list = []
        result = word_cut_baiduyun(weibo_content)
        result_json = json.loads(result)
        try:
            for item in result_json['items']:
                word = item['item']
                if word not in stop_list:
                    no_stop_line_list.append(word)
        except KeyError:
            no_stop_line_list.append('key error')
        no_stop_line = sid + ':' + '\t'.join(no_stop_line_list) + '\n'
        print(no_stop_line)
        open('no_stop_weibo_baidu.txt', 'w',encoding='gbk',errors='ignore').write(no_stop_line)
        count = count + 1
        print('共有{0}条，已完成{1}条。'.format(str(total_count), str(count)))
    reader.close()


def word_to_vec_baiduyun(process_str):
    process_str.encode('gbk')
    post_data_dict = dict(word=process_str)
    post_data = json.dumps(post_data_dict)
    token_json_line = open('baiduyun_access_token.json', 'r').readline()
    format_json = json.loads(token_json_line)
    post_url = 'https://aip.baidubce.com/rpc/2.0/nlp/v2/word_emb_vec'
    post_params = dict(access_token=format_json['access_token'])
    r = requests.post(post_url, params=post_params, data=post_data)
    return r.text


def word_to_vec():
    count_reader = open('no_stop_weibo.txt', 'r', encoding='gbk', errors='ignore')
    total_count = len(count_reader.readlines())
    count_reader.close()

    reader = open('no_stop_weibo.txt', 'r', encoding='gbk', errors='ignore')
    reader.readline()
    count = 0
    while True:
        line = reader.readline()
        if not line:
            break
        words = line.split(':')[1].split('\t')
        sid = line.split(':')[0]
        for word in words:
            result = word_to_vec_baiduyun(word)
            print(result)


word_cut()
