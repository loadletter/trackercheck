#!/usr/bin/env python2
import sys
from multiprocessing.pool import ThreadPool
from threading import Lock
from scraper import scrape

def process_url(url, lock):
	try:
		scrape(url, ['25BE9FC43266847BD8271E417AF8CF048D46E5CD'])
	except Exception:
		if not PRINT_GOOD:
			with lock:
				print url
	else:
		if PRINT_GOOD:
			with lock:
				print url

def main():
	pool = ThreadPool(processes=10)
	outlock = Lock()
	for line in sys.stdin:
		s = line.strip()
		if s:
			pool.apply_async(process_url, [s, outlock])
	pool.close()
	pool.join()

if __name__ == "__main__":
	if len(sys.argv) != 2 or sys.argv[1].lower() not in ['good', 'bad']:
		print >>sys.stderr, "Usage:", sys.argv[0], "[good|bad]"
		print >>sys.stderr, "This script takes a list of torrent trackers and spits out the good/bad ones"
		print >>sys.stderr, "ie: cat mytrackers.txt | sort -u |", sys.argv[0], "bad"
		sys.exit(2)
	if sys.argv[1].lower() == 'good':
		PRINT_GOOD = True
	else:
		PRINT_GOOD = False
	main()
