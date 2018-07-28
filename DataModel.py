import logging
from sqlalchemy import Column, NVARCHAR, Integer, TEXT, DATETIME, BOOLEAN, VARCHAR, FLOAT
from sqlalchemy.ext.declarative import declarative_base

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)

Base = declarative_base()


class CNKIContent(Base):
    __tablename__ = 'T_CNKI_ORI'

    sid = Column(Integer, primary_key=True)
    SrcDatabase = Column(VARCHAR(255))
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
    Organ = Column(VARCHAR(255))
    Organ_Longitude = Column(FLOAT)
    Organ_Latitude = Column(FLOAT)
    Province = Column(VARCHAR(255))
    City = Column(VARCHAR(255))
    District = Column(VARCHAR(255))
    City_Longitude = Column(FLOAT)
    City_Latitude = Column(FLOAT)
