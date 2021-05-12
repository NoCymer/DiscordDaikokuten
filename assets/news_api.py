from GoogleNews import GoogleNews
from datetime import date, timedelta
import random


def getnews(subject):
    googlenews = GoogleNews(lang='en')
    current_date = date.today()
    date_string = current_date.strftime("%m/%d/%Y")
    date_string_previous_day = date.today() - timedelta(days=1)
    googlenews.set_time_range(date_string, date_string_previous_day.strftime("%m/%d/%Y"))
    googlenews.search(str(subject))
    result = googlenews.get_links()
    googlenews.clear()
    try:
        return str(result[random.randint(0, len(result))])
    except IndexError:
        date_string_previous_week = date.today() - timedelta(days=7)
        googlenews.set_time_range(date_string, date_string_previous_week.strftime("%m/%d/%Y"))
        googlenews.search(str(subject))
        result = googlenews.get_links()
        return str(result[random.randint(0, len(result))])
