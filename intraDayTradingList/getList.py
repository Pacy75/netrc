import sys, requests, json

# argv[1]:
# 0 stock (default)
# 1 counter
STOCK = '0'
COUNTER = '1'

def getCurrentList(opt):
    if opt == COUNTER:
        url = 'http://www.tpex.org.tw/web/stock/trading/intraday_trading/intraday_trading_list_result.php'
    else:
        url = 'http://www.twse.com.tw/exchangeReport/TWTB4U'

    try:
        resp = requests.get(url=url)
        content = json.loads(resp.content)
        if opt == COUNTER:
            return content['aaData']
        else:
            return content['data']
    except Exception as e:
        print 'Got exception at getCurrentList'
        print e
        sys.exit(-1)


def main(opt):
    content = getCurrentList(opt)
    candidates = [d[0] for d in content]
    print "(" + opt + ") Total " + str(len(candidates)) + " symbols."

    fo = open("List" + opt + ".txt","w")
    for symbol in candidates:
        fo.write(symbol + '\n')
    fo.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        opt = sys.argv[1]
    else:
        opt = STOCK
    main(opt)