# -*- coding: utf-8 -*-
#!/usr/bin/env python


import mechanize
import datetime
from lxml import html, cssselect

now = datetime.datetime.now()
br = mechanize.Browser()


def select_form_by_name(name):
	for form in br.forms():
		if form.name == name:
			return form

response = br.open('http://www.hvv.de/fahrplaene/abfahrten/index.php')

form  = br.select_form(name="departure-listing-form")

br.form["station"] = "Saarlandstrasse"
br.form["on"] = str(now.day) + "." + str(now.month) + "." + str(now.year)
br.form["at"] =  str(now.hour) + ":" + str(now.minute)



tree = html.fromstring(br.submit().read())
elements  = tree.cssselect(".standard.departures-listing td")
stationen =  elements[::2]
print elements
for station in stationen:
	if isinstance(station.text, unicode):
		print station.text.encode("utf-8"), station.text
	print station.text



