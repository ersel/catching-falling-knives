import json
import pandas
from io import StringIO

def analyze_stocks(decliners):
    df = pandas.DataFrame.from_dict(decliners, orient='index')
    # pick companies which are cashflow positive and has paid a dividend last year
    cols = ['pe_ratio', 'dividend_yield']
    df[cols] = df[df[cols] > 0][cols]
    filtered = df.dropna()
    ranked = filtered.sort_values(by=['pe_ratio', 'dividend_yield', 'price_decline_percentage'], ascending=[True, False, True])
    print(ranked)

    buff = StringIO()
    ranked.to_csv(buff)
    buff.seek(0)
    csv = buff.getvalue()
    buff.close()

    return ranked.values.tolist(), csv
