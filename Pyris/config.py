from os import mkdir
from os.path import expanduser, join, isdir

conf_dir = expanduser('~/.pyris')
conf_file = join(conf_dir, 'config')
url_file = join(conf_dir, 'urls')
stored_dir = join(conf_dir, 'stored')

def setup_conf():
    if not isdir(conf_dir):
        mkdir(conf_dir)
    if not isdir(stored_dir):
        mkdir(stored_dir)
