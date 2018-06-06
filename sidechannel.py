import argparse
import urllib2
import urllib
import time
import sys
import os

config = {}

def get_response_delay(config, data):
	request = urllib2.Request(config["url"])
	request = set_headers(config, request)

	start = 0
	try:
		if config["verbose"]:
			print "[VERBOSE***] Sending the following data: %s" % (config["data"] % urllib.quote(data))
		
		start = time.time()
		response = urllib2.urlopen(request, (config["data"] % urllib.quote(data)))
	except:
		delay = time.time() - start
		if config["verbose"]:
			print "[VERBOSE***] Exception was raised: %s" % sys.exc_info()[0]
		return delay
	
	delay = time.time() - start	
	
	if config["verbose"]:
		print "[VERBOSE***] HTTP response for %s" % data
		print response.read()
		
	return delay

def fetch_headers(config):
	config["headers"] = {}
	for line in open(config["headers_path"]).readlines():
		key, value = line.strip().split(":", 1)
		config["headers"][key] = value

def set_headers(config, request):
	for key in config["headers"].keys():
		request.add_header(key, config["headers"][key])
	return request

def file_exists(filepath):
	if not os.path.exists(filepath):
		print "[-] %s not found" % filepath
		sys.exit(0)
	
if __name__ == "__main__":
	print "Generic Side Channel User Enumeration\nMr.Un1k0d3r RingZer0 Team 2017\n\n"
	
	parser = argparse.ArgumentParser(description="Generic Side Channel Utility Options.")
	parser.add_argument('--headers', help='Path to HTTP headers file.', required=True)
	parser.add_argument('--url', help='Path the the URL', required=True)
	parser.add_argument('--data', help='Post data (Fuzzing point need to be replaced by a %s)', required=True)
	parser.add_argument('--default', help='Default value use a benchmark for the side channel', required=True)
	parser.add_argument('--list', help='Path to the file that contain the list of users', required=True)
	parser.add_argument('--delay', help='Delay between valid and invalid value (in milliseconds 0.01)', required=True)
	parser.add_argument('--gt', nargs='?', default=False, help='Will be considered valid it greater than (default is less than)')
	parser.add_argument('--verbose', nargs='?', default=False, help='Enable Verbose mode')
	args = parser.parse_args()

	config["url"] = args.url
	config["data"] = args.data
	config["headers_path"] = args.headers
	config["verbose"] = args.verbose
	config["default"] = args.default
	config["gt"] = args.gt
	config["list"] = args.list
	config["delay"] = float(args.delay)

	benchmark = get_response_delay(config, config["default"])
	
	file_exists(config["list"])
	file_exists(config["headers_path"])
	fetch_headers(config)
	
	print "[+] Benchmark for the valid user %s is %f" % (config["default"], benchmark)
	
	keyword = "slower"
	if config["gt"]:
		keyword = "faster"

	output = "Everything %s than %f will be considered valid" % (keyword, float(benchmark - delay))
	print "[+] %s" % output
		
	for user in open(config["list"], "rb").readlines():
		user = user.strip()
		current = get_response_delay(config, user)
		
		if config["verbose"]:
			print "[VERBOSE***] %s response time is %f" % (user, current)
			
		if config["gt"]:
			if current >= benchmark - delay:
				print "[SUCCESS] %s is valid. benchmark is %f" % (user, current)
		elif current <= benchmark - delay:
			print "[SUCCESS] %s is valid" % user
		else:
			print "[FAILED] %s is NOT valid. benchmark is %f" % (user, current)
