import sys, requests, json, time, threading, os, pause
from crawlingThread import CrawlingThread
from datetime import datetime, timedelta

DEV = '0'
PROD = '1' 

def getDayTradingStocks():
    url = 'http://www.twse.com.tw/exchangeReport/TWTB4U'
    try:
        resp = requests.get(url=url)
        content = json.loads(resp.content)
        return content
    except Exception as e:
        print 'Got exception at getDayTradingStocks'
        print e
        return []

def getDayTradingStocksFromBackup():
    dirname = os.path.dirname(__file__)
    fname = dirname + '/../intraDayTradingList/List0.txt'
    if not os.path.isfile(fname):
        return []
    with open(fname) as f:
        lines = f.readlines()
        content = [x.strip() for x in lines] 
    return content

def split(arr, size):
    arrs = []
    while len(arr) > size:
        pice = arr[:size]
        arrs.append(pice)
        arr = arr[size:]
    arrs.append(arr)
    return arrs

def main(opt):
    print "(" + opt + ")Started at: " + datetime.now().strftime("%I:%M:%S.%f %p")
    now = datetime.now()
    endTime = now + timedelta(seconds=11) # for DEV
    if opt == PROD:
        endTime = now.replace(hour=13, minute=30, second=10, microsecond=0)

    print "Set end time at: " + endTime.strftime("%I:%M:%S.%f %p")
    content = getDayTradingStocks()
    if [] == content:
        date = datetime.now().strftime("%Y%m%d")
        candidates = getDayTradingStocksFromBackup()
    else:
        date = content['date']
        candidates = [d[0] for d in content['data']]
    print date + " Total " + str(len(candidates)) + " stocks."
    
    if [] == candidates:
        print "Stop because no candidate found."
        return

    candidates = split(candidates, 100)
    print "Divide to " + str(len(candidates)) + " lists."
    
    if not os.path.exists(date):
        os.mkdir(date, 0755);

    if opt == PROD:
        startTime = now.replace(hour=9, minute=0, second=0, microsecond=0)
        print "Set start time at: " + startTime.strftime("%I:%M:%S.%f %p")
        if datetime.now() < startTime:
            pause.until(startTime)
    
    threads = []
    start_time = time.time()
    for cList in candidates:
        param = "|".join(["tse_{}.tw".format(c) for c in cList])
        threads.append(CrawlingThread(len(threads), date, endTime, param))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    elapsed_time = time.time() - start_time
    print "Total elapsed time: " + str(elapsed_time)
    print "Finished at: " + datetime.now().strftime("%I:%M:%S.%f %p")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        opt = sys.argv[1]
    else:
        opt = DEV
    main(opt)
