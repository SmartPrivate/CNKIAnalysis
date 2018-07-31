from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from enum import Enum, unique
import DataModel

import logging

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)

localhost_str = 'mssql+pyodbc://sa:900807@localhost/OpenAcademicGraphDB?driver=ODBC+Driver+17+for+SQL+Server'
remotehost_str = 'mssql+pyodbc://sa:Alex19900807.@192.168.22.197/WangXiaoDB?driver=ODBC+Driver+17+for+SQL+Server'

DBMySQLEngine: str = 'mysql+pymysql://root:900807@localhost:3306/alex_db'
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
        {DataModel.CNKILocationContent.City_Latitude: model.City_Latitude,
         DataModel.CNKILocationContent.City_Longitude: model.City_Longitude})
    new_session.commit()


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
    return model_list


def update_province_paper_count(province, count):
    db_session: sessionmaker = create_db_session(DBName.MySQL)
    new_session = db_session()
    new_session.query(DataModel.CNKIProvinceSumContent).filter(
        DataModel.CNKIProvinceSumContent.province_name == province).update(
        {DataModel.CNKIProvinceSumContent.paper_count: count})
    new_session.commit()
