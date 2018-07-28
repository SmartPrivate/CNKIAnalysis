import logging
import DBConnector, DataModel
import requests
import json
import time

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)


def get_city_and_organ_location_by_autonavi(start_sid):
    models = DBConnector.cnki_location_query_all()
    count = 0
    for model in models:
        model: DataModel.CNKILocationContent
        if model.sid < start_sid:
            continue
        url = 'https://restapi.amap.com/v3/geocode/geo?address={0}&key=f60f13bfa6f8ebc1952e6d21b72ccd11'.format(
            model.Organ)
        web = requests.get(url)
        response = json.loads(web.text)
        print(response)
        if response['status'] == '0':
            continue
        if response['count'] == '0':
            continue
        response_model = DataModel.CNKILocationContent()
        response_model.Province = response['geocodes'][0]['province']
        city = response['geocodes'][0]['city']
        if type(city) is str:
            response_model.City = city
        else:
            response_model.City = None
        district = response['geocodes'][0]['district']
        if type(district) is str:
            response_model.District = district
        else:
            response_model.District = None
        response_model.Organ_Longitude = float(response['geocodes'][0]['location'].split(',')[0])
        response_model.Organ_Latitude = float(response['geocodes'][0]['location'].split(',')[1])
        DBConnector.update_cnki_location_city(model.sid, response_model)
        count = count + 1
        if count == 6000:
            break


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
    count = 0
    for model in models:
        model: DataModel.CNKILocationContent
        url = 'https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(
            model.Organ, api_key)
        proxy = {'http': 'socks5://127.0.0.1:1086',
                  'https': 'socks5://127.0.0.1:1086'}
        web = requests.get(url=url, proxies=proxy)
        response=json.loads(web.text)
        if response['status']!='OK':
            continue
        print(response['results'][0]['formatted_address'])


# get_city_and_organ_location_by_autonavi()
# get_city_and_organ_location_by_tencent(11615)
get_city_and_organ_location_by_google(15518)
