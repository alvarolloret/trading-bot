import time
import sys
	
try:
    import httplib
except:
    import http.client as httplib
  
  
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

def main(argv):
	period = 10
	have_internet()
	while True:
		print "period"
		time.sleep(period)

if __name__ == "__main__":
	main(sys.argv[1:])