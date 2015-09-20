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