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
    MyModel,
    Base,
    Entry,
    Klasse,
    Pupil,
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
        # create one pupil named hans
        pupil1 = Pupil(name='Hans')
        # create a classbook entry 
        eintrag1 = Entry(
            date=datetime.date.today(),
            lesson_no=1,
            attendance=True,
            # delay=25,
            )
        # add the entry to hans
        eintrag1.pupil = [pupil1]
        # now add them to the database for persistence
        DBSession.add(pupil1)
        DBSession.add(eintrag1)
