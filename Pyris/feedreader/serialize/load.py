from pickle import load
from os.path import join, exists
from config import stored_dir, url_file

def from_pkl():
    feed_list = []
    with open(url_file, 'r') as f:
        for line in f:
            url = line.strip()
            fname = str(hash(url))
            stored_file = join(stored_dir, fname)
            if exists(stored_file):
                with open(stored_file, 'rb') as f:
                    feed = load(f)
                feed_list.append(feed)
    return feed_list
