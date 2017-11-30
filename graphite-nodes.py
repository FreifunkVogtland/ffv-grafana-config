#!/usr/bin/python
# -*- coding: utf-8; -*-

import sys
import json
import time

def get_nodes_count(nodes):
	onlinenodes_count = 0
	offlinenodes_count = 0

	for n in nodes['nodes']:
		if not 'statistics' in n:
			continue

		if not 'flags' in n:
			continue

		if not 'online' in n['flags']:
			continue

		if not n['flags']['online']:
			offlinenodes_count += 1
		else:
			onlinenodes_count += 1

	return (onlinenodes_count, offlinenodes_count)

def main():
	if len(sys.argv) != 2:
		print("./graphite-nodes.py NODESJSON")
		sys.exit(1)

	nodesjson = sys.argv[1]

	# load
	nodes = json.load(open(nodesjson))
	(onlinenodes_count, offlinenodes_count) = get_nodes_count(nodes)

	timestamp = int(time.time())
	print("freifunk.global.onlinenodes %u %u" % (onlinenodes_count, timestamp))
	print("freifunk.global.offlinenodes %u %u" % (offlinenodes_count, timestamp))
	print("freifunk.global.nodes %u %u" % (onlinenodes_count + offlinenodes_count, timestamp))

if __name__ == "__main__":
	main()
