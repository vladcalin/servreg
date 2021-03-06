import datetime
import humanize
import psutil
import re

from sqlalchemy import create_engine, Column, String, Integer, Boolean, DateTime, Sequence, Index, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
Session = sessionmaker()


def init_database(dburl):
    engine = create_engine(dburl)
    print("created engine {}".format(engine))
    return engine


def get_session_class():
    return sessionmaker()


class Service(Base):
    __tablename__ = "emerald_services"

    id = Column(Integer, Sequence("seq_id_service"), primary_key=True)
    name = Column(String)

    url = Column(String, index=True)

    first_seen = Column(DateTime, default=datetime.datetime.now)
    last_seen = Column(DateTime, default=datetime.datetime.now)

    is_alive = Column(Boolean, default=True)

    def update_is_alive(self):
        print((datetime.datetime.now() - self.last_seen).total_seconds())
        self.is_alive = (datetime.datetime.now() - self.last_seen).total_seconds() <= 60

    def human_readable_first_seen(self):
        return humanize.naturalday(self.first_seen)

    def human_readable_last_seen(self):
        return humanize.naturaltime(self.last_seen)


class Incident(Base):
    __tablename__ = "emerald_incidents"

    SEVERITY_LOW = 1
    SEVERITY_MEDIUM = 2
    SEVERITY_HIGH = 3

    id = Column(Integer, Sequence("seq_id_incidents"), primary_key=True)
    severity = Column(Integer, default=SEVERITY_LOW)
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.now)

    @classmethod
    def create(cls, severity, message):
        instance = cls()
        instance.severity = severity
        instance.message = message
        return instance
