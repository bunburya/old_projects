from feedreader.components.base import BaseListObject
from feedreader.components.final import Feed


class DynamicFeedObject(Feed):
    """A feed-like object whose contents change regularly. This will be
    used to implement Important, Unread etc."""
    
    is_dynamic = True
    
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

# Below not workable

class ImportantList(DynamicFeedObject):
    
    def __init__(self, sources=[]):
        self._title = 'Important'
        self.is_important = False
        DynamicFeedObject.__init__(self, sources)
    
    #def 
