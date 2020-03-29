"""TODO:
- Finish BaseObject class; it should hold data and methods common to all objects.
- Re-implement mark as read on select.
    - Use on_select and on_deselect.
    - UnreadList must mark as read only on deselect, or else it must repopulate less often
      than on every select.
- Sorting mechanisms, at least by time.
"""

class BaseObject:
    
    is_dynamic = False
    
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
        try:
            return max(len(i.title) for i in self.items)
        except ValueError:
            return 0
    
