#!/usr/bin/python
# -*- coding: utf-8; -*-

import whisper
import glob
import sys

start = 1475625600
end = 1481312640

def main():
	timedict = {}
	fnum = 0

	for t in range(start, end, 60):
		timedict[t] = None

	x = 0
	files = glob.glob('input/*/clients.wsp')
	for f in files:
		fnum += 1
		sys.stderr.write("%u of %u\n" % (fnum, len(files)))

		for t in range(start, end, 60):
			(tinfo, values) = whisper.fetch(f, t, t + 60)
			if len(values) != 1:
				continue

			if values[0] == None:
				continue

			if timedict[t] == None:
				timedict[t] = 0

			print values
			x += values[0]

			timedict[t] += int(values[0])

	for t in timedict:
		if timedict[t] == None:
			continue

		print("freifunk.global.clients %u %u" % (timedict[t], t))

if __name__ == "__main__":
	main()
