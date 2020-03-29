#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import curses
import feedparser

from ui.interface import Interface
from feedreader.components.final import Feed, FeedList
from feedreader.components.dynamic import UnreadList
from feedreader.serialize.load import from_pkl

#fp_objs = from_pkl()
fp_objs = [feedparser.parse('http://feeds.feedburner.com/CeartaIE?format=xml')]

feed_objs = [Feed(f) for f in fp_objs]

# unread = UnreadList(feed_objs)    # for some reason this breaks everything
unread = UnreadList()
for b in feed_objs:
    unread.add_source(b)
unread.update_buffer()
feed_objs.append(unread)



feed_list = FeedList(feed_objs)

#feed_list = FeedList([Feed(b) for b in feeds])

def run(stdscr):
    ui = Interface(feed_list, stdscr)
    while True:
        ui.input()
        
curses.wrapper(run)

