import json
from io import StringIO
import operator
import csv

def analyze_stocks(decliners):
    decliners_list = []
    for key, value in decliners.items():
        pe_ratio = value.get('pe_ratio')
        dividend_yield = value.get('dividend_yield')
        if pe_ratio and dividend_yield:
            decliners_list.append([
                value.get('symbol'),
                value.get('closing_price'),
                value.get('price_decline'),
                value.get('price_decline_percentage'),
                pe_ratio,
                dividend_yield
            ])
    ranked_stocks = sorted(decliners_list, key=operator.itemgetter(3))
    ranked_stocks = sorted(ranked_stocks, key=operator.itemgetter(5), reverse=True)
    ranked_stocks = sorted(ranked_stocks, key=operator.itemgetter(4))

    buff = StringIO()
    writer = csv.writer(buff)
    writer.writerow(['Symbol', 'Closing Price', 'Price Decline', 'Price Decline Percent', 'PE', 'Dividend Yield'])
    writer.writerows(ranked_stocks)
    buff.seek(0)
    csv_data = buff.getvalue()
    buff.close()

    return ranked_stocks, csv_data
