#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Tue May 18 15:24:52 2010

import wx

#YYYYMMDD.HHMMSS of this release.
__version__ = 20100528
human_version = "2010-05-28"

# begin wxGlade: extracode
import pyBASIC
import threading
import time

thread_is_on = False
kill_thread = False
file_location = ""
debug_mode = False
input_queue = ""
    
OUTPUT_EVENT_ID = wx.NewId()
OPEN_ID = wx.NewId()
SAVE_AS_ID = wx.NewId()
SAVE_ID = wx.NewId()
RUN_ID = wx.NewId()
DEBUG_ID = wx.NewId()
ABOUT_ID = wx.NewId()
UPDATES_ID = wx.NewId()

class OutputEvent ( wx.PyEvent ):
    '''An event that handles output from the parser.'''
    def __init__(self, standard_output, error_output):
        wx.PyEvent.__init__(self)
        self.SetEventType(OUTPUT_EVENT_ID)
        self.stdout = standard_output
        self.stderr = error_output

def OUTPUT_EVENT(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, OUTPUT_EVENT_ID, func)

class BASICThread ( threading.Thread ):
    '''This thread runs the BASIC program and manages messages to and
    from it.'''
    def __init__(self, program_text, notify_window):
        self.program_text = program_text
        threading.Thread.__init__( self )
        self._notify_window = notify_window
        
    def stdout(self, text):
        '''Handles the stdout questioning for the thread.'''
        wx.PostEvent(self._notify_window, OutputEvent(text, ""))

    def stderr(self, text):
        '''Handles the stderr for the thread.'''
        wx.PostEvent(self._notify_window, OutputEvent("", text))
        
    def input(self, text):
        '''Handles input for the thread.'''
        global input_queue
        self.stdout(text)
        while input_queue == "":
            time.sleep(.1)
        iq = input_queue
        input_queue = ""
        return iq
    def kill( self ):
        '''Gives the thread a suicide mission.'''
        return kill_thread
        
    def run ( self ):
        import pyBASIC
        global program_text
        global thread_is_on, kill_thread
        thread_is_on = True
        
        #Replace handlers with our own.
        pyBASIC.parser.error_fx = self.stderr
        pyBASIC.runner.error_fx = self.stderr
        pyBASIC.runner.input_fx = self.input
        pyBASIC.runner.output_fx = self.stdout
        pyBASIC.runner.check_killed = self.kill
        
        pyBASIC.set_debug( debug_mode )
        
        print "Compileing"
        doc = pyBASIC.tokenize_document(self.program_text)
        print "Running"
        try:
            pyBASIC.run(doc)
        except:
            self.stderr("FATAL ERROR, Quitting")
            self.stdout("-------------\nABNORMAL EXIT")
        print "Quitting"
        kill_thread = False
        thread_is_on = False    
# end wxGlade



class main_frame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: main_frame.__init__
        kwds["style"] = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.MAXIMIZE_BOX|wx.SYSTEM_MENU|wx.RESIZE_BORDER|wx.TAB_TRAVERSAL|wx.CLIP_CHILDREN
        wx.Frame.__init__(self, *args, **kwds)
        self.window_1 = wx.SplitterWindow(self, -1, style=wx.SP_3D|wx.SP_BORDER)
        self.window_1_pane_2 = wx.Panel(self.window_1, -1)
        self.window_1_pane_1 = wx.Panel(self.window_1, -1)
        
        # Menu Bar
        self.frame_1_menubar = wx.MenuBar()
        self.file_menu = wx.Menu()
        self.open_document_item = wx.MenuItem(self.file_menu, OPEN_ID, "Open\tCtrl+o", "Opens an existing document.", wx.ITEM_NORMAL)
        self.file_menu.AppendItem(self.open_document_item)
        self.file_menu.AppendSeparator()
        self.save_document_item = wx.MenuItem(self.file_menu, SAVE_ID, "Save\tCtrl+s", "Saves the current document you are working on.", wx.ITEM_NORMAL)
        self.file_menu.AppendItem(self.save_document_item)
        self.save_document_as_item = wx.MenuItem(self.file_menu, SAVE_AS_ID, "Save As\tCtrl+Shift+s", "Saves the document you are working with in a new location.", wx.ITEM_NORMAL)
        self.file_menu.AppendItem(self.save_document_as_item)
        self.frame_1_menubar.Append(self.file_menu, "File")
        wxglade_tmp_menu = wx.Menu()
        self.run_document_item = wx.MenuItem(wxglade_tmp_menu, RUN_ID, "Run\tCtrl+r", "Runs the currently open document.", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.run_document_item)
        self.debug_button = wx.MenuItem(wxglade_tmp_menu, DEBUG_ID, "Debug\tCtrl+d", "Shows debug statments to help you figure out whats going wrong.", wx.ITEM_CHECK)
        wxglade_tmp_menu.AppendItem(self.debug_button)
        self.frame_1_menubar.Append(wxglade_tmp_menu, "Program")
        wxglade_tmp_menu = wx.Menu()
        self.about_button = wx.MenuItem(wxglade_tmp_menu, ABOUT_ID, "About", "About pyBASIC IDE", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.about_button)
        self.check_updates_menuitem = wx.MenuItem(wxglade_tmp_menu, UPDATES_ID, "Check For Updates", "Checks for updates.", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.check_updates_menuitem)
        self.frame_1_menubar.Append(wxglade_tmp_menu, "Help")
        self.SetMenuBar(self.frame_1_menubar)
        # Menu Bar end
        self.editor_text_ctrl = wx.TextCtrl(self.window_1_pane_1, -1, "PRINT \"Hello World\"", style=wx.TE_MULTILINE)
        self.output_text_ctrl = wx.TextCtrl(self.window_1_pane_2, -1, "", style=wx.TE_MULTILINE)
        self.input_text_ctrl = wx.TextCtrl(self.window_1_pane_2, -1, "")
        self.submit_button = wx.Button(self.window_1_pane_2, -1, "Submit")
        self.error_text_ctrl = wx.TextCtrl(self.window_1_pane_2, -1, "", style=wx.TE_MULTILINE)

        self.__set_properties()
        self.__do_layout()

        wx.EVT_MENU(self, OPEN_ID, self.open_document)
        wx.EVT_MENU(self, SAVE_ID, self.save_document)
        wx.EVT_MENU(self, SAVE_AS_ID, self.save_document_as)
        wx.EVT_MENU(self, RUN_ID, self.run_basic)
        wx.EVT_MENU(self, DEBUG_ID, self.debug_activate)
        wx.EVT_MENU(self, ABOUT_ID, self.about_program)
        wx.EVT_MENU(self, UPDATES_ID, self.check_updates)
        wx.EVT_BUTTON(self, self.submit_button.GetId(), self.submit_text)
        # end wxGlade
        # Set up event handler for any worker thread results
        OUTPUT_EVENT(self,self.OnOutput)
        #Bind the input control with the enter key
        self.input_text_ctrl.Bind(wx.EVT_KEY_DOWN, self.input_key_press)
        
    def input_key_press(self, event):
        '''
        Checks for the enter key, if it has been pressed then the program will
        submit the value that is in the pad input box
        '''
        keycode = event.GetKeyCode()
        #If user pressed enter or return spawn the submit input event
        if keycode == wx.WXK_RETURN or keycode == wx.WXK_NUMPAD_ENTER:
            self.submit_text(event)
        event.Skip()
        
    def OnOutput(self, event):
        '''Handles changing the display when an event is post.'''
        if event.stderr != "":
            self.error_text_ctrl.AppendText( str(event.stderr) + "\n")
        if event.stdout != "":
            if event.stdout.endswith("\n"):
                self.output_text_ctrl.AppendText( str(event.stdout))
            else:
                self.output_text_ctrl.AppendText( str(event.stdout) + "\n")
            
    def __set_properties(self):
        # begin wxGlade: main_frame.__set_properties
        self.SetTitle("pyBASIC - Integrated Development Enviornment")
        self.SetSize((700, 500))
        self.editor_text_ctrl.SetToolTipString("Write your code here.")
        self.output_text_ctrl.SetBackgroundColour(wx.Colour(0, 0, 0))
        self.output_text_ctrl.SetForegroundColour(wx.Colour(255, 255, 255))
        self.output_text_ctrl.SetToolTipString("Output will appear here")
        self.input_text_ctrl.SetToolTipString("Input your text here.")
        self.error_text_ctrl.SetForegroundColour(wx.Colour(255, 0, 0))
        self.error_text_ctrl.SetToolTipString("Errors will appear here")
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: main_frame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(self.editor_text_ctrl, 1, wx.ALL|wx.EXPAND, 4)
        self.window_1_pane_1.SetSizer(sizer_2)
        sizer_3.Add(self.output_text_ctrl, 2, wx.ALL|wx.EXPAND, 4)
        sizer_4.Add(self.input_text_ctrl, 1, wx.ALL, 4)
        sizer_4.Add(self.submit_button, 0, wx.ALL, 3)
        sizer_3.Add(sizer_4, 0, wx.EXPAND, 0)
        sizer_3.Add(self.error_text_ctrl, 1, wx.ALL|wx.EXPAND, 4)
        self.window_1_pane_2.SetSizer(sizer_3)
        self.window_1.SplitVertically(self.window_1_pane_1, self.window_1_pane_2)
        sizer_1.Add(self.window_1, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        self.Centre()
        self.SetSize((700, 500))
        # end wxGlade
        
    def submit_text(self, event): # wxGlade: main_frame.<event_handler>
        global input_queue
        input_queue = self.input_text_ctrl.GetValue() #Set even if 0
        if input_queue != "":
            self.output_text_ctrl.AppendText(">" + str(input_queue) + "\n")
        else:
            self.error_text_ctrl.AppendText( "INPUT ERROR: Please input some real text or a number.\n")
        self.input_text_ctrl.Clear()
        
        event.Skip()

    def open_document(self, event): # wxGlade: main_frame.<event_handler>
        import os
        global file_location
        dlg = wx.FileDialog(self, "Open a file", os.getcwd(), "", "BASIC Files (*.bas)|*.bas|All Files|*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            print "Opening at: %s" % (path)
            
            file = open(path, 'r')
            self.editor_text_ctrl.Clear()
            self.editor_text_ctrl.AppendText( file.read() )
            file.close()
            file_location = path
        dlg.Destroy()

    def save_document(self, event, quiet=False): # wxGlade: main_frame.<event_handler>
        global file_location
        if file_location == "":
            import os
            dlg = wx.FileDialog(self, "Save a file", os.getcwd(), "", "BASIC Files (*.bas)|*.bas|All Files|*.*", wx.SAVE)
            if dlg.ShowModal() == wx.ID_OK:
                file_location = dlg.GetPath()
                if dlg.GetFilterIndex() == 0 and not file_location.endswith(".bas"):
                    file_location = file_location+".bas"
            dlg.Destroy()
            
        print "Saving at: %s" % (file_location)
        
        file = open(file_location, 'w')
        file.write(self.editor_text_ctrl.GetValue())
        file.close()
        
        event.Skip()
        
    def run_basic(self, event): # wxGlade: main_frame.<event_handler>
        '''Run the BASIC program the user has.'''
        global kill_thread
        global thread_is_on
        
        if thread_is_on:
            '''If thread is running'''
            print "Thread is on"
            kill_thread = True
            time.sleep(1)
            
        print "Starting another thread..."
        #Clear the inputs
        self.input_text_ctrl.Clear()
        self.error_text_ctrl.Clear()
        self.output_text_ctrl.Clear()
        

        program_text = self.editor_text_ctrl.GetValue()
        
        compiler_thread = BASICThread( program_text, self )
        compiler_thread.start()
        
        #event.skip()

    def about_program(self, event): # wxGlade: main_frame.<event_handler>
        description = """pyBASIC IDE is a cross between TIBASIC, and CLASSIC BASIC, allowing new programmers to experience the excitement of the classical home programming language.\n\n Special thanks to Jill Carlson."""
        licence = """pyBASIC is free software; you can redistribute it and/or modify it 
under the terms of the GNU General Public License as published by the Free Software Foundation; 
either version 3 of the License, or (at your option) any later version.

Ubuntu Remote is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
See the GNU General Public License for more details. You should have received a copy of 
the GNU General Public License along with Ubuntu Remote; if not, write to 
the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA"""

        info = wx.AboutDialogInfo()
        
        info.SetName( 'pyBASIC IDE' )
        info.SetVersion( human_version )
        info.SetDescription( description )
        info.SetCopyright( '© 2010 Joseph Lewis <joehms22@gmail.com>' )
        info.SetWebSite( 'http://code.google.com/p/pybasic/' )
        info.SetLicence( licence )
        info.AddDeveloper( 'Joseph Lewis <joehms22@gmail.com>' )
        
        wx.AboutBox(info)
        
            
    def save_document_as(self, event): # wxGlade: main_frame.<event_handler>
        global file_location
        file_location = ""
        self.save_document(event)
        
    def debug_activate(self, event): # wxGlade: main_frame.<event_handler>
        global debug_mode 
        debug_mode = not debug_mode
        print debug_mode
        
    def check_updates(self, event, silent=False): # wxGlade: main_frame.<event_handler>
        print "Checking for updates please wait..."
        import urllib
        import webbrowser
        
        try:
            version_on_site = urllib.urlopen("http://pybasic.googlecode.com/svn/trunk/current_version.txt").read()
            
            print "Version On Site: " + str(float(version_on_site)) + " This Version " + str(__version__)

            if float(version_on_site) > __version__:
                dial = wx.MessageDialog(None, 'Updates Avalable!\nhttp://code.google.com/p/pybasic/', 'Info', wx.OK)
                dial.ShowModal()
                webbrowser.open("http://code.google.com/p/pybasic")
            elif silent == False:
                dial = wx.MessageDialog(None, 'You are up to date!', 'Info', wx.OK)
                dial.ShowModal()
            elif float(version_on_site) < __version__:
                dial = wx.MessageDialog(None, 'You are using BETA, Thanks!', 'Info', wx.OK)
                dial.ShowModal()

        except:
            if silent == False:
                dial = wx.MessageDialog(None, 'Unable to reach server.', 'Info', wx.OK)
                dial.ShowModal()

# end of class main_frame

def startup():
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = main_frame(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    frame_1.check_updates("", silent=True)
    app.MainLoop()

if __name__ == "__main__":
    startup()
