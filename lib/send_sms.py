from datetime import datetime
import os
from twilio.rest import Client
from lib.weekday import get_previous_weekday

def text_daily_picks(picks, url):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    last_weekday = get_previous_weekday()
    report_date = datetime.strptime(last_weekday, '%Y%m%d').strftime('%d/%m/%Y')

    summary = 'US Bargain Stocks for {}\n'.format(report_date)
    for symbol in picks[:10]:
        summary += '{} @ ${}, {}%\n'.format(symbol[0], symbol[1], symbol[3])

    summary += '\n{}'.format(url)
    client.api.account.messages.create(
    to="+447378259495",
    from_="+441618508105",
    body=summary)
    return summary


