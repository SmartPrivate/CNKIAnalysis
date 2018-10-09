import logging

import redis

import DBConnector
import DataModel

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)


def get_chnname_and_code(temp_model: DataModel.China_AL6_AL6):
    r = redis.Redis(host='192.168.22.197', port=8173, db=2, decode_responses=True, encoding='utf-8')
    special_district1 = ['乌恰县', '阿图什市', '阿合奇县', '阿克陶县', '克孜勒苏柯尔克孜自治州', '喀什地区', '阿拉尔市', '阜康市', '五家渠市', '乌鲁木齐市',
                         '吴忠市', '化隆回族自治县', '同心县', '利通区', '米东区', '达坂城区', '沙依巴克区', '乌鲁木齐县', '天山区',
                         '水磨沟区', '头屯河区', '新市区']
    special_district2 = ['甘孜藏族自治州', '九寨沟县', '茂县', '碌曲县', '卓尼县', '德钦县', '洛隆县', '乃东区', '谢通门县', '桑珠孜区', '边坝县', '呼和浩特市',
                         '蒙古族自治县', '雅江县', '互助土族自治县', '同德县', '兴海县', '湟源县', '门源县', '曲麻莱县', '治多县', '刚察县', '海晏县',
                         '大通回族土族自治县', '海东市', '西宁市', '玉树藏族自治州', '精河县']
    local_name_list = temp_model.locname.split('/')
    if '德令哈市' in temp_model.locname:
        return temp_model.id, '德令哈市', r.get('德令哈市')
    if len(local_name_list) == 3:
        temp01 = local_name_list[0].replace(' ', '')
        if temp01 in special_district1:
            local_name = local_name_list[0]
        elif '民和回族土族自治县' in local_name_list[0]:
            local_name = '民和回族土族自治县'
        else:
            local_name = local_name_list[1].replace(' ', '')
    else:
        local_name = local_name_list[0]
        temp_list = local_name.split(' ')
        if len(temp_list) == 3:
            if temp_list[1] in special_district2:
                local_name = temp_list[1]
        elif len(temp_list) == 2:
            if temp_list[1].replace('(', '').replace(')', '') in ['夏河县', '合作市', '舟曲县', '松潘县', '壤塘县', '康定市', '炉霍县',
                                                                  '久治县', '玉树市', '若尔盖县']:
                local_name = temp_list[1].replace('(', '').replace(')', '')
            else:
                local_name = temp_list[0]
                if '洛龙区' in local_name:
                    local_name = '洛龙区'
        else:
            local_name = temp_list[0]
            if '(' in local_name:
                local_name = local_name[0:local_name.index('(')]
    if '广州市' in local_name:
        local_name = '广州市'
    if '(' in local_name:
        local_name = local_name[0:local_name.index('(')]
    if ' ' in local_name:
        local_name = local_name[0:local_name.index(' ')]
    if r.exists(local_name):
        return temp_model.id, local_name, r.get(local_name)
    else:
        return temp_model.id, local_name, 0


def get_map_info():
    districts = DBConnector.query_all(DataModel.District)
    dist_tuple_list = []
    models = DBConnector.query_all(DataModel.China_AL6_AL6)
    for model in models:
        model: DataModel.China_AL6_AL6
        dist_from_dict = list(filter(lambda o: o.district_name == model.distname, districts))
        if len(dist_from_dict) > 1 or len(dist_from_dict) == 0:
            continue
        dist_model: DataModel.District = dist_from_dict[0]
        dist_tuple = (
            model.id, dist_model.province_name, dist_model.province_code, dist_model.city_name, dist_model.city_code,
            dist_model.district_code)
        dist_tuple_list.append(dist_tuple)
    DBConnector.update_all(dist_tuple_list)
