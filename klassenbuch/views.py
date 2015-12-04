import deform
from deform import ValidationFailure
import colander

from . import helper
from .models import SchoolYearDay, SchoolYear

from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Day,
    Lesson,
    Pupil,
    Klasse
    )

@view_config(route_name='view_day', renderer='templates/view_day.pt')
def day_view(request):
    _id = request.matchdict['dayid']
    _day = Day.get_by_id(_id)
    
    return {'day': _day,}

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    #try:
    #    one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    #except DBAPIError:
    #    return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': 'one', 'project': 'klassenbuch'}
    
@view_config(route_name='create_newyear', renderer='templates/create_newyear.pt')
def newyear_view(request):
    class SchoolYearData(colander.MappingSchema):
        """
        Schema for creating a schoolyear
        """
        name = colander.SchemaNode(
            colander.String(),
            title='Bezeichnung des Schuljahres',
        )
        start_date = colander.SchemaNode(
            colander.Date(),
            title='Erster Schultag',
        )
        end_date = colander.SchemaNode(
            colander.Date(),
            title='Letzter Schultag',
        )
        begin_herbst = colander.SchemaNode(
            colander.Date(),
            title='Beginn der Herbstferien',
        )
        end_herbst = colander.SchemaNode(
            colander.Date(),
            title='Ende der Herbstferien',
        )
        begin_winter = colander.SchemaNode(
            colander.Date(),
            title='Beginn der Weihnachtsferien',
        )
        end_winter = colander.SchemaNode(
            colander.Date(),
            title='Ende der Winterferien',
        )
        begin_ostern = colander.SchemaNode(
            colander.Date(),
            title='Beginn der Osterferien',
        )
        end_ostern = colander.SchemaNode(
            colander.Date(),
            title='Ende der Osterferien',
        )
    
    schema = SchoolYearData()
    form = deform.Form(
        schema,
        buttons = [deform.Button('submit', "Okay")],
    )
    #Wurde das Formular abgeschickt?
    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)    
        except ValidationFailure as err:
            return {'form': err.render()}
        print(appstruct)
        #do something with the data supplied
        #verspeichern tun mir des jetzt
        school_date_list = helper.create_date_list(appstruct)
        #Schuljahr anlegen
        new_year = SchoolYear(name=appstruct["name"],
                              start_date=appstruct["start_date"],
                                end_date=appstruct["end_date"])
        DBSession.add(new_year)
        DBSession.flush()
        
        for datum in school_date_list:
            #verspeichern
            new_date = SchoolYearDay(
                date=datum,
                year_id=new_year.id
            )
        print("That worked")
        return HTTPFound(location=request.route_url('year_view',
                                                    year_id=new_year.id))
    html = form.render()
    return {'form': html,}
    
@view_config(route_name='year_view', renderer='templates/year_view.pt')
def year_view(request):
    _id = request.matchdict['year_id']
    _year = SchoolYear.get_by_id(_id)
    
    return {'year': _year,}


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_klassenbuch_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

