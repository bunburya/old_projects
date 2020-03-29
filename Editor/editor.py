#! /usr/bin/python

'''Simple text editor program written in Python/Tk.'''

from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import askquestion
from os.path import isfile

# Define errors to be used.

class MenuCreationError(Exception):
    pass

class Editor(Frame):
    
    current_file = None
    
    def copy(self):
        all_text = self.text.get('1.0', 'end')
        if all_text != '\n':
            try:
                self.text.clipboard_append(self.text.selection_get())
                self.report('Selection copied to clipboard.')
            except TclError:
                ask = askquestion('Copy all?', 'No text selected.\nWould you like to copy all text?')
                if ask == 'yes':
                    self.text.clipboard_append(all_text)
                    self.report('All text copied to clipboard.')
        else:
            self.report('Nothing to copy.')
    
    def paste(self):
        try:
            self.text.insert(INSERT, self.text.selection_get(selection='CLIPBOARD'))
            self.report('Pasted selection from clipboard.')
        except TclError:
            self.report('Nothing to paste.')
    
    def newFile(self):
        self.current_file = None
        self.text.delete('1.0', 'end')
        
    
    def saveFirst(self, func):
        if self.text.edit_modified():
            if self.saveYN():
                self.saveFile()
        func()
    
    def saveYN(self):
        ask = askquestion('Save changes?', '\nWould you like to\nsave your changes?')
        if ask == 'yes':
            return True
        elif ask == 'no':
            return False
    
    def preOpen(self):
        if self.text.get('1.0', 'end') != '\n':
            if self.saveYN():
                self.saveFile()
        self.openFile()
            
    def report(self, text):
        self.status["text"] = text
            
    def importSource(self):
        import http.client
        path = self.path.get()
        if 'http://' in path:
            path = path[7:]
        if '/' in path:
            slash = path.find('/')
            host = path[:slash]
            url = path[slash:]
        else:
            host = path
            url = ''
        connect = http.client.HTTPConnection(host)
        connect.request('GET', url)
        response = connect.getresponse()
        if response.status == 200:
            text = response.read().decode('utf8')
            #for i in range(len(text)):
            self.text.insert('1.0', text)
            self.report(path+' loaded.')
            self.path.destroy()
            self.submit.destroy()
        else:
            self.report(path+' failed to load.')
        
    def openFile(self):
        path = askopenfilename()
        if not path:
            return
        filename = path.split('/')[-1]
        with open(path, mode='r') as f:
            text = f.readlines()
        self.text.delete('1.0', 'end')
        for i in range(len(text)):
            self.text.insert(str(i+1)+'.0', text[i])
        self.report(path+' opened.')
        self.text.edit_modified(False)
        self.current_file = path
        self.master.title(filename+' - Alan\'s Python Editor')
    
    def saveFile(self):
        self.saveAs(self.current_file)
    
    def saveAs(self, cwf=None):
        if cwf:
            path = cwf
        else:
            path = asksaveasfilename()
        if not path:
            return
        filename = path.split('/')[-1]
        with open(path, mode='w') as f:
            f.write(self.text.get('1.0', "end"))
        self.report(path+' saved.')
        self.text.edit_modified(False)
        self.current_file = path
        self.master.title(filename+' - Alan\'s Python Editor')
            
    def getSourcePage(self):
        self.path = Entry(self)
        self.path.grid(column=1, row=1, columnspan=2, sticky=W+N)
        self.submit = Button(self, text="Submit", command=self.importSource)
        self.submit.grid(column=3, row=1, sticky=W+N)
    
        
    def createWidgets(self):
        
        ## Configure rows and columns
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        for i in range(10):
            self.columnconfigure(i, weight=0)
        
        ## Create textbox
        self.height = 35
        self.width = 110
        self.text = Text(self, height=self.height, width=self.width, wrap=WORD, undo=True)
        self.text.grid(column=0, row=2, columnspan=self.width-1, rowspan=self.height-1, sticky=N+S+E+W)
        self.x_scroll = Scrollbar(self, orient=HORIZONTAL, command=self.text.xview)
        self.x_scroll.grid(column=0, row=self.height+1, columnspan=self.width-1, sticky=W+E)
        self.y_scroll = Scrollbar(self, orient=VERTICAL, command=self.text.yview)
        self.y_scroll.grid(column=self.width, row=2, rowspan=self.height-1, sticky=N+S)
        self.text.config(xscrollcommand=self.x_scroll.set, yscrollcommand=self.y_scroll.set)
        
        ## Create menus
        ###############
        ## To save typing and create a cleaner mechanism for adding and
        ## editing menu options, options are provided to the createMenu
        ## function which generates menus accordingly.
        
        ## createMenu take two arguments: option, and one of toplevel
        ## or parent.
        ##  The option argument is a tuple or list specifying the menu
        ##  options.
        ##  The toplevel argument is set to True if the menu is a
        ##  top level menu, ie if it is not a sub-menu of any other
        ##  menu. Otherwise, the menu is presumed to be a sub-menu.
        ##  The parent argument is provided if the menu is a sub-menu
        ##  and specifies the sub-menu's parent menu.
        
        ## An option tuple is a tuple of tuples. Each sub-tuple contains
        ## a variable number of elements depending on the object being
        ## created. Usually, the tuple will contain three elements.
        ##  0: The name of the option, and the text that will be
        ##    displayed for the option.
        ##  1: The option type; must be of a kind recognised by
        ##    Tkinter's Menu.add() method.
        ##  2: The command to be executed when the option is selected.
        ##    If the option being created is a cascade menu, the command
        ##    should be another option tuple which will be used to build
        ##    the sub-menu.
        ## If the option is a radiobutton, including a fourth element
        ## (of any kind or value) will select the option by default.
        ###############
        
        self.radio_ctrlvars = {}
        
        def createMenu(options, toplevel=False, parent=None):
            if toplevel:
                b_column, b_text = toplevel
                button = Menubutton(self, text=b_text)
                button.grid(column=b_column, row=1, columnspan=1, sticky=W+N+E)
                button.menu = Menu(button, tearoff=0)
                button["menu"] = button.menu
                my_menu = button.menu
            else:
                my_menu = parent
            
            for item in options:
                if item[1] == "cascade":
                    cascade = Menu(button, tearoff = 0)
                    createMenu(item[2], parent=cascade)
                    ##for submenu_item in item[2]:
                    ##    cascade.add(submenu_item[1], label=submenu_item[0], command=submenu_item[2])
                    my_menu.add_cascade(label=item[0], menu=cascade)
                    
                elif item[1] == "radiobutton":
                    try: group = item[3]
                    except IndexError: raise MenuCreationError('Radiobutton "%s" requires additional "group" argument.' % item[0])
                    if not group in self.radio_ctrlvars:
                        self.radio_ctrlvars[group] = StringVar()
                    my_menu.add_radiobutton(label=item[0], command=item[2], variable=self.radio_ctrlvars[group], value=item[0])
                    if len(item) > 4:
                        self.radio_ctrlvars[group].set(item[0])
                else:
                    my_menu.add(item[1], label=item[0], command=item[2])

        
        # File menu
        
        filemenu = (
                    ("New File", "command", lambda:self.saveFirst(self.newFile)),
                    ("Open", "command", lambda:self.saveFirst(self.openFile)),
                    ("Save", "command", self.saveFile),
                    ("Save as...", "command", self.saveAs),
                    ("Import page source", "command", self.getSourcePage),
                    ("Quit", "command", lambda:self.saveFirst(self.quit))
                )
        
        # Edit menu
        
        editmenu = ( 
                    ("Undo", "command", self.text.edit_undo),
                    ("Redo", "command", self.text.edit_redo),
                    ("Copy", "command", self.copy),
                    ("Paste", "command", self.paste)
                )

        # View menu
        
        # > Wrap submenu
        wrapmenu = (
                    ("Word", "radiobutton", lambda:self.text.config(wrap=WORD), "wrap", 1),
                    ("Character", "radiobutton", lambda:self.text.config(wrap=CHAR), "wrap"),
                    ("None", "radiobutton", lambda:self.text.config(wrap=NONE), "wrap")
                )
        
        viewmenu = (("Wrap", "cascade", wrapmenu),)
        
        ## ...
        
        menu_bar = (
                    ("File", filemenu),
                    ("Edit", editmenu),
                    ("View", viewmenu)
                )
                
        for i in range(len(menu_bar)):
            createMenu(menu_bar[i][1], (i, menu_bar[i][0]))
        
        ## Create statusbar
        self.status = Label(self, text="Hi.")
        self.status.grid(column=0, row=self.height+2, columnspan=self.width, sticky=W+S)
    
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.grid(sticky=N+E+S+W)
        self.createWidgets()

root = Tk()
root.title('Alan\'s Python Editor')
app = Editor(master=root)
app.mainloop()
root.destroy()
