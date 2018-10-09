import logging
from sqlalchemy import Column, NVARCHAR, Integer, TEXT, DATETIME, BOOLEAN, VARCHAR, FLOAT
from sqlalchemy.ext.declarative import declarative_base

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)

Base = declarative_base()


class CNKIContent(Base):
    __tablename__ = 'T_CNKI_ORI_TEMP'

    sid = Column(Integer, primary_key=True)
    SrcDatabase = Column(VARCHAR(8))
    Title = Column(TEXT)
    Author = Column(VARCHAR(255))
    Organ = Column(TEXT)
    Source = Column(NVARCHAR(255))
    Keyword = Column(TEXT)
    Summary = Column(TEXT)
    PubTime = Column(DATETIME)
    FirstDuty = Column(VARCHAR(255))
    Fund = Column(TEXT)
    Year = Column(Integer)


class CNKIMainContent(Base):
    __tablename__ = 'T_CNKI_ORI'

    sid = Column(Integer, primary_key=True)
    SrcDatabase = Column(VARCHAR(8))
    Title = Column(TEXT)
    Author = Column(VARCHAR(255))
    Organ = Column(TEXT)
    Source = Column(NVARCHAR(255))
    Keyword = Column(TEXT)
    Summary = Column(TEXT)
    PubTime = Column(DATETIME)
    FirstDuty = Column(VARCHAR(255))
    Fund = Column(TEXT)
    Year = Column(Integer)


class CNKILocationContent(Base):
    __tablename__ = 'T_CNKI_Location'

    sid = Column(Integer, primary_key=True)
    ori_sid = Column(Integer)
    organ_full_name = Column(VARCHAR(255))
    organ_short_name = Column(VARCHAR(255))
    organ_longitude = Column(FLOAT)
    organ_latitude = Column(FLOAT)
    province_name = Column(VARCHAR(50))
    province_code = Column(VARCHAR(6))
    city_name = Column(VARCHAR(50))
    city_code = Column(VARCHAR(6))
    district_name = Column(VARCHAR(50))
    district_code = Column(VARCHAR(6))


class UniversityLocation(Base):
    __tablename__ = 'D_University_Location'

    university_name = Column(VARCHAR(50), primary_key=True)
    province = Column(VARCHAR(50))
    city = Column(VARCHAR(50))
    district = Column(VARCHAR(50))
    longitude = Column(FLOAT)
    latitude = Column(FLOAT)


class CNKIProvinceSumContent(Base):
    __tablename__ = 'T_CNKI_Province_Sum'

    sid = Column(Integer, primary_key=True)
    province_name = Column(VARCHAR(255))
    paper_count = Column(Integer)


class China_AL2_AL6(Base):
    __tablename__ = 'China_AL2-AL6'

    id = Column(Integer, primary_key=True)
    country = Column(VARCHAR(254))
    name = Column(VARCHAR(254))
    enname = Column(VARCHAR(254))
    locname = Column(VARCHAR(254))
    distname = Column(VARCHAR(50))
    distcode = Column(VARCHAR(6))
    proname = Column(VARCHAR(50))
    procode = Column(VARCHAR(6))
    cityname = Column(VARCHAR(50))
    citycode = Column(VARCHAR(6))
    pacount=Column(VARCHAR(10))
    offname = Column(VARCHAR(254))
    boundary = Column(VARCHAR(254))
    adminlevel = Column(Integer)
    wikidata = Column(VARCHAR(254))
    wikimedia = Column(VARCHAR(254))
    timestamp = Column(VARCHAR(254))
    note = Column(VARCHAR(254))
    rpath = Column(VARCHAR(254))
    ISO3166_2 = Column(VARCHAR(254))

class China_AL6_AL6(Base):
    __tablename__ = 'china_al6-al6'

    id = Column(Integer, primary_key=True)
    country = Column(VARCHAR(254))
    name = Column(VARCHAR(254))
    enname = Column(VARCHAR(254))
    locname = Column(VARCHAR(254))
    distname = Column(VARCHAR(50))
    distcode = Column(VARCHAR(6))
    proname = Column(VARCHAR(50))
    procode = Column(VARCHAR(6))
    cityname = Column(VARCHAR(50))
    citycode = Column(VARCHAR(6))
    pacount = Column(VARCHAR(10))
    offname = Column(VARCHAR(254))
    boundary = Column(VARCHAR(254))
    adminlevel = Column(Integer)
    wikidata = Column(VARCHAR(254))
    wikimedia = Column(VARCHAR(254))
    timestamp = Column(VARCHAR(254))
    note = Column(VARCHAR(254))
    rpath = Column(VARCHAR(254))
    ISO3166_2 = Column(VARCHAR(254))


class Province(Base):
    __tablename__ = 'D_Province'

    province_code = Column(VARCHAR(6), primary_key=True)
    province_name = Column(VARCHAR(50))


class City(Base):
    __tablename__ = 'D_City'

    city_code = Column(VARCHAR(6), primary_key=True)
    city_name = Column(VARCHAR(50))
    province_code = Column(VARCHAR(6))
    province_name = Column(VARCHAR(50))


class District(Base):
    __tablename__ = 'D_District'

    district_code = Column(VARCHAR(6), primary_key=True)
    district_name = Column(VARCHAR(50))
    city_code = Column(VARCHAR(6))
    city_name = Column(VARCHAR(50))
    province_code = Column(VARCHAR(6))
    province_name = Column(VARCHAR(50))
