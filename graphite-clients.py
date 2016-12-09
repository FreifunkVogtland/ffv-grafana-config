#!/usr/bin/python
# -*- coding: utf-8; -*-

import sys
import json
import time

def get_client_count(nodes):
	client_count = 0

	for n in nodes['nodes']:
		if not 'statistics' in n:
			continue

		if not 'flags' in n:
			continue

		if not 'online' in n['flags']:
			continue

		if not n['flags']['online']:
			continue

		if not 'clients' in n['statistics']:
			continue

		client_count += n['statistics']['clients']

	return client_count

def main():
	if len(sys.argv) != 2:
		print("./graphite-clients.py NODESJSON")
		sys.exit(1)

	nodesjson = sys.argv[1]

	# load
	nodes = json.load(open(nodesjson))
	client_count = get_client_count(nodes)

	timestamp = int(time.time())
	print("freifunk.global.clients %u %u" % (client_count, timestamp))

if __name__ == "__main__":
	main()
