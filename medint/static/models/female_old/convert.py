#!/usr/bin/env python

import re

f = open('out.js.backup')
for l in f:
    if not re.match('^\d+', l) and l:
      print l[:-1]