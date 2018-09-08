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
    province = Column(VARCHAR(255))
    province_code = Column(Integer)
    city = Column(VARCHAR(255))
    district = Column(VARCHAR(255))


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
