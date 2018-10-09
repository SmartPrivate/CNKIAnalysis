import logging
import DBConnector, DataModel
import re

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)


def init_main_table():
    university_list, college_list, company_list, facility_list, normal_list = [], [], [], [], []
    model_list: list = DBConnector.cnki_query_all()
    for model in model_list:
        model: DataModel.CNKIContent
        if '大学' in model.Organ:
            university_index = model.Organ.index('大学')
            organ = model.Organ[0:university_index + 2]
            # if '实验室' in organ:
            #    organ = organ[0:organ.index('实验室') + 3]
            university_model = DataModel.CNKILocationContent()
            university_model.Organ = organ
            university_model.ori_sid = model.sid
            university_list.append(university_model)
            continue

        if '学院' in model.Organ:
            organ = model.Organ[0:model.Organ.index('学院') + 2]
            college_model = DataModel.CNKILocationContent()
            college_model.ori_sid = model.sid
            college_model.Organ = organ
            college_list.append(college_model)
            continue

        normal_model = DataModel.CNKILocationContent()
        normal_model.ori_sid = model.sid
        normal_model.Organ = model.Organ
        normal_list.append(normal_model)
    DBConnector.db_list_writer(university_list)
    DBConnector.db_list_writer(college_list)
    DBConnector.db_list_writer(normal_list)


def init_location_table():
    models: [DataModel.CNKIMainContent] = DBConnector.query_all(DataModel.CNKIMainContent)
    organ_model_list = []
    for model in models:
        if not model.Organ:
            continue
        for organ in model.Organ.split(';'):
            organ_model = DataModel.CNKILocationContent()
            organ_model.organ_full_name = organ
            organ_model.ori_sid = model.sid
            organ_model_list.append(organ_model)
    DBConnector.db_list_writer(organ_model_list)


def organ_cleaning():
    models = DBConnector.query_all(DataModel.CNKIMainContent)
    for model in models:
        model: DataModel.CNKIMainContent
        if not model.Organ:
            continue
        if model.Organ in ['计算机仿真', '计算机应用', '计算机应用研究', '软件学报', '计算机辅助设计与图形学学报', '图象图形', '图学学报', '系统仿真学报', '中文信息学报']:
            DBConnector.delete_organ(model.sid)
            continue
        if not re.search('\d\d\d\d\d\d', model.Organ) and not re.search('^[a-zA-Z]', model.Organ) and not re.search(
                '\d\d\d\d\d', model.Organ):
            continue
        organs = model.Organ.split(';')
        organ_list = []
        for organ in organs:
            if re.search('\d\d\d\d\d\d', organ):
                continue
            if re.search('^[a-zA-Z]', organ):
                continue
            if re.match('\d\d\d\d\d', organ):
                continue
            organ_list.append(organ)
        new_organ = ';'.join(organ_list)
        DBConnector.update_new_college_name(model.sid, new_organ)


def get_short_organ_name(keyword):
    models = DBConnector.query_all(DataModel.CNKILocationContent)
    short_name_list = []
    for model in models:
        model: DataModel.CNKILocationContent
        if model.organ_short_name:
            continue
        if keyword in model.organ_full_name:
            short_name = model.organ_full_name[:model.organ_full_name.index(keyword) + len(keyword)]
            if '(' in short_name:
                short_name = short_name[short_name.index('(') + 1:]
            short_name_list.append((model.sid, short_name))
    DBConnector.update_short_names(short_name_list)


def get_locations_by_year():
    for year in range(2002, 2018, 5):
        location_models = DBConnector.query_cnki_location_by_year_range(year - 5, year)
        count_tuple_list = []
        dist_code_list = list(map(lambda o: o.district_code, location_models))
        dist_code_set = set(dist_code_list)
        for dist_code in dist_code_set:
            id_ = DBConnector.get_id_by_dist_code(dist_code)
            if id_ == '':
                continue
            count_tuple_list.append((id_, len(list(filter(lambda o: o == dist_code, dist_code_list)))))
        with open('{0}_{1}.csv'.format(str(year - 5), str(year-1)), 'a', encoding='utf-8') as f:
            f.write('id' + ',' + 'pacount' + '\n')
            for item in count_tuple_list:
                f.write(item[0] + ',' + str(item[1]) + '\n')
            f.close()
        print('Finish {0} to {1}'.format(str(year - 5), str(year)))


get_locations_by_year()
