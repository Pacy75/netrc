import csv, json, requests, sys, threading, time, pause
from datetime import datetime, timedelta

class CrawlingThread(threading.Thread):
    def __init__(self, num, date, endTime, param):
        threading.Thread.__init__(self)
        self.num = num
        self.date = date
        self.endTime = endTime

        self.url = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp"
        self.params = dict(ex_ch=param)

        self.f = open(date + "/" + date + "_" + str(num) + ".csv","w")
        self.writer = csv.writer(self.f)

    def addRow(self, row):
        try:
            dd = datetime.utcnow()
            time_ns = str(dd.strftime('%s')) + str(dd.microsecond).zfill(6) + '000'
            self.writer.writerow([time_ns, row.get('t'), row.get('c'), row.get('z'), row.get('tv'), row.get('v'), row.get('a'), row.get('f'), row.get('b'), row.get('g')])
        except Exception as e:
            print e
            r = json.dumps(row)
            print 'Got exception at when addRow: ' + str(r)

    def crawling(self):
        try:
            resp = requests.get(url=self.url, params=self.params)
            content = json.loads(resp.content)
            data = content['msgArray']
            for d in data:
                self.addRow(d)

        except Exception as e:
            print 'Got exception at Thread ' + str(self.num)
            print e

    def run(self):
        while datetime.now() < self.endTime:
            start_time = time.time()
            startTime = datetime.now()
            print "(" + str(self.num) + ") start at: " + startTime.strftime("%I:%M:%S.%f %p")
            self.crawling()
            elapsed_time = time.time() - start_time
            print "(" + str(self.num) + ") Elapsed time for a request: " + str(elapsed_time)
            endTime = startTime.replace(second=(startTime.second / 5) * 5, microsecond=0) + timedelta(seconds=5) + timedelta(seconds=self.num/2)
            if self.num % 2 == 1:
                endTime = endTime + timedelta(microseconds=500000)
            if datetime.now() < endTime:
                pause.until(endTime)
        self.f.close()

