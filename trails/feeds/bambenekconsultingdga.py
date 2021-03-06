#!/usr/bin/env python

"""
Copyright (c) 2014-2017 Miroslav Stampar (@stamparm)
See the file 'LICENSE' for copying permission
"""

import gzip
import os
import re
import tempfile
import urllib2

from core.settings import NAME
from core.settings import TIMEOUT

__url__ = "http://osint.bambenekconsulting.com/feeds/dga-feed.txt"
__check__ = "Domain used by"
__reference__ = "bambenekconsulting.com"

def _open():
    retval = None

    try:
        req = urllib2.Request(__url__, None, {"User-agent": NAME, "Accept-encoding": "gzip"})
        resp = urllib2.urlopen(req, timeout=TIMEOUT)
        handle, filename = tempfile.mkstemp()

        bsize = 1024 * 1024
        while True:
            content = resp.read(bsize)
            if content:
                os.write(handle, content)
                if len(content) != bsize:
                    break
            else:
                break

        os.close(handle)
        retval = gzip.open(filename)

    except Exception, ex:
        pass

    return retval

def fetch():
    retval = {}
    handle = _open()

    if handle:
        try:
            while True:
                line = handle.readline()
                if not line:
                    break
                match = re.search(r"\A([^,\s]+),Domain used by ([^ ]+)", line)
                if match:
                    retval[match.group(1)] = ("%s dga (malware)" % match.group(2).lower(), __reference__)
        except:
            pass
        finally:
            try:
                os.remove(handle.filename)
            except (IOError, OSError):
                pass

    return retval
