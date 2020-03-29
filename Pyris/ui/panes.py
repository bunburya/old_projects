import curses
from textwrap import wrap
from feedreader.htmlhandler import HTMLHandler
from feedreader.components.final import FeedEntry

"""TODO: Make the whole thing more clean, maybe move more stuff to Interface level.

Monocle is almost implemented, but scrolling while in monocle should not mark read.
- Giving up on it for now, consider completing at later date or removing."""

class Pane:
    
    def __init__(self, start_y, start_x, win_h, win_w, pad_h, pad_w, ui):
        
        self.border_status = False
        self.is_maximised = False
        self.is_minimised = False
        self.ui = ui
        
        # Setting win_hs and win_ws
        self.start_y = start_y
        self.start_x = start_x
        self.pad_h = pad_h
        self.pad_w = pad_w
        self.win_h = win_h
        self.win_w = win_w
        self.max_y = ui.max_y
        self.max_x = ui.max_x
        
        self.min_resize_h = 3   # 1 row/col + 2 for borders
        self.min_resize_w = 3   # "
        self.max_resize_h = self.max_y #- 1#self.min_resize_h
        self.max_resize_w = self.max_x #- 1#self.min_resize_w
        
        self.scroll_y = 0
        self.pad = curses.newpad(self.pad_h, self.pad_w)
        
        self.ext_tests = {
                    'x':    lambda: self.win_w < self.max_resize_w,
                    'y':    lambda: self.win_h < self.max_resize_h
                    }
        self.shr_tests = {
                    'x':    lambda: self.win_w > self.min_resize_w,
                    'y':    lambda: self.win_h > self.min_resize_h
                    }

        self.draw()
    
    def toggle_border(self, on_off):
        if on_off:
            self.border.border()
            self.border_status = True
        else:
            self.border.erase()
            self.border_status = False
        self.border.noutrefresh()
        self.refresh()
        
    
    def draw(self):
        self.border = curses.newwin(self.win_h, self.win_w,
                                    self.start_y, self.start_x)
        if self.border_status:
            self.border.border()
        self.border.noutrefresh()
        self.refresh()
    
    def refresh(self):
        
        self.pad.noutrefresh(self.scroll_y, 0, self.start_y+1,
                            self.start_x+1, self.start_y+self.win_h-2,
                            self.start_x+self.win_w-2)
    
    # draw() in the below methods is what raises the error when you try
    # to resize too far.
    
    def can_extend(self, plane):
        return self.ext_tests[plane]()
    
    def can_shrink(self, plane):
        return self.shr_tests[plane]()
    
    def extend_left(self):
        self.start_x -= 1
        self.win_w += 1
        self.draw()
    
    def extend_right(self):
        self.win_w += 1
        self.draw()
    
    def extend_up(self):
        self.start_y -= 1
        self.win_h += 1
        self.draw()
    
    def extend_down(self):
        self.win_h += 1
        self.draw()
    
    def shrink_left(self):
        self.start_x += 1
        self.win_w -= 1
        self.draw()
    
    def shrink_right(self):
        self.win_w -= 1
        self.draw()
    
    def shrink_up(self):
        self.win_h -= 1
        self.draw()
    
    def shrink_down(self):
        self.start_y += 1
        self.win_h -= 1
        self.draw()
    
    # Scrolling methods
    
    def scroll_down(self):
        if self.scroll_y + self.win_h < self.length + 2:
            self.scroll_y += 1
            self.refresh()
    
    def scroll_up(self):
        if self.scroll_y > 0:
            self.scroll_y -= 1
            self.refresh()
    
    # Monocle-related methods
        
    def maximise(self, max_y, max_x):
        self.is_maximised = True
        self.is_minimised = False
        self.old_size = (self.start_y, self.start_x,
                             self.win_h, self.win_w)
        self.start_y = 0
        self.start_x = 0
        self.win_h = max_y
        self.win_w = max_x
        self.refresh()
    
    def unmaximise(self):
        self.is_maximised = False
        self.start_y, self.start_x, self.win_h, self.win_w = self.old_size
        self.refresh()
    
    def minimise(self):
        self.is_minimised = True
        self.is_maximised = False
        self.old_size = (self.start_y, self.start_x,
                             self.win_h, self.win_w)

        self.start_y = -1   # This should have the effect of hiding
        self.start_x = -1   # the window
        self.win_h = 3      #
        self.win_w = 3      #
        
        self.refresh()
    
    def unminimise(self):
        self.is_minimised = True
        self.start_y, self.start_x, self.win_h, self.win_w = self.old_size
        self.refresh()

class ListPane(Pane):
    
    #def __init__(self, start_y, start_x, win_h, win_w, pad_h, pad_w):
    #    Pane.__init__(self, start_y, start_x, win_h, win_w, pad_h, pad_w)
        
    def add(self, item):
        posn = item.posn
        title = item.title[:self.pad_w-1]
        self.pad.addstr(posn, 0, title)
    
    def print_item(self, item):
        """Print the title of the item, applying any necessary attributes."""
        #TODO: Clean this up
        self.pad.addstr(item.posns[self.list_obj], 0, ' '*(self.pad_w-1))
        text = item.title[:self.pad_w-1]
        if self.list_obj in item.is_selected:
            # item is selected for purposes of this pane.
            if not item.is_read:
                attr = curses.A_STANDOUT | curses.A_BOLD
            else:
                attr = curses.A_STANDOUT
        elif item.is_important:
            attr = curses.A_UNDERLINE   # this will be changed, maybe
        elif not item.is_read:
            attr = curses.A_BOLD
        else:
            attr = None
        
        if attr is None:
            self.pad.addstr(item.posns[self.list_obj], 0, text)
        else:
            self.pad.addstr(item.posns[self.list_obj], 0, text, attr)
        self.refresh()
    
    def print_sel(self):
        self.print_item(self.list_obj.selected)
    
    def print_changed(self):
        for item in self.list_obj:
            if item.is_changed:
                self.print_item(item)
    
    def print_all(self):
        for i in self.list_obj:
            self.print_item(i)
    
    def select(self, item):
        to_desel = self.list_obj.selected
        self.list_obj.select_item(item)
        if not (to_desel is None):
            self.print_item(to_desel)
        self.print_item(item)
        self.on_select(item)
    
    def select_next(self):
        to_desel = self.list_obj.selected
        self.list_obj.select_next()
        if self.list_obj.sel_posn >= self.scroll_y + self.win_h-2:
            self.scroll_down()
        self.print_item(to_desel)
        self.print_item(self.list_obj.selected)
        self.on_select(self.list_obj.selected)
            
    def select_prev(self):
        to_desel = self.list_obj.selected
        self.list_obj.select_prev()
        if self.list_obj.sel_posn < self.scroll_y:
            self.scroll_up()
        self.print_item(to_desel)
        self.print_sel()
        self.on_select(self.list_obj.selected)
    
    def on_select(self, item):
        """This is to be overridden by sub-classes"""
        pass
    
    def display(self, list_obj):
        # This currently tries to handle both empty and non-empty list
        # objects, but doesn't do it very well. Maybe handle empty objects
        # elsewhere, and only handle non-empty objects here.
        self.list_obj = list_obj
        self.length = len(list_obj)
        try:
            max_len = max(len(i.title) for i in list_obj)
        except ValueError:
            max_len = 0
        too_small = False
        if max_len > 0:     # if list_obj is not empty
            if self.length > self.pad_h:
                self.pad_h = self.length
                too_small = True
            if self.list_obj.max_len > self.pad_w:
                self.pad_w = self.list_obj.max_len
                too_small = True
            if too_small:
                self.pad = curses.newpad(self.pad_h, self.pad_w)
            else:
                self.pad.erase()
            self.scroll_y = 0
        
            for item in list_obj:
                #self.add(item)
                self.print_item(item)
            self.select(list_obj.items[0])
        else:               # if list_obj is empty
            self.pad.erase()
            self.refresh()
        

class FeedListPane(ListPane):
    
    def __init__(self, start_y, start_x, win_h, win_w, pad_h, pad_w, ui):
        self.feed_pane = ui.feed_pane
        ListPane.__init__(self, start_y, start_x, win_h, win_w, pad_h, pad_w, ui)
    
    def on_select(self, item):
        self.feed_pane.display(item)

class FeedViewPane(ListPane):
    
    def __init__(self, start_y, start_x, win_h, win_w, pad_h, pad_w, ui):
        self.entry_pane = ui.entry_pane
        ListPane.__init__(self, start_y, start_x, win_h, win_w, pad_h, pad_w, ui)
    
    def on_select(self, item):
        self.entry_pane.display(item)

class EntryViewPane(Pane):
    
    def display(self, entry):
        self.scroll_y = 0
        self.entry = entry
        text = entry.text
        lines = text.split('\n\n')
        formatted = []
        text_w = self.max_x if self.is_minimised else self.win_w-2
        for line in lines:
            formatted += wrap(line, text_w)
            formatted += ['']
        length = len(formatted)
        self.length = length
        if length > self.pad_h:
            self.pad_h = length
            self.pad = curses.newpad(self.pad_h, self.pad_w)
        else:
            self.pad.erase()
        for pos, line in enumerate(formatted):
            self.pad.addstr(pos, 0, line)
        self.refresh()
    
