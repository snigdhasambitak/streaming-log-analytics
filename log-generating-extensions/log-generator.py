import json
import time
import datetime
from weakref import ref
import pytz
import numpy
import random
import gzip
import zipfile
import sys
import argparse
from kafka import KafkaProducer

from faker import Faker
from random import randrange
from tzlocal import get_localzone

local = get_localzone()


class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:  # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False


parser = argparse.ArgumentParser(__file__, description="Fake Apache Log Generator")
parser.add_argument("--output", "-o", dest='output_type', help="Write to a Log file, a gzip file or to STDOUT",
                    choices=['LOG', 'GZ', 'CONSOLE'])
parser.add_argument("--log-format", "-l", dest='log_format', help="Log format, Common or Extended Log Format ",
                    choices=['CLF', 'ELF'], default="ELF")
parser.add_argument("--num", "-n", dest='num_lines', help="Number of lines to generate (0 for infinite)", type=int,
                    default=1)
parser.add_argument("--prefix", "-p", dest='file_prefix', help="Prefix the output file name", type=str)
parser.add_argument("--sleep", "-s", help="Sleep this long between lines (in seconds)", default=0.0, type=float)
parser.add_argument("--filename", "-f", dest='file_name', help="Log File name", type=str)
args = parser.parse_args()

log_lines = args.num_lines
file_prefix = args.file_prefix
output_type = args.output_type
log_format = args.log_format
file_name = args.file_name

faker = Faker()

timestr = time.strftime("%Y%m%d-%H%M%S")
otime = datetime.datetime.now()

outFileName = 'access_log_' + timestr + '.log' if not file_prefix else file_prefix + '_access_log_' + timestr + '.log'
outFileName = outFileName if not file_name else file_name

for case in switch(output_type):
    if case('LOG'):
        f = open(outFileName, 'w')
        break
    if case('GZ'):
        f = gzip.open(outFileName + '.gz', 'w')
        break
    if case('CONSOLE'): pass
    if case():
        f = sys.stdout

response = ["200", "404", "500", "301"]

verb = ["GET", "POST", "DELETE", "PUT"]
resources = ["/list", "/wp-content", "/wp-admin", "/explore", "/search/tag/list", "/app/main/posts",
             "/posts/posts/explore", "/apps/cart.jsp?appID="]
uaList = [faker.firefox, faker.chrome, faker.safari, faker.internet_explorer, faker.opera]

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))

flag = True
counter = 1
while flag:
    if args.sleep:
        increment = datetime.timedelta(seconds=args.sleep)
    else:
        increment = datetime.timedelta(seconds=random.randint(30, 300))
    otime += increment

    ip = faker.ipv4()
    dt = otime.strftime('%d/%b/%Y:%H:%M:%S')
    tz = datetime.datetime.now(local).strftime('%z')
    vrb = numpy.random.choice(verb, p=[0.6, 0.1, 0.1, 0.2])

    uri = random.choice(resources)
    if uri.find("apps") > 0:
        uri += str(random.randint(1000, 10000))

    resp = numpy.random.choice(response, p=[0.9, 0.04, 0.02, 0.04])
    byt = int(random.gauss(5000, 50))
    referer = faker.uri()
    useragent = numpy.random.choice(uaList, p=[0.5, 0.3, 0.1, 0.05, 0.05])()
    log_obj = {
        "id": counter,
        "ip": ip,
        "timestamp": dt,
        "timezone": tz,
        "method": vrb,
        "url": uri,
        "response_code": resp,
        "response_bytes": byt,
        "referrer": referer,
        "user_agent": useragent
    }
    ack = producer.send("log", value=log_obj)
    f.write(json.dumps(log_obj) + "\n")
    f.flush()
    log_lines = log_lines - 1
    counter = counter + 1
    flag = False if log_lines == 0 else True
    if args.sleep:
        time.sleep(args.sleep)
producer.flush()
producer.close()

# Run infinitely with a gap of 5 sec within two logs
# python3 apache-fake-log-gen.py -n 0 -o LOG -f .\logs\apache_logs.log -s 5
