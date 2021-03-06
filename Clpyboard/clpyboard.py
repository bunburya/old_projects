#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#       clpyboard.py
#       
#       Copyright 2010 Alan Bunbury <bunburya@tcd.ie>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

"""Clpyboard is a simple application that stores data you copy to the
clipboard and allows you to select it for pasting later on."""

from sys import argv
from os.path import dirname, join, isfile
from pickle import dump, load
import wx

class Main(wx.Frame):
    """The main class for clpyboard."""
    
    pwd = dirname(argv[0])
    save_file = join(pwd, 'saved')
    
    def __init__(self):
        wx.Frame.__init__(self, None)
        self.icon = SystrayIcon(self, self.pwd)
        self.old_data = []
        self.data_count = 0
        self.funcs = {}
        self.create_menu()
        self.icon.Bind(wx.EVT_TASKBAR_LEFT_UP, self.on_click)
        if isfile(self.save_file):
            self.load_data()
        self.start_daemon()
    
    def show_menu(self, event):
        """Show the main menu."""
        self.PopupMenu(self.menu)
    
    def create_menu(self):
        """Create the main menu and append options."""
        self.menu = wx.Menu()
        self.menu.AppendSeparator()
        self.menu.Append(-5, "Clear")
        self.icon.Bind(wx.EVT_MENU, self.clear, id=-5)
        self.menu.Append(-10, "Quit")
        self.icon.Bind(wx.EVT_MENU, self.quit_app, id=-10)

    def check_cb(self, event):
        """Checks the clipboard to see if new content has been added."""
        if wx.TheClipboard.Open():
            data = wx.TextDataObject()
            success = wx.TheClipboard.GetData(data)
            wx.TheClipboard.Close()
            if success:
                data = data.GetText()
                if data not in self.old_data:
                    self.store(data)
    
    def store(self, data):
        """Called if new data is detected. Stores the data in memory and
        adds a corresponding option to the menu."""
        label = data
        label = label.replace('\n', ' ')
        if len(label) > 20:
            label = label[:17]+'...'
        self.old_data.append(data)
        self.funcs[self.data_count] = self.on_select()
        self.menu.InsertRadioItem(0, self.data_count, label)
        self.menu.Check(self.data_count, True)
        self.icon.Bind(wx.EVT_MENU, self.funcs[self.data_count],
                        id=self.data_count)
        self.data_count += 1
        
    
    def on_select(self):
        """Generates and returns a function that will be executed when
        the relevant option is selected in the menu."""
        dc = self.data_count
        def to_cb_relevant(event):
            self.to_cb(self.old_data[dc])
            self.menu.Check(dc, True)
        return to_cb_relevant
    
    def to_cb(self, data):
        """Replaces the current clipboard contents with the
        selected data."""
        if wx.TheClipboard.Open():
            wx.TheClipboard.Clear()
            wx.TheClipboard.SetData(wx.TextDataObject(data))
            wx.TheClipboard.Close()
    
    def on_click(self, event):
        """Pop up the menu when the systray icon is clicked."""
        self.icon.PopupMenu(self.menu)
    
    def clear(self, event):
        """Clear all stored data from memory."""
        for i in range(self.data_count):
            self.menu.Delete(i)
        self.funcs = {}
        self.old_data = []
        self.data_count = 0
    
    def start_daemon(self, t=1000):
        """Start the daemon, which will check the clipboard for new
        content every t/1000 seconds."""
        self.timer = wx.Timer(self, t)
        self.Bind(wx.EVT_TIMER, self.check_cb, self.timer)
        self.timer.Start(t)
    
    def save_data(self):
        with open(self.save_file, 'wb') as f:
            dump(self.old_data, f)
    
    def load_data(self):
        with open(self.save_file, 'rb') as f:
            for line in load(f):
                self.store(line)
    
    def quit_app(self, event):
        self.save_data()
        quit()


class SystrayIcon(wx.TaskBarIcon):
    def __init__(self, frame, pwd):
        wx.TaskBarIcon.__init__(self)
        self.frame = frame
        icon_path = join(pwd, 'clpyboard_icon.gif')
        self.SetIcon(wx.Icon(icon_path, wx.BITMAP_TYPE_GIF),'Clpyboard')
        
if __name__ == '__main__':
    app = wx.App(False)
    window = Main()
    app.MainLoop()
