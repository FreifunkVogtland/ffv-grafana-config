#!/usr/bin/python3
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
		'tags': [
			'place',
			'municipality',
		],
	},
	"Auerbach": {
		'regex': '^AE-.*',
		'filename': "auerbach.json",
		'tags': [
			'place',
			'municipality',
		],
	},
	"Bad Brambach": {
		'regex': '^BB-.*',
		'filename': "bad-brambach.json",
		'tags': [
			'place',
			'municipality',
		],
	},
	"Bad Elster": {
		'regex': '^BE-.*',
		'filename': "bad-elster.json",
		'tags': [
			'place',
			'municipality',
		],
	},
	"Bergen": {
		'regex': '^B-.*',
		'filename': "bergen.json",
		'tags': [
			'place',
			'municipality',
		],
	},
	"Bösenbrunn": {
		'regex': '^BOE-.*',
		'filename': "bösenbrunn.json",
		'tags': [
			'place',
			'municipality',
		],
	},
	"Eichigt": {
		'regex': '^EIC-.*',
		'filename': "eichigt.json",
		'tags': [
			'place',
			'municipality',
		],
	},
	"Ellefeld": {
		'regex': '^ELL-.*',
		'filename': "ellefeld.json",
		'tags': [
			'place',
			'municipality',
		],
	},
	"Elsterberg": {
		'regex': '^ELS-.*',
		'filename': "elsterberg.json",
		'tags': [
			'place',
			'municipality',
		],
	},
	"Falkenstein": {
		'regex': '^FST-.*',
		'filename': "falkenstein.json",
		'tags': [
			'place',
			'municipality',
		],
	},
	"Grünbach": {
		'regex': '^GB-.*',
		'filename': "gruenbach.json",
		'tags': [
			'place',
			'municipality',
		],
	},
	"Heinsdorfergrund": {
		'regex': '^HDG-.*',
		'filename': "heinsdorfergrund.json",
		'tags': [
			'place',
			'municipality',
		],
	},
	"Klingenthal": {
		'regex': '^K-.*',
		'filename': "klingenthal.json",
		'tags': [
			'place',
			'municipality',
		],
	},
	"Lengenfeld": {
		'regex': '^LE-.*',
		'filename': "lengenfeld.json",
		'tags': [
			'place',
			'municipality',
		],
	},
	"Limbach": {
		'regex': '^LIM-.*',
		'filename': "limbach.json",
		'tags': [
			'place',
			'municipality',
		],
	},
	"Markneukirchen": {
		'regex': '^MKN-.*',
		'filename': "markneukirchen.json",
		'tags': [
			'place',
			'municipality',
		],
	},
	"Mühlental": {
		'regex': '^MTL-.*',
		'filename': "muehlental.json",
		'tags': [
			'place',
			'municipality',
		],
	},
	"Muldenhammer": {
		'regex': '^MH-.*',
		'filename': "muldenhammer.json",
		'tags': [
			'place',
			'municipality',
		],
	},
	"Netzschkau": {
		'regex': '^N-.*',
		'filename': "netzschkau.json",
		'tags': [
			'place',
			'municipality',
		],
	},
	"Neuensalz": {
		'regex': '^NSZ-.*',
		'filename': "neuensalz.json",
		'tags': [
			'place',
			'municipality',
		],
	},
	"Neumark": {
		'regex': '^NMK-.*',
		'filename': "neumark.json",
		'tags': [
			'place',
			'municipality',
		],
	},
	"Neustadt": {
		'regex': '^NST-.*',
		'filename': "neustadt.json",
		'tags': [
			'place',
			'municipality',
		],
	},
	"Oelsnitz": {
		'regex': '^OEL-.*',
		'filename': "oelsnitz.json",
		'tags': [
			'place',
			'municipality',
		],
	},
	"Pausa-Mühltroff": {
		'regex': '^PMF-.*',
		'filename': "pausa-muehltroff.json",
		'tags': [
			'place',
			'municipality',
		],
	},
	"Plauen": {
		'regex': '^PL-.*',
		'filename': "plauen.json",
		'tags': [
			'place',
			'municipality',
		],
	},
	"Pöhl": {
		'regex': '^POE-.*',
		'filename': "poehl.json",
		'tags': [
			'place',
			'municipality',
		],
	},
	"Reichenbach": {
		'regex': '^RC-.*',
		'filename': "reichenbach.json",
		'tags': [
			'place',
			'municipality',
		],
	},
	"Rodewisch": {
		'regex': '^RDW-.*',
		'filename': "rodewisch.json",
		'tags': [
			'place',
			'municipality',
		],
	},
	"Rosenbach": {
		'regex': '^RBH-.*',
		'filename': "rosenbach.json",
		'tags': [
			'place',
			'municipality',
		],
	},
	"Schöneck": {
		'regex': '^S-.*',
		'filename': "schoeneck.json",
		'tags': [
			'place',
			'municipality',
		],
	},
	"Steinberg": {
		'regex': '^SBG-.*',
		'filename': "steinberg.json",
		'tags': [
			'place',
			'municipality',
		],
	},
	"Theuma": {
		'regex': '^T-.*',
		'filename': "theuma.json",
		'tags': [
			'place',
			'municipality',
		],
	},
	"Tirpersdorf": {
		'regex': '^TDF-.*',
		'filename': "tirpersdorf.json",
		'tags': [
			'place',
			'municipality',
		],
	},
	"Treuen": {
		'regex': '^TR-.*',
		'filename': "treuen.json",
		'tags': [
			'place',
			'municipality',
		],
	},
	"Triebel": {
		'regex': '^TRI-.*',
		'filename': "triebel.json",
		'tags': [
			'place',
			'municipality',
		],
	},
	"Weischlitz": {
		'regex': '^WEI-.*',
		'filename': "weischlitz.json",
		'tags': [
			'place',
			'municipality',
		],
	},
	"Werda": {
		'regex': '^WER-.*',
		'filename': "werda.json",
		'tags': [
			'place',
			'municipality',
		],
	},
	"City-Hotel": {
		'regex': '^PL-Neundorfer23-City-Hotel.*',
		'filename': "city-hotel.json",
		'tags': [
			'place',
			'venue',
		],
	},
	"Hotel Alexandra": {
		'regex': '^PL-Bahnhof17-HotelAlexandra.*',
		'filename': "hotel-alexandra.json",
		'tags': [
			'place',
			'venue',
		],
	},
	"Zum Kerkermeister - Auerbach": {
		'regex': '^AE-Kirchpl1-Kerkermeister*',
		'filename': "zum-kerkermeister.json",
		'tags': [
			'place',
			'venue',
		],
	},
	"Parkhotel": {
		'regex': '^PL-Raedel18-(Parkhotel-.*|FriesischeBotschaft)',
		'filename': "parkhotel.json",
		'tags': [
			'place',
			'venue',
		],
	},
	"KlangGarten - Kurzfilm- & Musikfestival": {
		'regex': '^PL-(Walkgasse7-ViVo|Bleich3-WeisbachschesHaus-\\d|FFV-Klanggarten\\d)',
		'filename': "klanggarten.json",
		'tags': [
			'place',
			'event',
		],
	},
}

def dump_json(data, filename):
	with open(filename, 'w') as f:
		json.dump(data, f)
		f.flush()
		os.fsync(f.fileno())

def asciify(s):
	return s.encode('ascii', 'replace').decode('ascii')

def get_id_name_pairs(nodelistjson):
	id_name_pairs = []

	for node in nodelistjson['nodes']:
		if not 'id' in node:
			continue

		if not 'name' in node:
			continue

		id_pair = {
			'id': node['id'],
			'name': asciify(node['name']),
		}
		id_name_pairs.append(id_pair)

	return id_name_pairs

def filter_id_name_pairs(id_name_pairs, regex):
	r = re.compile(regex)
	return list(filter(lambda n: r.match(n['name']), id_name_pairs))

def generate_place_dashboard(id_name_pairs, place_template, title, tags):
	place = copy.deepcopy(place_template)
	id_array = [p['id'] for p in id_name_pairs]
	id_str = ','.join(id_array)

	place['title'] = title
	place['tags'] = tags
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
		print(title)
		regex = places[title]['regex']
		filename = places[title]['filename']
		tags = places[title]['tags']

		place_pairs = filter_id_name_pairs(id_name_pairs, regex)

		dashboard = generate_place_dashboard(place_pairs, place_template, title, tags)

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
