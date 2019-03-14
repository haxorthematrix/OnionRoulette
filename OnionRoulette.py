import sys
import requests
import argparse
proxies = {'http': "socks5h://127.0.0.1:9050"}
infile=""
outfile=""

parser = argparse.ArgumentParser(description='.onion link validator, aka .onion roulette')
parser.add_argument('-i','--infile', help='Input file with list of addresses to test, proceeded by URL IE http://', required=True)
parser.add_argument('-o','--outfile', help='Output file for list of working sites', required=True)

args = parser.parse_args()

input_file = open(args.infile,'r')
output_file = open(args.outfile,'w')

for i in input_file.readlines():
     try:
          i = i.rstrip('\n')
          r = requests.get(i, proxies=proxies, allow_redirects=False, timeout=5) 
          output_file.write(r.url)
          output_file.write('\n')
          print(r.url, r.status_code)
     except requests.exceptions.Timeout:
          # Maybe set up for a retry, or continue in a retry loop
          print(i, 'timed out')
     except requests.exceptions.TooManyRedirects:
          # Tell the user their URL was bad and try a different one
          print(i, 'had too many redirects')
     except requests.exceptions.RequestException as e:
          # catastrophic error. bail.
          print(i, "caused a catastrophic error with python requests. I'm out!")
          print(e)
          sys.exit(1)
     except requests.ConnectionError as exc:
          # filtering DNS lookup error from other connection errors
          # (until https://github.com/shazow/urllib3/issues/1003 is resolved)
          if type(exc.message) != requests.packages.urllib3.exceptions.MaxRetryError:
               raise
          reason = exc.message.reason    
          if type(reason) != requests.packages.urllib3.exceptions.NewConnectionError:
               raise
          if type(reason.message) != str:
               raise
          if ("[Errno 11001] getaddrinfo failed" in reason.message or     # Windows
               "[Errno -2] Name or service not known" in reason.message or # Linux
               "[Errno 8] nodename nor servname " in reason.message):      # OS X
               message = 'DNSLookupError'
          else:
               raise

print('Finished. Thanks for playing .onion roulette.')