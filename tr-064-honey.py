#!/usr/bin/env python
#
# usage:
#       iptables -I INPUT -p tcp --dport 7547 -j ACCEPT
#       ./tr-064-honey.py
# read more at:
# https://badcyber.com/new-mirai-attack-vector-bot-exploits-a-recently-discovered-router-vulnerability/

from twisted.web import server, resource
from twisted.internet import reactor, endpoints
from time import time
from collections import namedtuple
from geoip import geolite2

# Tunables:
PORT = "tcp:7547"

try:
    import config
    DB = config.db
except ImportError:
    DB = None

ev = namedtuple("attack_event", "ts ip country payload data")
if DB:
    import dataset

def insert_data(rec):
    if DB:
        db_conn = dataset.connect(DB)
        attacks_table = db_conn['attacks']
        attacks_table.insert(rec)

def parse_ntp(data):
    try:
        return data.split("NewNTPServer1>")[1][:-2]
    except IndexError:
        return "unable to parse"

def banner():
    print("Ready, listening on: {}...".format(PORT))
    print("be sure to allow incoming traffic.")
    print("="*40)

def country_lookup(ipaddr):
    try:
        return geolite2.lookup(ipaddr).country
    except:
        return "None"

class Counter(resource.Resource):
    isLeaf = True
    numberRequests = 0

    def render_POST(self, request):
        data = request.content.read()
        ip = request.getClientIP()
        attack = ev(time(), ip, country_lookup(ip), parse_ntp(data), data)
        print("{:0.0f} {}\t({})\tpayload:{}".format(*attack[:4]))
        with open("mirai.log", "a") as fd:
            fd.write(str(attack))
            fd.write("\n")
        insert_data(attack._asdict())
        self.numberRequests += 1
        request.setHeader(b"content-type", b"text/plain")
        content = u"Ticking away the moments that make up a dull day\n"
        return content.encode("ascii")

if __name__ == "__main__":
    endpoints.serverFromString(reactor, PORT).listen(server.Site(Counter()))
    banner()
    reactor.run()
