from urllib.request import urlopen
from feedreader.feedobjects import Feed
from feedparser import parse
from config import url_file

def update(url_feed_map):
	
	with open(url_file, 'r') as f:
		for line in f:
			url = line.strip()
			fp_obj = parse(url)
			if url in url_feed_map:
				url_feed_map[url].update(fp_obj)
			else:
				url_feed_map[url] = fp_obj
	return url_feed_map
