from datetime import date, timedelta, datetime


URL_DATE_FORMAT = "%Y-%m-%d"

def next_weekdays(next, start_date_string = date.today().strftime("%Y-%m-%d")):
    start_date = datetime.strptime(start_date_string, URL_DATE_FORMAT)


    date_strings = []
    counter = 0
    while(len(date_strings) < next):
        d = start_date + timedelta(days=counter)
        if(d.weekday() in range(0, 5)):
            date_strings.append(d.strftime(URL_DATE_FORMAT))
        counter += 1




    return date_strings



def segunda_a_sexta():
    today = date.today()

    return today.weekday() in range(0, 5) # retorna true se for um dia de segunda a sexta.
