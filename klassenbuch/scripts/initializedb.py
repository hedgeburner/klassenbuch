import os
import sys
import datetime
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models import (
    DBSession,
    Base,
    Klasse,
    Pupil,
    Day,
    Lesson,
    SchoolYear,
    SchoolYearDay
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        #create two schoolyears
        
        this_year = SchoolYear(name="2015/16", start_date=datetime.date(2015, 9, 7),
                                end_date=datetime.date(2016, 7, 22))
        DBSession.add(this_year)
        DBSession.flush()
        first_day = SchoolYearDay(date=datetime.date(2015,9,7), year_id = this_year.id)
        second_day = SchoolYearDay(date=datetime.date(2015,12,4), year_id = this_year.id)
        #create a lesson for pupil1
        lesson1 = Lesson(
            attendance=True,
            delay=20,
            lesson_no=1
        )
        lesson2 = Lesson(
            attendance=True,
            delay=0,
            lesson_no=2
        )
        lesson3=Lesson(
            attendance=False,
            lesson_no=3
        )
        # create a classbook entry 
        heute = Day(
            date=datetime.date.today(),
            excused = False,
            lessons=[lesson1, lesson2, lesson3],
            )
        # create one pupil named hans
        pupil1 = Pupil(name='Häns', days=[heute])
        
        # now add them to the database for persistence
        DBSession.add(pupil1)
        DBSession.add(heute)
        DBSession.add(first_day)
        DBSession.add(second_day)