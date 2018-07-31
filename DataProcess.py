import logging
import DBConnector, DataModel

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


def province_count():
    model_list = []
    provinces = open('province.txt', 'r').read().split('\n')
    for province in provinces:
        model = DataModel.CNKIProvinceSumContent()
        model.province_name = province
        count = len(DBConnector.cnki_location_query_by_province(province))
        model.paper_count = count
        model_list.append(model)
        # DBConnector.update_province_paper_count(province, count)
    DBConnector.db_list_writer(model_list)


# province_count()
