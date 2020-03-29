from pickle import dump
from config import stored_dir, url_file
from os.path import join

def to_pkl(feed):
    # name of storage file is hash(url) for now, for uniqueness.
    fname = str(hash(feed.url))
    fp_obj = feed.fp_obj
    stored_file = join(stored_dir, fname)
    with open(stored_file, 'wb') as f:
            dump(fp_obj, f)
