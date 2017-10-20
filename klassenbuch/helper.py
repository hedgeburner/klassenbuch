
import datetime

def create_date_list(appstruct):
    start = appstruct["start_date"]
    end = appstruct["end_date"]
    tag = datetime.timedelta(days=1)
    holidays = get_holidays(start.year)
    result = []
    now = start
    while now <= end:
        if (is_weekday(now) and (now not in holidays) and
        not (appstruct["begin_herbst"] <= now <= appstruct["end_herbst"]) and
        not (appstruct["begin_winter"] <= now <= appstruct["end_winter"]) and
        not (appstruct["begin_ostern"] <= now <= appstruct["end_ostern"])):
            result.append(now)
        now += tag
    return result
    
def calculate_easter(year):
    """Osteralgorithmus von C. Gauss."""
    k = year // 100
    m = 15 + (3*k + 3) // 4 - (8*k + 13) // 25
    s = 2-(3*k + 3) // 4
    a = year % 19
    d = (19*a + m) % 30
    r = (d + a // 11) // 29
    og = 21 + d-r
    sonn = 7-(year + year // 4 + s) % 7
    oe = 7-(og -sonn) % 7
    Ostern = og + oe
    marz1 = datetime.date(year, 3, 1)
    tag = datetime.timedelta(days=1)
    result = marz1 + Ostern * tag
    return result

def get_holidays(startyear):
    """calculate all official holidays in hesse starting from 1.9
    of starting year - 31.8. of next year.
    return a set.
    """
    tag = datetime.timedelta(days=1)
    tag_der_deutschen_einheit = datetime.date(startyear, 10, 3)
    ostern = calculate_easter(startyear + 1)
    karfreitag = ostern - 2 * tag
    ostermontag = ostern + tag
    mai1 = datetime.date(startyear + 1, 5, 1)
    himmelfahrt = ostern + 39 * tag
    pfingsten = ostern + 49 * tag
    fronleichnam = ostern + 60 * tag
    return {tag_der_deutschen_einheit, ostern, karfreitag, ostermontag,
            mai1, himmelfahrt, pfingsten, fronleichnam}
    
def is_weekday(date):
    """
    return true if the date is a weekday.
    """
    return date.isoweekday() < 6