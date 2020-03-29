from feedreader.htmlhandler import HTMLHandler

"""TODO:
- Finish BaseObject class; it should hold data and methods common to all objects.
- Re-implement mark as read on select.
    - Use on_select and on_deselect.
    - UnreadList must mark as read only on deselect, or else it must repopulate less often
      than on every select.
- Sorting mechanisms, at least by time.
"""

class BaseObject:
    
    def __init__(self):
        self.posns = {}
        self.is_selected = set() # was self.is_selected = False
        self.is_important = False
        self.select_marks_read = False #hmmmm
        self._seen = False # was self.read
    
    def on_select(self):
        pass
    
    def on_deselect(self):
        pass
    
    def mark_self_nb(self, nb):
        self.is_important = nb
        

class BaseListObject(BaseObject):
    
    def __init__(self, items=None):
        self.is_changed = False
        self.selected = None
        BaseObject.__init__(self)
        if items is not None:
            self.populate(items)
    
    # __iter__ and __next__ could just refer to self.items's methods
    # could probably implement __getitem__ like this as well
    
    def __iter__(self):
        self.iter_posn = -1
        return self
    
    def __next__(self):
        self.iter_posn += 1
        try:
            return self.items[self.iter_posn]
        except IndexError:
            raise StopIteration
    
    def __len__(self):
        return len(self.items)
    
    def populate(self, items=None):
        if items is not None:
            self.items = items
        for p, i in enumerate(self.items):
            i.posns[self] = p
        #self.select(items[0])
    
    def select_item(self, item=None, mark_read=False):
        if item is None:
            item = self.items[0]
        self.deselect_item()
        self.selected = item
        item.is_selected.add(self)
        if mark_read: #maybe move this to item.on_select or item.on_deselect
            item.mark_self_read()
        item.on_select()
    
    def deselect_item(self):
        to_desel = self.selected
        if not (to_desel is None):
            to_desel.is_selected.remove(self)
            self.selected = None
            to_desel.on_deselect()
    
    def select_next(self):
        try:
            self.select_item(self.items[self.selected.posns[self]+1])
        except IndexError:
            pass
    
    def select_prev(self):
        if self.selected.posns[self] > 0:
            self.select_item(self.items[self.selected.posns[self]-1])
    
    # Marking read
    
    def mark_item_read(self, item, read):
        item.mark_self_read(read)
    
    def mark_all_read(self, read):
        for i in self.items:
            i.mark_self_read(read)

    def mark_self_read(self, read):
        self.mark_all_read(read)
    
    # Marking important
    
    def mark_item_nb(self, item, nb):
        item.mark_self_nb(nb)
    
    def mark_all_read(self, nb):
        for i in self.items:
            i.mark_self_read(self, nb)
    
    @property
    def sel_posn(self):
        return self.selected.posns[self]
    
    @property
    def max_len(self):
        return max(len(i.title) for i in self.items)
    
        
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
        fp_obj = self.fp_obj
        self._title = fp_obj.feed.get('title', None)
        # NB: feeds have url, entries have link
        self.url = fp_obj.feed.get('url', None)
        self.updated = fp_obj.feed.get('updated', None)
            
    @property
    def title(self):
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


class FeedEntry(BaseObject):
    
    def __init__(self, entry, parent):
        """This currently takes the feed entry and takes the info we need,
        discarding the rest."""
        self.title = entry.get('title', None)
        self.link = entry.get('link', None)
        self.updated = entry.get('updated', None)
        self.author = entry.get('author', None)
        self.summary = entry.get('summary', None)
        try:
            raw_data = entry.content[0].value
            handler = HTMLHandler()
            handler.feed(raw_data)
            self.text = handler.get()
            self.summary_only = False
        except AttributeError:
            self.text = self.summary
            self.summary_only = True
        
        self.parent = parent

        BaseObject.__init__(self)
    
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


# Below is work in progress, not workable yet.

#  UnreadList should not inherit from Feed.

class DynamicFeedObject(Feed):
    """A feed-like object whose contents change regularly. This will be
    used to implement Important, Unread etc."""
    
    def __init__(self, sources):
        self.sources = sources[:] # deepcopy is NB!!
        self.update_buffer()
        BaseListObject.__init__(self)
    
    def add_source(self, source):
        """Sources must derive from BaseListObject."""
        self.sources.append(source)

    @property
    def unread_count(self):
        return sum(i.unread_count for i in self.sources)
    
    @property
    def title(self):
        return '{0} ({1})'.format(self._title, self.unread_count)

class UnreadList(DynamicFeedObject):
    
    def __init__(self, sources=[]):
        self._title = 'Unread'
        self.is_important = False
        DynamicFeedObject.__init__(self, sources)
    
    def mark_all_read(self, read):
        for i in self.items:
            i.mark_self_read(read)
    
    #def select_item(self, item=None):
    #    BaseListObject.select_item(self, item, mark_read=False)
    
    def on_deselect(self):
        self.update_buffer()
    
    def update_buffer(self):
        buff = []
        for s in self.sources:
            buff += s.unread
        for p, i in enumerate(buff):
            i.posns[self] = p
        self._buff = buff
    
    @property
    def items(self):
        return self._buff
    
    @property
    def unread(self):
        return self.items
    
    @property
    def is_changed(self):
        return [s.is_changed for s in self.sources]
    
    @is_changed.setter
    def is_changed(self, new):
        pass

class ImportantList(DynamicFeedObject):
    
    def __init__(self, sources=[]):
        self._title = 'Important'
        self.is_important = False
        DynamicFeedObject.__init__(self, sources)
    
    #def 
