#!/usr/bin/python
import sys, os

sys.path.insert(0, "/media/KINGSTON/Aplicaciones/")

os.environ["DJANGO_SETTINGS_MODULE"] = "jma.settings"

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
