# Onion Roulette

In the process of digging through "the dark web" and attempting to find specific information at .onion TOR hidden service addresses, I quickly became annoyed at manually searching and weeding out which sites were available and which had moved on.

OnionRoulette is intended to take an input list of .onion addresses, attempt to connect to them over the specified protocol and obtain the HTTP status code.  If a 2XX, 3XX or 4XX is returned the host is considered up and the URL is written to a new file for later investigation.  If no response is recieved or times out, it moves on to the next.

Given that there is lots of questionable data out there on "the dark web", OnionRoulette only parses the HTTP status codes, and does not retain any information on the page itself, either text or images.

That said, be careful out there.

Finally, the error trapping is crap. I still get errors I haven't figured out yet, mostly due to the TOR proxy failing and requests complaining about too many retries.  It also can't tell if TOR is up, and a circuit established, so you are on your own there.  Pull requests accepted and appreciated.

## Requirements

OnionRoulette is written in python3, so you'll need python3, obviously.  pip3 is also helpfull for installing the required python modules.

You'll also need python requests: 

```pip3 install requests```

Additionally, OnionRoulette requires the command line version of tor, up and running with a completed circuit.  Mine, by default started a SOCK5 proxy on localhost:9050, so that is how OnionRoulette is configured.  You can update for your own local configuration by modifying the following line in OnionRoulette.py:

```proxies = {'http': "socks5h://127.0.0.1:9050"}```

You will also need a text file with a list of .onion addresses to check, one per line in teh following format:

```<URI><FQDN>```

Where URI is a protocol, such as http:// and FQDN is a host, such as krkzagd5yo4bvypt.onion:

```http://krkzagd5yo4bvypt.onion```

(At the time of writing, that's he hidden service for the TOR Project.)

The trailing forward slash "/" os optional, and requests to specific pages on the hosts are permissable as well:

```http://krkzagd5yo4bvypt.onion/about/overview.html.en```

## Usage

```
OnionRoulette.py [-h] -i INFILE -o OUTFILE

.onion link validator, aka .onion roulette

optional arguments:
  -h, --help            show this help message and exit
  -i INFILE, --infile INFILE
                        Input file with list of addresses to test, proceeded
                        by URL IE http://
  -o OUTFILE, --outfile OUTFILE
                        Output file for list of working sites
```                

##  Additional Notes

OnionRoulette works just as well on non-TOR hidden services, for say normal TLD enabled sites, IE https://google.com and so on.