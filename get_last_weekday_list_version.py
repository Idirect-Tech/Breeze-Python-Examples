import calendar as cal
import sys
from datetime import datetime

def get_last_weekday(str_day, int_year, int_month):
    '''
    Get the last weekday of a given month in a given year.
        Parameters:
            str_day (str):  case insensitive day of week you want to seek.
                            ex.: 'thursday', 'tuesday'
            int_year (int): integer representing year in YYYY format
                            ex.: 1998, 2002
            int_month (int):    integer representing the month in MM format
                            ex.: 1, 11
        
        Returns:
            _   (datetime): date object from the Python's Standard datetime library


    '''
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
