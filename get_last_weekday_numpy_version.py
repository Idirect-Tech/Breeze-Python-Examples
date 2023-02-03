import numpy as np
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
        int_day=dict_day_codes[str_day.lower()]
    except KeyError:
        print("Check spelling!")
        sys.exit(0)
    list_calendar = cal.monthcalendar(int_year, int_month)
    list_weekdays = [1,2,3,4,5,6,7]
    list_product = [list_weekdays for dates in cal.monthcalendar(int_year,int_month)]

    arr_cal, arr_product=np.array(list_calendar), np.array(list_product)

    arr_zeros=np.zeros(arr_cal.shape, int)

    np.copyto(dst=arr_product, src=arr_zeros, where=arr_cal == 0)
    x = np.argwhere(arr_product==int_day)[-1]
    return datetime(int_year, int_month, arr_cal[x[0]][x[1]])
