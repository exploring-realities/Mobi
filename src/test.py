#!/usr/bin/python
import datetime
import crawler

now = datetime.datetime.now()
on = str(now.day) + "." + str(now.month) + "." + str(now.year)
at = str(now.hour) + ":" + str(now.minute)
response_json = crawler.request_station_info("Hallerstrasse", at, on)
print response_json