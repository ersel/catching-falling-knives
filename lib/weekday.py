from datetime import datetime, timedelta

def get_previous_weekday():
    # markets are open mon-fri, weekdays
    previous_date = datetime.now() - timedelta(1)
    while previous_date.weekday() > 4:
        previous_date = previous_date - timedelta(1)

    return previous_date.strftime("%Y%m%d")
