import logging
import DataModel
import DBConnector

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)


def calculate_paper_count():
    paper_count_tuple_list = []
    models = DBConnector.query_all(DataModel.China_AL6_AL6)
    total_count = len(models)
    location_models = DBConnector.query_all(DataModel.CNKILocationContent)
    for model in models:
        model: DataModel.China_AL6_AL6
        if len(model.distcode) != 6:
            continue
        model.pacount = len(list(filter(lambda o: o.district_code == model.distcode, location_models)))
        paper_count_tuple = (model.id, model.pacount)
        paper_count_tuple_list.append(paper_count_tuple)
        total_count = total_count - 1
        print('{0} to load'.format(total_count))
    DBConnector.update_paper_count(paper_count_tuple_list)


def get_city_name_by_local_moran():
    with open('high-low.csv', 'r', encoding='gbk') as f:
        lines = f.readlines()
        id_list = []
        for line in lines:
            map_id = line.split(',')[0]
            id_list.append(map_id)
        results = DBConnector.get_city_name_by_map_id(id_list)
        # print(','.join(list(map(lambda o: o.split(':')[0], results))))
        for result in results:
            print(result)


