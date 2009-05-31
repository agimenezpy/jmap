#!/usr/bin/python
import sys, os

sys.path.insert(0, "/home/agimenez/Desktop/jmawiki/jma/")

os.environ["DJANGO_SETTINGS_MODULE"] = "web.settings"

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
