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
def request_station_info(station, at, on):
    br = mechanize.Browser()
    br.open('http://www.hvv.de/fahrplaene/abfahrten/index.php')
    br.select_form(name="departure-listing-form")

    # Make form request.
    br.form["station"] = station
    br.form["at"] = at
    br.form["on"] = on

    response_html_str = br.submit().read()
    # response_html_str = get_string_of_file('response_html_timeout.html')
    # save_string_to_file(response_html_str, 'response_html_timeout.html')

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

    if output["departure-times"] == []:
        error_header = tree.cssselect("h2.error")[0]
        output.update({"error": error_header.text})

    return output


def request_route_info(current, target):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open('http://geofox.hvv.de/jsf/home.seam?clear=true&language=de')
    br.select_form(name="personalSearch")
    print br.form


def save_string_to_file(string, filename):
    with open(filename, 'w') as file:
        file.write(string)


def get_string_of_file(filename):
    with open(filename, 'r') as file:
        return file.read()


# request_route_info(1, 2)
