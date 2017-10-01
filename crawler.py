# -*- coding: utf-8 -*-
# !/usr/bin/env python


import mechanize
import datetime
from lxml import html, cssselect


def select_form_by_name(name):
    for form in br.forms():
        if form.name == name:
            return form


def request_station_info(station):
    br = mechanize.Browser()
    br.open('http://www.hvv.de/fahrplaene/abfahrten/index.php')
    br.select_form(name="departure-listing-form")

    # Make form request.
    now = datetime.datetime.now()
    br.form["station"] = station
    br.form["on"] = str(now.day) + "." + str(now.month) + "." + str(now.year)
    br.form["at"] = str(now.hour) + ":" + str(now.minute)
    return br.submit().read()


def save_string_to_file(filename, string):
    with open(filename, 'w') as file:
        file.write(string)


def get_string_of_file(filename):
    with open(filename, 'r') as file:
        return file.read()


if __name__ == "__main__":
    file_name = "response_html.html"
    response_html_str = request_station_info("Hallerstrasse")
    # response_html_str = get_string_of_file(file_name)

    tree = html.fromstring(response_html_str)
    stations_unfiltered = tree.cssselect(".standard.departures-listing td")
    station_filtered = []
    for station in stations_unfiltered:
        if not station.text is None:
            station_filtered.append(station.text.encode("utf-8").strip())

    stations = station_filtered[0::2]
    etas = station_filtered[1::2]
    for station, time in zip(stations, etas):
        print station + "\t" + time
