import urllib2
import urllib
import time
import sys
import os

debug = False
gt = False

def get_response_delay(url, data, username):
	request = urllib2.Request(url)
	request.add_header("Content-Type", "application/x-www-form-urlencoded")
	request.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:48.0) Gecko/20100101 Firefox/48.0")
	request.add_header("Referer", url)
	request.add_header("Origin",url)
	start = time.time()
	try:
		if debug:
			print "[VERBOSE***] Sending the following data: %s" % (data % urllib.quote(username))
		response = urllib2.urlopen(request, (data % urllib.quote(username)))
	except:
		if debug:
			print "[VERBOSE***] Exception was raised: %s" % sys.exc_info()[0]
			return -1
	
	delay = time.time() - start	
	
	if debug:
		print "[VERBOSE***] HTTP response for %s" % username
		print response.read()
		
	return delay

if __name__ == "__main__":
	print "Generic Side Channel User Enumeration\nMr.Un1k0d3r RingZer0 Team 2017\n\n"
	
	if len(sys.argv) < 6:
		print "Usage: python %s [url] [valid_user] [path] [delay] [data] -verbose -gt\n" % sys.argv[0]
		print "\tUrl                Full url to the API (http://url.com/api/v1/...)"
		print "\tValid User         Valid user to benchmark the delay"
		print "\tPath               Path to a list of username"
		print "\tDelay              Delay used for benchmark (milliseconds) Ex: 0.1"
		print "\tData               Post data (%s need to be placed somewhere instead of the username)"
		print "\tVerbose            Verbose output"
		print "\tGreater than (-gt) Will check if it's greater than"
		sys.exit(0)

	if "-verbose" in sys.argv:
		debug = True
	
	if  "-gt" in sys.argv:
		gt = True
		
	url = sys.argv[1]
	username = sys.argv[2]

	filepath = sys.argv[3]
	delay = float(sys.argv[4])
	data = sys.argv[5]

	if not os.path.exists(filepath):
		print "[-] %s not found" % filepath
		sys.exit(0)

	benchmark = get_response_delay(url, data, username)
	
	print "[+] Valid user benchmark is %f" % benchmark
	keyword = "slower"
	if gt:
		keyword = "faster"

	output = "Everything %s than %f will be considered valid" % (keyword, float(benchmark - delay))
	print "[+] %s" % output
		
	for user in open(filepath, "rb").readlines():
		user = user.strip()
		current = get_response_delay(url, data, user)
		if current == -1:
			print "Can't get a proper response for %s" % user
		else:
			if debug:
				print "[VERBOSE***] %s response time is %f" % (user, current)
				
			if gt:
				if current >= benchmark - delay:
					print "[SUCCESS] %s is valid. benchmark is %f" % (user, current)
			elif current <= benchmark - delay:
				print "[SUCCESS] %s is valid" % user
			else:
				print "[FAILED] %s is NOT valid. benchmar is %f" % (user, current)
