#!/usr/bin/env python

import config
import dataset
from tabulate import tabulate
from collections import namedtuple

ev = namedtuple("attack_event", "ts ip country payload")

db_conn = dataset.connect(config.db)
result = db_conn['attacks']
table = []
for l in result:
    table.append(ev(l['ts'], l['ip'], l['country'], l['payload']))
print(tabulate(table, headers="keys", floatfmt=".0f"))
