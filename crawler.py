# -*- coding: utf-8 -*-
# !/usr/bin/env python


import mechanize
import datetime
import json
from lxml import html, cssselect


def select_form_by_name(name):
    for form in br.forms():
        if form.name == name:
            return form


# Returns informations regarding the time of departures of a requested station.
def request_station_info(station, on, at):
    br = mechanize.Browser()
    br.open('http://www.hvv.de/fahrplaene/abfahrten/index.php')
    br.select_form(name="departure-listing-form")

    # Make form request.
    br.form["station"] = station
    br.form["on"] = on
    br.form["at"] = at

    # response_html_str = br.submit().read()
    # save_string_to_file(response_html_str, 'response_html.html')

    response_html_str = get_string_of_file('response_html.html')
    tree = html.fromstring(response_html_str)
    stations_unfiltered = tree.cssselect(".standard.departures-listing td")
    station_filtered = []
    for station in stations_unfiltered:
        if not station.text is None:
            station_filtered.append(station.text.encode("utf-8").strip())

    stations = station_filtered[0::2]
    etas = station_filtered[1::2]
    output = {"departure-times": []}
    for station, time in zip(stations, etas):
        output["departure-times"].append({"station": station, "departure-time": time})
    print output
    return output


def save_string_to_file(string, filename):
    with open(filename, 'w') as file:
        file.write(string)


def get_string_of_file(filename):
    with open(filename, 'r') as file:
        return file.read()


if __name__ == "__main__":
    filename = ""
    now = datetime.datetime.now()
    on = str(now.day) + "." + str(now.month) + "." + str(now.year)
    at = str(now.hour) + ":" + str(now.minute)
    response_json = request_station_info("Hallerstrasse", on, at)
    # response_json =
    print json.dumps(response_json, sort_keys=True, indent=4, separators=(',', ': '))
