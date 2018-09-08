import logging
import DBConnector, DataModel
import requests
import json
import time
import redis

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)


def get_city_and_organ_location_by_autonavi(organ):
    r = redis.Redis(host='192.168.22.197', port=8173, db=1, encoding='gbk', decode_responses=True)
    params = {'address': organ, 'key': 'f60f13bfa6f8ebc1952e6d21b72ccd11'}
    url = 'https://restapi.amap.com/v3/geocode/geo?'.format(organ)
    web = requests.get(url, params=params)
    response = json.loads(web.text)
    print(response)
    response_model = DataModel.UniversityLocation()
    response_model.university_name = organ
    if response['status'] == '0' or response['count'] == '0':
        return False
    response_model.province = response['geocodes'][0]['province']
    city = response['geocodes'][0]['city']
    if type(city) is str:
        response_model.city = city
    else:
        response_model.city = None
    district = response['geocodes'][0]['district']
    if type(district) is str:
        response_model.district = district
    else:
        response_model.district = None
    response_model.longitude = float(response['geocodes'][0]['location'].split(',')[0])
    response_model.latitude = float(response['geocodes'][0]['location'].split(',')[1])
    DBConnector.db_writer(response_model)
    location_dict = dict(province=response_model.province, city=response_model.city, district=response_model.district,
                         longitude=response_model.longitude, latitude=response_model.latitude)
    r.hmset(organ, location_dict)
    print('已添加{0}位置信息'.format(organ))
    return True


def get_city_and_organ_location_by_tencent(start_sid):
    models = DBConnector.cnki_location_query_all()
    api_key = 'PFSBZ-GTOKP-JWHD3-VWKIL-KI4BQ-4YFQP'
    count = 0
    for model in models:
        model: DataModel.CNKILocationContent
        if model.sid < start_sid:
            continue
        url = 'https://apis.map.qq.com/ws/geocoder/v1/?address={0}&key={1}'.format(
            model.Organ, api_key)
        web = requests.get(url)
        time.sleep(0.3)
        response = json.loads(web.text)
        print(response)
        if response['status'] != 0:
            continue
        response_model = DataModel.CNKILocationContent()
        response_model.Province = response['result']['address_components']['province']
        response_model.City = response['result']['address_components']['city']
        response_model.District = response['result']['address_components']['district']
        response_model.Organ_Longitude = response['result']['location']['lng']
        response_model.Organ_Latitude = response['result']['location']['lat']
        DBConnector.update_cnki_location_city(model.sid, response_model)
        count = count + 1
        if count == 5000:
            break


def get_city_and_organ_location_by_google(start_sid):
    models = DBConnector.cnki_location_query_all_min_sid(start_sid)
    api_key = 'AIzaSyBuyQu2l_H3nCgGo84W26VwEVhFTNnm99g'
    for model in models:
        model: DataModel.CNKILocationContent
        if model.City is None:
            continue
        url = 'https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(
            model.City, api_key)
        proxy = {'http': 'socks5://127.0.0.1:1086',
                 'https': 'socks5://127.0.0.1:1086'}
        web = requests.get(url=url, proxies=proxy)
        response = json.loads(web.text)
        if response['status'] != 'OK':
            continue
        print(response['results'][0]['formatted_address'])
        location = response['results'][0]['geometry']['location']
        print(location)
        response_model = DataModel.CNKILocationContent()
        response_model.City_Longitude = location['lng']
        response_model.City_Latitude = location['lat']
        DBConnector.update_cnki_location_city_location(model.sid, response_model)


def get_city_test_autonavi(organ, city):
    params = {'address': organ, 'city': city, 'key': 'f60f13bfa6f8ebc1952e6d21b72ccd11'}
    url = 'https://restapi.amap.com/v3/geocode/geo?'.format(organ)
    web = requests.get(url, params=params)
    response = json.loads(web.text)
    print(response)


def get_city_test_tencent(organ):
    api_key = 'PFSBZ-GTOKP-JWHD3-VWKIL-KI4BQ-4YFQP'
    url = 'https://apis.map.qq.com/ws/geocoder/v1/?address={0}&key={1}'.format(
        organ, api_key)
    web = requests.get(url)
    response = json.loads(web.text)
    print(response)


def load_dict(organ_name):
    r = redis.Redis(host='192.168.22.197', port=8173, db=1, encoding='gbk', decode_responses=True)
    return r.hgetall(organ_name)


def get_city_by_dict():
    city_dict = load_dict()
    location_models = DBConnector.query_all(DataModel.CNKILocationContent)
    update_models = []
    for location_model in location_models:
        location_model: DataModel.CNKILocationContent
        if not location_model.organ_short_name:
            continue
        if '学院' not in location_model.organ_short_name:
            continue
        try:
            location_model.city = city_dict[location_model.organ_short_name][1]
            location_model.province = city_dict[location_model.organ_short_name][0]
            location_model.district = city_dict[location_model.organ_short_name][2]
            location_model.organ_longitude = city_dict[location_model.organ_short_name][3]
            location_model.organ_latitude = city_dict[location_model.organ_short_name][4]
            update_models.append(location_model)
        except KeyError:
            continue
    DBConnector.update_cnki_location_city_locations(update_models)


def update_one_organ(organ_name):
    city_dict = load_dict(organ_name)
    DBConnector.update_location_info_by_organ_short_name(organ_name, city_dict)
    print('已添加{0}位置信息到主表'.format(organ_name))


def new_old_name_clean(old_name, new_name):
    DBConnector.update_new_old_name(old_name, new_name)
    print('已将{0}替换为{1}...'.format(old_name, new_name))


def update_college_name(old_name, new_name):
    new_old_name_clean(old_name, new_name)
    update_one_organ(new_name)


def update_college_and_city(old_name, new_name):
    new_old_name_clean(old_name, new_name)
    update_one_organ(new_name)


def get_location_by_organ_city(organ, city):
    r = redis.Redis(host='192.168.22.197', port=8173, db=1, encoding='gbk', decode_responses=True)
    if r.exists(organ):
        return True
    params = {'address': organ, 'city': city, 'key': 'f60f13bfa6f8ebc1952e6d21b72ccd11'}
    url = 'https://restapi.amap.com/v3/geocode/geo?'.format(organ)
    web = requests.get(url, params=params)
    response = json.loads(web.text)
    print(response)
    response_model = DataModel.UniversityLocation()
    response_model.university_name = organ
    if response['status'] == '0' or response['count'] == '0':
        DBConnector.db_writer(response_model)
        return False
    response_model.province = response['geocodes'][0]['province']
    city = response['geocodes'][0]['city']
    if type(city) is str:
        response_model.city = city
    else:
        response_model.city = None
    district = response['geocodes'][0]['district']
    if type(district) is str:
        response_model.district = district
    else:
        response_model.district = None
    response_model.longitude = float(response['geocodes'][0]['location'].split(',')[0])
    response_model.latitude = float(response['geocodes'][0]['location'].split(',')[1])
    location_dict = dict(province=response_model.province, city=response_model.city, district=response_model.district,
                         longitude=response_model.longitude, latitude=response_model.latitude)
    r.hmset(organ, location_dict)
    print('已添加{0}位置信息'.format(organ))
    return True


def get_city_by_old_new(old_name, new_name, city):
    r = redis.Redis(host='192.168.22.197', port=8173, db=0, encoding='gbk', decode_responses=True)
    if r.get(old_name) == new_name:
        r.delete(old_name)
    r.set(old_name, new_name)
    print('已存入{0}和{1}对应关系'.format(old_name, new_name))
    if get_location_by_organ_city(new_name, city):
        update_college_and_city(old_name, new_name)


# get_city_test_autonavi('中国舰船研究院','北京')



old = '浙江省可视媒体智能处理技术研究重点实验室'
new = '浙江工业大学'
city_name = '宁波'
get_city_by_old_new(old, new, city_name)
