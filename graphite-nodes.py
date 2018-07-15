#!/usr/bin/python
# -*- coding: utf-8; -*-

import json
import sys
import time


def get_nodes_count(nodes):
    onlinenodes_count = 0
    offlinenodes_count = 0

    for n in nodes['nodes']:
        if 'is_online' not in n:
            continue

        if not n['is_online']:
            offlinenodes_count += 1
        else:
            onlinenodes_count += 1

    return (onlinenodes_count, offlinenodes_count)


def main():
    if len(sys.argv) != 2:
        print("./graphite-nodes.py MESHVIEWERJSON")
        sys.exit(1)

    meshviewerjson = sys.argv[1]

    # load
    nodes = json.load(open(meshviewerjson))
    (onlinenodes_count, offlinenodes_count) = get_nodes_count(nodes)

    timestamp = int(time.time())
    print("freifunk.global.offlinenodes %u %u" % (offlinenodes_count,
                                                  timestamp))


if __name__ == "__main__":
    main()
