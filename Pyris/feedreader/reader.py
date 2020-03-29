from ui.interface import Interface
from feedreader.components.final import FeedList, Feed, FeedEntry
import pickle

class FeedReader:
    """This class should contain the 3 component classes."""
    
    def __init__(self):
        feeds = self.load()
        self.feed_list = FeedList(feeds)
    
    def load(self, fpath='/home/alan/bin/pyris/testing/test_feeds.pkl'):
        """This should be changed"""
        with open(fpath, 'rb') as f:
            return pickle.load(f)
