import logging
import requests
import json

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


def word_process(process_str: str):
    process_str.encode('gbk')
    post_data_dict = dict(text=process_str)
    post_data = json.dumps(post_data_dict)
    token_json_line = open('baiduyun_access_token.json', 'r').readline()
    format_json = json.loads(token_json_line)
    post_url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/lexer'
    post_params = dict(access_token=format_json['access_token'])
    r = requests.post(post_url, params=post_params, data=post_data)
    return r.text


result = word_process('我是一名光荣的中国共产党员!')
print(result)
