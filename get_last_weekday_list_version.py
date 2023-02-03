import calendar as cal
import sys
from datetime import datetime

def get_last_weekday(str_day, int_year, int_month):
    dict_day_codes = {'monday':1,
                    'tuesday':2,
                    'wednesday':3,
                    'thursday':4,
                    'friday':5,
                    'saturday':6,
                    'sunday':7}
    try:
        int_day=dict_day_codes[str_day]
    except KeyError:
        print("Check spelling!")
        sys.exit(0)
    list_calendar = cal.monthcalendar(int_year, int_month)
    list_weekdays = [1,2,3,4,5,6,7]
    list_product = [list_weekdays for dates in cal.monthcalendar(int_year,int_month)]

    l_cal = [x for sub_list in list_calendar for x in sub_list]
    l_prod = [x for sub_list in list_product for x in sub_list]
    l_out = [l_prod[i] if l_cal[i]!=0 else 0 for i in range(len(l_cal))]
    l_out.reverse()
    return datetime(int_year, int_month, l_cal[len(l_cal)-l_out.index(int_day)-1])





get_last_weekday('thursday', 1998, 10)