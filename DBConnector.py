import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from enum import Enum, unique
import DataModel

import logging
import redis

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)

localhost_str = 'mssql+pyodbc://sa:900807@localhost/OpenAcademicGraphDB?driver=ODBC+Driver+17+for+SQL+Server'
remotehost_str = 'mssql+pyodbc://sa:Alex19900807.@192.168.22.197/WangXiaoDB?driver=ODBC+Driver+17+for+SQL+Server'

DBMySQLEngine: str = 'mysql+pymysql://alex:Mc2460022.@192.168.22.197:3306/alex_db'
DBSQLServerEngine: str = localhost_str


@unique
class DBName(Enum):
    MySQL = 0
    MSSQLSERVER = 1


DBNameDic = {0: 'mysql', 1: 'mssql'}


def create_db_session(db_name: DBName):
    connect_str: str
    if db_name == DBName.MSSQLSERVER:
        connect_str = DBSQLServerEngine
    elif db_name == DBName.MySQL:
        connect_str = DBMySQLEngine
    engine = create_engine(connect_str)
    session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    return session


def db_writer(model: object):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    new_session.add(model)
    new_session.commit()
    new_session.close()


def db_list_writer(models):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    new_session.bulk_save_objects(models)
    new_session.commit()
    new_session.close()


def query_all(data_model: DataModel):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    return new_session.query(data_model).all()


def cnki_query_all():
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    return new_session.query(DataModel.CNKIContent).all()


def cnki_location_query_all():
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    return new_session.query(DataModel.CNKILocationContent).all()


def cnki_location_query_all_min_sid(sid):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    return new_session.query(DataModel.CNKILocationContent).filter(DataModel.CNKILocationContent.sid >= sid).all()


def cnki_query_by_sid(sid):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    return new_session.query(DataModel.CNKIContent).filter(DataModel.CNKIContent.sid == sid).one()


def cnki_query_by_organ(organ):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    return new_session.query(DataModel.CNKILocationContent).filter(
        DataModel.CNKILocationContent.Organ.like('%{0}%'.format(organ))).all()


def update_cnki_location_model(sid, organ):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    new_session.query(DataModel.CNKILocationContent).filter(DataModel.CNKILocationContent.sid == sid).update(
        {DataModel.CNKILocationContent.Organ: organ})
    new_session.commit()


def update_cnki_location_city(sid, model: DataModel.CNKILocationContent):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    new_session.query(DataModel.CNKILocationContent).filter(DataModel.CNKILocationContent.sid == sid).update(
        {DataModel.CNKILocationContent.City: model.City,
         DataModel.CNKILocationContent.Organ_Longitude: model.Organ_Longitude,
         DataModel.CNKILocationContent.Organ_Latitude: model.Organ_Latitude,
         DataModel.CNKILocationContent.Province: model.Province,
         DataModel.CNKILocationContent.District: model.District})
    new_session.commit()


def update_cnki_location_city_location(sid, model: DataModel.CNKILocationContent):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    new_session.query(DataModel.CNKILocationContent).filter(DataModel.CNKILocationContent.sid == sid).update(
        {DataModel.CNKILocationContent.organ_latitude: model.organ_latitude,
         DataModel.CNKILocationContent.organ_longitude: model.organ_longitude})
    new_session.commit()
    new_session.close()


def update_cnki_location_city_locations(models):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    for model in models:
        model: DataModel.CNKILocationContent
        try:
            new_session.query(DataModel.CNKILocationContent).filter(
                DataModel.CNKILocationContent.sid == model.sid).update(
                {DataModel.CNKILocationContent.province: model.province,
                 DataModel.CNKILocationContent.city: model.city,
                 DataModel.CNKILocationContent.district: model.district,
                 DataModel.CNKILocationContent.organ_latitude: model.organ_latitude,
                 DataModel.CNKILocationContent.organ_longitude: model.organ_longitude})
            new_session.commit()
            print('完成sid={0}'.format(model.sid))
        except:
            continue
        finally:
            new_session.close()


def update_cnki_location_city_by_distinct():
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    model_list = new_session.query(DataModel.CNKILocationContent).filter(
        DataModel.CNKILocationContent.City.isnot(None)).distinct(DataModel.CNKILocationContent.Organ).all()
    count = len(model_list)
    print('共有{0}条'.format(str(count)))
    for model in model_list:
        new_session.query(DataModel.CNKILocationContent).filter(
            DataModel.CNKILocationContent.Organ == model.Organ).update(
            {DataModel.CNKILocationContent.City: model.City,
             DataModel.CNKILocationContent.Province: model.Province,
             DataModel.CNKILocationContent.District: model.District,
             DataModel.CNKILocationContent.Organ_Latitude: model.Organ_Latitude,
             DataModel.CNKILocationContent.Organ_Longitude: model.Organ_Longitude})
        new_session.commit()
        print('已完成第{0}条！'.format(str(count)))
        count = count - 1


def cnki_location_query_by_province(province):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    model_list = new_session.query(DataModel.CNKILocationContent).filter(
        DataModel.CNKILocationContent.Province == province).all()
    new_session.close()
    return model_list


def cnki_location_query_by_province_is_null():
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    model_list = new_session.query(DataModel.CNKILocationContent).filter(
        DataModel.CNKILocationContent.Province == None).all()
    new_session.close()
    return model_list


def update_province_paper_count(province, count):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    new_session.query(DataModel.CNKIProvinceSumContent).filter(
        DataModel.CNKIProvinceSumContent.province_name == province).update(
        {DataModel.CNKIProvinceSumContent.paper_count: count})
    new_session.commit()


def update_new_college_name(sid, new_organ):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    new_session.query(DataModel.CNKIMainContent).filter(DataModel.CNKIMainContent.sid == sid).update(
        {DataModel.CNKIMainContent.Organ: new_organ})
    new_session.commit()
    new_session.close()


def delete_organ(sid):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    new_session.query(DataModel.CNKIMainContent).filter(DataModel.CNKIMainContent.sid == sid).delete()
    new_session.commit()
    new_session.close()


def update_short_name(sid, short_name):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    new_session.query(DataModel.CNKILocationContent).filter(DataModel.CNKILocationContent.sid == sid).update(
        {DataModel.CNKILocationContent.organ_short_name: short_name})
    new_session.commit()
    new_session.close()


def update_short_names(short_name_list):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    for sid, short_name in short_name_list:
        new_session.query(DataModel.CNKILocationContent).filter(DataModel.CNKILocationContent.sid == sid).update(
            {DataModel.CNKILocationContent.organ_short_name: short_name})
        new_session.commit()
    new_session.close()


def update_new_old_name(old_name, new_name):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    new_session.query(DataModel.CNKILocationContent).filter(
        DataModel.CNKILocationContent.organ_short_name == old_name).update(
        {DataModel.CNKILocationContent.organ_short_name: new_name})
    new_session.commit()
    new_session.close()


def update_location_info_by_organ_short_name(organ, city_dict):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    new_session.query(DataModel.CNKILocationContent).filter(
        DataModel.CNKILocationContent.organ_short_name == organ).update(
        {DataModel.CNKILocationContent.province: city_dict['province'],
         DataModel.CNKILocationContent.city: city_dict['province'],
         DataModel.CNKILocationContent.district: city_dict['district'],
         DataModel.CNKILocationContent.organ_longitude: city_dict['longitude'],
         DataModel.CNKILocationContent.organ_latitude: city_dict['latitude']})
    new_session.commit()
    new_session.close()


def check_university_by_name(organ):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    try:
        new_session.query(DataModel.UniversityLocation).filter(
            DataModel.UniversityLocation.university_name == organ).one()
        return True
    except sqlalchemy.orm.exc.NoResultFound:
        return False
    finally:
        new_session.close()


def add_province_code():
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    lines = open('province_code.txt', 'r', encoding='utf-8').readlines()
    province_dict = {}
    for line in lines:
        line_items = line.split(':')
        key = line_items[0]
        value = line_items[1].replace('\n', '')
        province_dict[key] = value
    for key in province_dict.keys():
        new_session.query(DataModel.CNKILocationContent).filter(DataModel.CNKILocationContent.province == key).update(
            {DataModel.CNKILocationContent.province_code: province_dict[key]})
        new_session.commit()
    new_session.close()

add_province_code()
