from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.dialects.mysql import MEDIUMTEXT, VARCHAR, BOOLEAN, DATETIME, LONGTEXT, INTEGER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Members(Base):

    __tablename__ = 'member'
    __table_args__ = {'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    member_id = Column(INTEGER, unique=True, nullable=False)
    #internal_id = Column(INTEGER, unique=True, nullable=False)
    url = Column(VARCHAR(350))
    language = Column(VARCHAR(2))
    full_address = Column(VARCHAR(350))
    gender = Column(MEDIUMTEXT)
    name = Column(MEDIUMTEXT)
    education = Column(MEDIUMTEXT)
    address = Column(MEDIUMTEXT)
    city = Column(MEDIUMTEXT)
    zipcode = Column(MEDIUMTEXT)
    email = Column(MEDIUMTEXT)
    tel = Column(MEDIUMTEXT)
    fax = Column(MEDIUMTEXT)
    website = Column(MEDIUMTEXT)
    job = Column(MEDIUMTEXT)
    sector = Column(MEDIUMTEXT)
    group = Column(MEDIUMTEXT)
    section = Column(MEDIUMTEXT)
    #memberoffices = relationship("MemberOffice", back_populates="child")


class Offices(Base):
    __tablename__ = 'office'
    __table_args__ = {'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    office_id = Column(INTEGER, unique=True, nullable=False)
    #internal_id = Column(INTEGER, unique=True, nullable=False)
    url = Column(VARCHAR(350))
    language = Column(VARCHAR(2))
    full_address = Column(VARCHAR(350))
    name = Column(MEDIUMTEXT)
    address = Column(MEDIUMTEXT)
    city = Column(MEDIUMTEXT)
    zipcode = Column(MEDIUMTEXT)
    email = Column(MEDIUMTEXT)
    tel = Column(MEDIUMTEXT)
    fax = Column(MEDIUMTEXT)
    website = Column(MEDIUMTEXT)
    sector = Column(MEDIUMTEXT)
    #children = relationship("MemberOffice", back_populates="parent")
    #memberoffices = relationship("MemberOffice", back_populates="child")

class MemberOffice(Base):
    __tablename__ = 'memberoffice'
    __table_args__ = {'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}

    id = Column(INTEGER, primary_key=True, autoincrement=True, nullable=False)
    member_id = Column(INTEGER, ForeignKey("member.id"))
    #member_id = Column(INTEGER, unique=True, nullable=True)
    office_id = Column(INTEGER, ForeignKey("office.id"))
    created_date = Column(DateTime, default=datetime.now)
    #child = relationship("Members", back_populates="memberoffices")

def create_all(engine):
    print("creating databases")
    Base.metadata.create_all(engine)
