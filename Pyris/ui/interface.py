"""TODO:
- Maximise
"""

import curses
from _curses import error as CursesError
from signal import alarm, SIGALRM, signal

from ui.panes import EntryViewPane, FeedListPane, FeedViewPane

import locale
locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

class Interface:
    
    # Special keys
    #RESIZE = chr(18)    #Ctrl-r
    #IMPORTANT = chr(9)  #Ctrl-i
    
    resize_keys = {'h': 'left', 'j': 'down', 'k': 'up', 'l': 'right'}
    focus_keys = {  '\t': 'clockwise', '\n': 'clockwise',
                    'Z': 'counter', '\x7F': 'counter'}
    scroll_keys = {'j': 'down', 'k': 'up'}
    modes = {'normal', 'resize', 'config', 'monocle'}
        #TODO: implement config, monocle
    
    def __init__(self, feed_list, stdscr):
        self.feed_list = feed_list
        self.stdscr = stdscr
        stdscr.refresh()
        curses.start_color()
        assert curses.has_colors()
        max_y, max_x = stdscr.getmaxyx()
        self.max_y, self.max_x = max_y, max_x
        
        # Determine the height of our panes.
        # Vertical values are reduced by 1 to account for the status bar
        feed_list_x = max_x // 5            # width of the feed list pane
        feed_list_y = max_y - 1             # height of the feed list pane
        rest_x = max_x - feed_list_x        # width of the rest of the screen
        feed_view_y = (max_y // 4) - 1      # height of the feed view pane
        entry_y = max_y - feed_view_y -1    # height of the rest of the screen
                
        self.entry_pane = EntryViewPane(feed_view_y, feed_list_x,
                                    entry_y, rest_x, max_y, max_x, self)
        self.feed_pane = FeedViewPane(0, feed_list_x, feed_view_y,
                                    rest_x, max_y, max_x, self)
        self.list_pane = FeedListPane(0, 0, feed_list_y, feed_list_x, max_y,
                                    max_x, self)
        self.next_clock = { self.list_pane: self.feed_pane,
                            self.feed_pane: self.entry_pane,
                            self.entry_pane: self.list_pane }
        self.next_counter = {   self.list_pane: self.entry_pane,
                                self.entry_pane: self.feed_pane,
                                self.feed_pane: self.list_pane  }
        self.mode = 'normal'
        self.focused = None
        self.focus(self.list_pane)
        self.resize_funcs = {'up': self.resize_up, 'down': self.resize_down,
                        'left': self.resize_left, 'right': self.resize_right}
        self.list_pane.display(feed_list)
        #self.list_pane.print_sel()
        #self.list_pane.print_all()
        self.list_pane.print_changed()
        self.write_status()
        #while True:
        #    self.input()
    
    def focus(self, pane):
        #if (self.focused is None) or (pane == self.focused):
        #    return
        if self.mode == 'monocle':
            if self.focused is not None:
                self.focused.minimise()
            self.focused = pane
            pane.maximise(self.max_y, self.max_x)
        else:
            if self.focused is not None:
                self.focused.toggle_border(False)
            pane.toggle_border(True)
            self.focused = pane
    
    def select_move(self, key):
        """For scrolling though lists."""
        if key == 'up':
            self.focused.select_prev()
        elif key == 'down':
            self.focused.select_next()
        self.list_pane.print_changed()
    
    def scroll_move(self, key):
        """For scrolling through an actual feed entry."""
        if key == 'up':
            self.focused.scroll_up()
        elif key == 'down':
            self.focused.scroll_down()
    
    def next_pane(self, direction):
        if direction == 'clockwise':
            return self.next_clock[self.focused]
        elif direction == 'counter':
            return self.next_counter[self.focused]
    
    def input(self):
        try:
            key = self.stdscr.getkey(0, 0)
        except CursesError:
            key = ''
        
        #while key == -1:
        #    key = self.stdscr.getkey(0, 0)
        
        if key == ' ':
            self.report('testing', 5)
        
        if key == 'u':
            self.update_all()
        
        if key == 'q':
            self.quit()
        
        if key == 'r':
            if self.mode == 'resize':
                self.leave_resize()
            else:
                self.enter_resize()
        
        if key == 'm':
            if self.mode == 'monocle':
                self.leave_monocle()
            else:
                self.enter_monocle()

        if self.mode in {'normal', 'monocle'}:
            if key in self.scroll_keys:
                if self.focused == self.entry_pane:
                    self.scroll_move(self.scroll_keys[key])
                else:
                    self.select_move(self.scroll_keys[key])
            
            if key in self.focus_keys:
                self.focus(self.next_pane(self.focus_keys[key]))

        # Catching exceptions doesn't work because by the time the
        # exception is raised, the size has already been changed.
        if self.mode == 'resize':
            if key in self.resize_keys:
                self.resize_funcs[self.resize_keys[key]]()
        curses.doupdate()
    
    def toggle_all(self, new):
        self.feed_pane.toggle_border(new)
        self.entry_pane.toggle_border(new)
        self.list_pane.toggle_border(new)
    
    def update_feed(self, feed):
        title = feed.title_only
        self.report('Updating {}'.format(title))
        feed.update()
        self.report('{} updated.'.format(title), 5)
    
    def update_all(self):
        for feed in self.feed_list:
            if not feed.is_dynamic:
                self.update_feed(feed)
        self.report('All feeds updated.', 5)
    
    def quit(self):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()
        quit()
    
    
    # Resize mode methods
    
    def enter_resize(self):
        self.toggle_all(True)
        self.mode = 'resize'
    
    def leave_resize(self):
        self.toggle_all(False)
        self.focused.toggle_border(True)
        self.mode = 'normal'
    
    def all_can_extend(self, plane, *windows):
        for w in windows:
            if not w.can_extend(plane):
                return False
        return True
    
    def resize_up(self):
        if (self.feed_pane.can_shrink('y') and self.entry_pane.can_extend('y')):
            self.feed_pane.shrink_up()
            self.entry_pane.extend_up()
    def resize_down(self):
        if self.feed_pane.can_extend('y') and self.entry_pane.can_shrink('y'):
            self.feed_pane.extend_down()
            self.entry_pane.shrink_down()
    def resize_left(self):
        if self.list_pane.can_shrink('x') and self.feed_pane.can_extend('x') and self.entry_pane.can_extend('x'):
            self.list_pane.shrink_right()
            self.feed_pane.extend_left()
            self.entry_pane.extend_left()
    def resize_right(self):
        if self.list_pane.can_extend('x') and self.feed_pane.can_shrink('x') and self.entry_pane.can_shrink('x'):
            self.list_pane.extend_right()
            self.feed_pane.shrink_left()
            self.entry_pane.shrink_left()
    
    # Monocle mode methods
    
    def enter_monocle(self):
        self.stdscr.clear()
        self.next_clock[self.focused].minimise()
        self.next_counter[self.focused].minimise()
        self.focused.maximise(self.max_y-1, self.max_x-1)
        self.mode = 'monocle'
        
    def leave_monocle(self):
        self.focused.unmaximise()
        self.next_clock[self.focused].unminimise()
        self.next_counter[self.focused].unminimise()
        self.mode = 'normal'

    # Prompting and reporting
    
    def write_status(self, text=None):
        """Writes text to the statusbar, which is the last line on the screen.
        Called with no arguments, resets the status to default.
        """
        if text is None:
            text = self.default_status
        self.stdscr.addstr(self.max_y-1, 0, text)
        self.stdscr.clrtoeol()
        # we need to refresh to screen as it happens.
        self.stdscr.refresh()
    
    def on_alarm(self, signum, frame):
        self.write_status()
    
    def report(self, msg, timeout=0):
        """Write msg to the status bar, and leave it there for timeout
        seconds. timeout defaults to 0. If timeout is 0, the status is
        left there indefinitely.
        """
        self.write_status(msg)
        if timeout:
            signal(SIGALRM, self.on_alarm)
            alarm(timeout)
    
    def prompt(self, msg):
        self.report(msg)
        response = self.stdscr.getstr(self.max_y-1, len(msg)+1)
        return response.decode(code)
    
    @property
    def default_status(self):
        return '{} feeds, {} entries.'.format(self.feed_list.feed_count,
                                              self.feed_list.entry_count)
