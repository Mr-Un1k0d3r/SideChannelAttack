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
                        print "[VERBOSE***] Exception was raised: %s" % sys.exc_info()[1]
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

if __name__ == "__main__":
        print "Benchmark Side Channel Tool\nMr.Un1k0d3r RingZer0 Team 2017\n\n"

        parser = argparse.ArgumentParser(description="ClickOnceGenerator Options.")
        parser.add_argument('--headers', help='Path to HTTP headers file.')
        parser.add_argument('--url', help='Path the the URL')
        parser.add_argument('--data', help='Post data')
        parser.add_argument('--default', help='Default value use a benchmark for the side channel')
        parser.add_argument('--round', help='Number of rounds')
        parser.add_argument('--verbose', nargs='?', default=False, help='Enable Verbose mode')
        args = parser.parse_args()

        config["url"] = args.url
        config["data"] = args.data
        config["headers_path"] = args.headers
        config["verbose"] = args.verbose
        config["default"] = args.default
        config["round"] = int(args.round)

        if not os.path.exists(config["headers_path"]):
                print "[-] %s not found. Cannot load HTTP headers" % filepath
                sys.exit(0)

        fetch_headers(config)

        i = 0
        while i < config["round"]:
                benchmark = get_response_delay(config, config["default"])
                print "[+] Delay for %s is %f" % (config["default"], benchmark)
                i += 1

        i = 0
        while i < config["round"]:
                current =  str(int(config["default"]) + i + 1)
                benchmark = get_response_delay(config, current)
                print "[+] Delay for %s is %f" % (current, benchmark)
                i += 1
