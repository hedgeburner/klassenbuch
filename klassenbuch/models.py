from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Unicode,
    Date,
    Boolean,
    Table,
    ForeignKey
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('my_index', MyModel.name, unique=True, mysql_length=255)


class Klasse(Base):
    """
    A class (or course) of pupils
    """
    __tablename__ = 'klasse'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    timetable = None
    

class Pupil(Base):
    """
    the students
    """
    __tablename__ = 'pupil'
    id = Column(Integer, primary_key=True)
    name = Column(Text)


"""
Each pupil has a number of entries.
"""
pupils_entries = Table(
    'pupils_entries', Base.metadata,
    Column(
        'pupil_id', Integer, ForeignKey('pupil.id'),
        primary_key=True, nullable=False),
    Column(
        'entry_id', Integer, ForeignKey('entry.id'),
        primary_key=True, nullable=False),
)


class Entry(Base):
    """
    a classbook entry
    """
    __tablename__ = 'entry'
    id = Column(Integer, primary_key=True)
    
    date = Column(Date)
    pupil = relationship(
            Pupil,
            secondary=pupils_entries,
            backref='entry')

    lesson_no = Column(Integer)
    attendance = Column(Boolean, default=True)
    delay = Column(Integer, default=0)
