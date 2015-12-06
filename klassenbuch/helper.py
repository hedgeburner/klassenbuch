
import datetime

def create_date_list(appstruct):
    print("Huhu!")
    return []
    
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
    for i in range(Ostern-1):
        marz1 += tag
    return marz1

print(calculate_easter(2014))