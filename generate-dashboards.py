#!/usr/bin/python
# -*- coding: utf-8; -*-

import copy
import sys
import os, os.path
import json
import re

places = {
	"Adorf": {
		'regex': '^A-.*',
		'filename': "adorf.json",
	},
	"Auerbach": {
		'regex': '^AE-.*',
		'filename': "auerbach.json",
	},
	"Bad Elster": {
		'regex': '^BE-.*',
		'filename': "bad-elster.json",
	},
	"Falkenstein": {
		'regex': '^FST-.*',
		'filename': "falkenstein.json",
	},
	"Klingenthal": {
		'regex': '^K-.*',
		'filename': "klingenthal.json",
	},
	"Lengenfeld": {
		'regex': '^LEN-.*',
		'filename': "Lengenfeld.json",
	},
	"Markneukirchen": {
		'regex': '^MKN-.*',
		'filename': "markneukirchen.json",
	},
	"Oelsnitz": {
		'regex': '^OEL-.*',
		'filename': "oelsnitz.json",
	},
	"Plauen": {
		'regex': '^PL-.*',
		'filename': "plauen.json",
	},
	"Reichenbach": {
		'regex': '^RC-.*',
		'filename': "reichenbach.json",
	},
	"Rodewisch": {
		'regex': '^RDW-.*',
		'filename': "rodewisch.json",
	},
	"Schoeneck": {
		'regex': '^S-.*',
		'filename': "schoeneck.json",
	},
	"Treuen": {
		'regex': '^TR-.*',
		'filename': "treuen.json",
	},
	"City-Hotel": {
		'regex': '^PL-Neundorfer23-City-Hotel.*',
		'filename': "city-hotel.json",
	},
	"Hotel Alexandra": {
		'regex': '^PL-Bahnhof17-HotelAlexandra.*',
		'filename': "hotel-alexandra.json",
	},
}

def dump_json(data, filename):
	with open(filename, 'w') as f:
		json.dump(data, f)
		f.flush()
		os.fsync(f.fileno())

def get_id_name_pairs(nodelistjson):
	id_name_pairs = []

	for node in nodelistjson['nodes']:
		if not 'id' in node:
			continue

		if not 'name' in node:
			continue

		id_pair = {
			'id': node['id'],
			'name': node['name'],
		}
		id_name_pairs.append(id_pair)

	return id_name_pairs

def filter_id_name_pairs(id_name_pairs, regex):
	r = re.compile(regex)
	return list(filter(lambda n: r.match(n['name']), id_name_pairs))

def generate_place_dashboard(id_name_pairs, place_template, title):
	place = copy.deepcopy(place_template)
	id_array = [p['id'] for p in id_name_pairs]
	id_str = ','.join(id_array)

	place['title'] = title
	place['rows'][0]['panels'][0]['targets'][0]['target'] = "alias(sumSeries(freifunk.nodes.{%s}.clients), 'Nutzer')" % (id_str)

	place['rows'][0]['panels'][1]['targets'] = []
	for p in id_name_pairs:
		target = {
			"refId": p['id'],
			"target": "alias(freifunk.nodes.%s.clients, '%s')" % (p['id'], p['name'])
		}
		place['rows'][0]['panels'][1]['targets'].append(target)

	place['rows'][0]['panels'][2]['targets'][0]['target'] = "alias(sumSeries(nonNegativeDerivative(freifunk.nodes.{%s}.traffic.rx.bytes)), 'Download')" % (id_str)
	place['rows'][0]['panels'][2]['targets'][1]['target'] = "alias(sumSeries(nonNegativeDerivative(freifunk.nodes.{%s}.traffic.tx.bytes)), 'Upload')" % (id_str)
	place['rows'][0]['panels'][2]['targets'][2]['target'] = "alias(sumSeries(nonNegativeDerivative(freifunk.nodes.{%s}.traffic.forward.bytes)), 'Mesh')" % (id_str)

	return place

def generate_places(id_name_pairs, templatepath, outpath):
	place_template = json.load(open(os.path.join(templatepath, "place.json")))

	for title in places:
		regex = places[title]['regex']
		filename = places[title]['filename']

		place_pairs = filter_id_name_pairs(id_name_pairs, regex)

		dashboard = generate_place_dashboard(place_pairs, place_template, title)

		outfile = os.path.join(outpath, filename)
		outfiletmp = os.path.join(outpath, '%s.tmp' % (filename))

		dump_json(dashboard, outfiletmp)
		os.rename(outfiletmp, outfile)

def generate_nodegroup(id_name_pairs, templatepath, outpath):
	dashboard = json.load(open(os.path.join(templatepath, "nodegroup.json")))
	filename = 'nodegroup.json'

	dashboard['templating']['list'][0]['options'] = []
	options = []
	for p in id_name_pairs:
		option = {
			"value": p['id'],
			"text": "%s (%s)" % (p['name'], p['id']),
			"selected": False
		}
		options.append(option)

	options = sorted(options, key=lambda k: k['text'])
	if options:
		options[0]['selected'] = True
		dashboard['templating']['list'][0]['current'] = {
			"tags": [],
			"text": options[0]["text"],
			"value": options[0]["value"]
		}

	dashboard['templating']['list'][0]['options'] = options
	outfile = os.path.join(outpath, filename)
	outfiletmp = os.path.join(outpath, '%s.tmp' % (filename))

	dump_json(dashboard, outfiletmp)
	os.rename(outfiletmp, outfile)

def generate_node(id_name_pairs, templatepath, outpath):
	dashboard = json.load(open(os.path.join(templatepath, "node.json")))
	filename = 'node.json'

	dashboard['templating']['list'][0]['options'] = []
	options = []
	for p in id_name_pairs:
		option = {
			"value": p['id'],
			"text": p['name'],
			"selected": False
		}
		options.append(option)

	options = sorted(options, key=lambda k: k['text'])
	if options:
		options[0]['selected'] = True
		dashboard['templating']['list'][0]['current'] = {
			"tags": [],
			"text": options[0]["text"],
			"value": options[0]["value"]
		}

	dashboard['templating']['list'][0]['options'] = options
	outfile = os.path.join(outpath, filename)
	outfiletmp = os.path.join(outpath, '%s.tmp' % (filename))

	dump_json(dashboard, outfiletmp)
	os.rename(outfiletmp, outfile)

def main():
	if len(sys.argv) != 4:
		print("./generate-dashboards.py NODELIST TEMPLATEPATH OUTPATH")
		sys.exit(1)

	nodelistjson = sys.argv[1]
	templatepath = sys.argv[2]
	outpath = sys.argv[3]

	# load
	nodelist = json.load(open(nodelistjson))
	id_name_pairs = get_id_name_pairs(nodelist)

	# store
	generate_places(id_name_pairs, templatepath, outpath)
	generate_nodegroup(id_name_pairs, templatepath, outpath)
	generate_node(id_name_pairs, templatepath, outpath)

if __name__ == "__main__":
	main()
