#!/usr/bin/python
#coding=utf-8
import sys, requests, json, csv, traceback
from datetime import datetime

def getDailyReport(date):
    url = 'http://www.twse.com.tw/exchangeReport/MI_INDEX'
    params = dict(
        response='json',
        type='ALLBUT0999',
    	date=date
    )
    try:
        resp = requests.get(url=url, params=params)
        content = json.loads(resp.content)
        return content
    except Exception as e:
        print 'Got exception at getDailyReport'
        print e
        print traceback.format_exc()
        sys.exit(-1)

def main():
    date = datetime.now().strftime("%Y%m%d")
    content = getDailyReport(date)
    header = content['fields5']
    header = [h.encode('utf-8') for h in header]
    data = content['data5']

    fw = open(date + "_report.csv","w")
    writer = csv.writer(fw)
    writer.writerow(header)
    for row in data:
        row = [r.encode('utf-8') for r in row]
        writer.writerow(row)
    fw.close()

if __name__ == "__main__":
    main()