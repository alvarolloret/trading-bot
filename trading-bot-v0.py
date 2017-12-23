# imported files
import time
import sys
try:
    import httplib
except:
    import http.client as httplib
from poloniex import poloniex 

api_key='RZPH057A-1L01XZUI-TL2ZCFLP-0QK92K9J'
api_secret='f50a8cd597bca93d33e997603b754277ac7e7e98e4ed4da37470f7d184639af089278633bbe9aac3e54da0042673823fcd3d8a5c34112396b4a158a9203ab698'


# Internet checking for connection, see : https://stackoverflow.com/a/29854274/5176549
def have_internet():
    conn = httplib.HTTPConnection("www.google.com", timeout=5)
    try:
	conn.request("HEAD", "/")
	conn.close()
	print "Connection made"
	return True
    except:
	print "Connection failed"
	conn.close()
	return False

# Poloniex basic examples: https://github.com/s4w3d0ff/python-poloniex
def poliex_test(key, secret):
	polo=poloniex(key,secret)
	print(polo.returnTicker()['BTC_ETC'])
	return


def main(argv):
	period = 1 #in seconds
	have_internet()
	poliex_test(api_key,api_secret)
	while True:
		print "period"
		time.sleep(period)

if __name__ == "__main__":
	main(sys.argv[1:])