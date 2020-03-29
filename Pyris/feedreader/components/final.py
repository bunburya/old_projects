from feedparser import parse

from feedreader.components.base import BaseObject, BaseListObject
from feedreader.htmlhandler import HTMLHandler
from feedreader.serialize.save import to_pkl
        
class Feed(BaseListObject):
    
    def __init__(self, fp_obj, get_attrs=True):
        self.fp_obj = fp_obj
        self.get_attrs()
        entries = [FeedEntry(e, self) for e in fp_obj.entries]
        self.unread = set(entries)
        self.important = set()
        
        BaseListObject.__init__(self, entries)
    
    def select_item(self, item=None):
        BaseListObject.select_item(self, item, mark_read=True)
    
    def get_attrs(self):
        """Takes the attrs we need from the parsed object."""
        fp_obj = self.fp_obj
        self._title = fp_obj.feed.get('title', None)
        self.url = fp_obj.get('url', None)
        self.updated = fp_obj.feed.get('updated', None)
            
    def update(self):
        new = parse(self.url)
        self.fp_obj.update(new)
        self.get_attrs()
        self.store()

    def store(self):
        """In future this will store the feed to a file."""
        pass

    @property
    def title_only(self):
        """Returns the feed title, without any trailing indicators."""
        return self._title

    @property
    def title(self):
        """Returns feed title plus an indicator of number unread."""
        uc = self.unread_count
        if uc > 0:
            return '{0} ({1})'.format(self._title, uc)
        else:
            return self._title
    
    @property
    def is_read(self):
        return self.unread_count == 0
    
    @property
    def unread_count(self):
        return len(self.unread)

class FeedList(BaseListObject):
    
    def __init__(self, feeds):
        BaseListObject.__init__(self, feeds)
        
    def mark_item_read(self, item, read):
        item.mark_self_read(read)
    
    def mark_self_read(self, read):
        for i in self.items:
            i.mark_self_read()
    
    @property
    def feed_count(self):
        return len(self.items)
    
    @property
    def entry_count(self):
        return sum(len(i) for i in self.items)


class FeedEntry(BaseObject):
    
    def __init__(self, parsed, parent):
        """This currently takes the feed entry and takes the info we need,
        discarding the rest."""
        self.parsed = parsed
        self.get_attrs()
        self.parent = parent

        BaseObject.__init__(self)
    
    def get_attrs(self):
        parsed = self.parsed
        self.title = parsed.get('title', None)
        self.link = parsed.get('link', None)
        self.updated = parsed.get('updated')
        self.author = parsed.get('author', None)
        self.summary = parsed.get('summary', None)
        try:
            raw_data = parsed.content[0].value
            handler = HTMLHandler()
            handler.feed(raw_data)
            self.text = handler.get()
            self.summary_only = False
        except AttributeError:
            self.text = self.summary
            self.summary_only = True
    
    def mark_self_read(self, read=True):
        self.parent.is_changed = True
        if self._seen != read:
            self._seen = read
            if read:
                self.parent.unread.discard(self)
            else:
                self.parent.unread.add(self)
    
    def mark_self_important(self, important=True):
        if self.is_important != important:
            self.is_important = important
            if important:
                self.parent.important.add(self)
            else:
                self.parent.important.discard(self)
    
    @property
    def is_read(self):
        return self._seen
