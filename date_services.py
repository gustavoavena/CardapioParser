from datetime import *

# datetime.date.today().strftime("%y-%m-%d")

URL_DATE_FORMAT = "%y-%m-%d"

def next_weekdays(next, start_date = date.today()):
    start_date = date.today()

    date_strings = []
    counter = 0
    while(len(date_strings) < next):
        d = start_date + timedelta(days=counter)
        if(d.weekday() in range(0, 5)):
            date_strings.append(d.strftime(URL_DATE_FORMAT))
        counter += 1

    # print(date_strings)



    return date_strings

