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


class SchoolYear(Base):
    """
    A list of all school years.
    """
    __tablename__ = 'schoolyear'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, unique=True)
    start_date = Column(Date)
    end_date = Column(Date)
    
    @classmethod
    def get_by_id(cls, id):
        return DBSession.query(cls).filter(cls.id == id).first()
    

class SchoolYearDay(Base):
    """
    A list containing all valid schooldays in a schoolyear.
    """
    __tablename__ = 'schoolyeardays'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    year_id = Column(Integer, ForeignKey('schoolyear.id'))
    

class Klasse(Base):
    """
    A class (or course) of pupils
    """
    __tablename__ = 'klasse'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    timetable = None
    #pupils = relationship("Pupil", backref='klasse')
    

class Pupil(Base):
    """
    the students
    """
    __tablename__ = 'pupil'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    days = relationship("Day",
                        secondary='pupils_days',
                        backref='pupil')


class Day(Base):
    """
    Table containing schooldays of one individual pupil.
    Every day references an apropiate number     of lesson objects.
    Here we store the status of official excuses for this day.
    """
    __tablename__ = 'day'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    excused = Column(Integer, default=0)
    lessons = relationship("Lesson", backref='day')
    
    @classmethod
    def get_by_id(cls, id):
        return DBSession.query(cls).filter(cls.id == id).first()


class Lesson(Base):
    """
    Table containing lessons of individual pupils.
    Here we store attendance or delays of that particular lesson
    of this particular pupil.
    """
    __tablename__ = 'lesson'
    id = Column(Integer, primary_key=True)
    lesson_no = Column(Integer)
    attendance = Column(Boolean, default=True)
    delay = Column(Integer, default=0)
    day_id = Column(Integer, ForeignKey('day.id'))

# Table linking days with the pupils they belong to.
pupils_days = Table(
    'pupils_days', Base.metadata,
    Column(
        'pupil_id', Integer, ForeignKey('pupil.id'), nullable=False),
    Column(
        'day_id', Integer, ForeignKey('day.id'), nullable=False)
)
