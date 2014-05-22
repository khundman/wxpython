#Testing a commit
#Commit code to github: git push origin master (after first one, can just typw git push)

#To Do's
#Multiple circles - redraw based on BN.parent.length

import wx
import os
import BayesianNetwork as BN
import functools
import datetime


#Frame - can't figure out how to change initial size
class BNGUI(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(BNGUI,self).__init__(*args,**kwargs)
        self.InitUI()
        self.SetBackgroundColour("white")

    def InitUI(self):
        menubar = wx.MenuBar()
        
        #File Menubar
        fileMenu = wx.Menu()
        fileMenu.Append(wx.ID_NEW, '&New')
        menuOpen = fileMenu.Append(wx.ID_OPEN, '&Open')
        fileMenu.Append(wx.ID_SAVE, '&Save')
        fileMenu.AppendSeparator()
        
        qmi = wx.MenuItem(fileMenu, wx.ID_EXIT, '&Quit\tCtrl+W')
        fileMenu.Append(qmi)
        
        self.Bind(wx.EVT_MENU, self.OnQuit, qmi)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        menuSave = fileMenu.Append(wx.ID_SAVE, '&Save')
        fileMenu.AppendSeparator()
        
        qmi = fileMenu.Append(wx.ID_EXIT, '&Quit\tCtrl+W')
        
        self.Bind(wx.EVT_MENU, self.OnQuit, qmi)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnSave, menuSave)

        menubar.Append(fileMenu, '&File')
        
        #View Menubar
        viewMenu = wx.Menu()
        self.shnw = viewMenu.Append(wx.ID_ANY, 'Show Network', 
            'Show Statusbar', kind=wx.ITEM_CHECK)
        
        viewMenu.Check(self.shnw.GetId(), True)
        
        self.Bind(wx.EVT_MENU, self.ToggleStatusBar, self.shnw)
        
        menubar.Append(viewMenu, '&View')
        self.SetMenuBar(menubar)

        #self.Panel = DrawPanel() #call DrawPanel class
        self.Fit()
        
        self.toolbar = self.CreateToolBar()
        self.toolbar.Realize()

        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText('Ready')

        self.SetSize((900, 700))
        self.SetTitle('Bayesian Network')
        self.Centre()
        self.Show(True)
        
    def ToggleStatusBar(self, e):
        if self.shnw.IsChecked():
            self.statusbar.Show()
        else:
            self.statusbar.Hide()

    def OnQuit(self, e):
        self.Close()

    def OnOpen(self,e):
        '''Load in existing JSON file - This works currently'''
        dlg = wx.FileDialog(self, "Choose a file", style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFilename()
            dirname = dlg.GetDirectory()
            f= dirname + '/' + filename
            BN.load(f) #Load and parse network from properly-formatted JSON file
        dlg.Destroy()
        
    def OnSave(self,event):
        # Save away the edited text
        # Open the file, do an RU sure check for an overwrite!
        dlg = wx.FileDialog(self, "Save JSON file", "", "",
                                   "JSON files (*.json)|*.json", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            # Open the file for write, write, close
            filename=dlg.GetFilename()
            dirname=dlg.GetDirectory()
            f= dirname + '/' + filename
            BN.save(f)
        # Get rid of the dialog to keep things tidy
        dlg.Destroy()

class panel_one (wx.Panel):

    def __init__( self, parent ):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, style = wx.TAB_TRAVERSAL )

        #self.Layout()
        #self.InitBuffer() 
        #self.Buffer = None 
        
        self.SetSize((900, 200))

        # View Properties button
        ViewPropBtn = wx.Button(self, label="View Properties", pos = (100,0))
        ViewPropBtn.Bind(wx.EVT_BUTTON, self.ChooseNodeToView)

        # Set Evidence button
        EvidenceBtn = wx.Button(self, label="Set Evidence", pos = (0,0))
        EvidenceBtn.Bind(wx.EVT_BUTTON, self.ChooseEvidenceNode)

        Sizer = wx.BoxSizer(wx.HORIZONTAL)
        Sizer.Add(ViewPropBtn, 0, wx.ALIGN_LEFT|wx.ALL, 5)
        #Sizer.Add(EvidenceBtn, 0, wx.ALIGN_LEFT|wx.ALL, 5)
        Sizer.Add(self, 0, wx.EXPAND)
        #Sizer.SetSizeHints(self)
        self.SetSizer(Sizer)
        
        self.SetBackgroundColour("gray")


    def InitBuffer(self):
        '''Setup canvas for circle drawing''' 
        size=self.GetClientSize() 
        self.Buffer = wx.EmptyBitmap(size.width, size.height) 
        self.dc = wx.MemoryDC() 
        self.dc.SelectObject(self.Buffer) 

    def ChooseNodeToView(self, e):
        #Choices
        size=self.GetClientSize() 
        sampleList = BN.nodesSave
        text0 = wx.StaticText(self, -1, "Please select node to view:", style = wx.ALIGN_CENTER)
        text0.CenterOnParent()
        self.ch = wx.Choice(self, -1, (120, 120), choices = sampleList)
        self.Bind(wx.EVT_CHOICE, self.ViewNode, self.ch)


    def ViewNode(self, event):
        #self.Refresh
        # Button to erase properties and redraw everything else
        ExitPropBtn = wx.Button(self, label="Return to Home")
        ExitPropBtn.Bind(wx.EVT_BUTTON, self.Refresh)

        Sizer = wx.BoxSizer(wx.VERTICAL)
        Sizer.Add(ExitPropBtn, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        self.SetSizerAndFit(Sizer)

        node = event.GetString() #this gets the value selected from the dropdown
        #List Control
        id=wx.NewId()
        prop=wx.ListCtrl(self,id, size=(700,600), style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        Sizer.Add(prop, 0, wx.ALIGN_LEFT|wx.ALL, 5)
        self.SetSizerAndFit(Sizer)
        prop.Show(True)

        bnIndex = BN.nodesSave.index(node)
        prop.InsertColumn(0,'Parent',width = 60)
        prop.InsertColumn(1,'States', width = 120)
        prop.InsertColumn(2,'CPT', width = 500)

        # 0 will insert at the start of the list
        pos = prop.InsertStringItem(0,str(BN.parentsSave[bnIndex]))
        # add values in the other columns on the same row
        prop.SetStringItem(pos,1,str(BN.statesSave[bnIndex]))
        prop.SetStringItem(pos,2,str(BN.cptsSave[bnIndex]))
        #text0.Destroy()

    def Refresh(self, event):
        self.Destroy()
        main()

    def ChooseEvidenceNode(self, event):
        #Choices
        #self.Refresh
        nodeList = BN.nodesSave
        text = wx.StaticText(self, -1, "Please select node to set evidence on:", (238, 100))
        self.ch = wx.Choice(self, -1, (250, 120), choices = nodeList)
        self.Bind(wx.EVT_CHOICE, self.ChooseEvidenceState, self.ch)
        #text.Destroy()

    def ChooseEvidenceState(self, event):
        #self.Refresh
        evidenceNode = event.GetString()
        evidenceHolder.append(evidenceNode)
        stateList = BN.statesSave[BN.nodesSave.index(evidenceNode)]
        text2 = wx.StaticText(self, -1, "Please select state for evidence:", (238, 200))
        self.ch2 = wx.Choice(self, -1, (250, 220), choices = stateList)
        self.Bind(wx.EVT_CHOICE, self.SetEvidence, self.ch2)
        #text.Destroy()    

    def SetEvidence(self, event):
        state = event.GetString()
        statePosition = BN.statesSave[BN.nodesSave.index(evidenceHolder[0])].index(state)
        BN.evidenceList.append({evidenceHolder[0]:statePosition})
        del evidenceHolder[:]

    def __del__( self ):
        pass

def getInputs(parent = None):
    '''Get inputs needed to create node and add to inputs to global lists in BN'''
    #Input name
    dlg = wx.TextEntryDialog(parent, 'Please enter name of node: ')
    dlg.ShowModal()
    BN.nodesSave.append(dlg.GetValue)

    #Input parents - CHANGE -> ask for number of parents and have new window pop up for each
    dlg.Destroy()
    dlg2 = wx.TextEntryDialog(parent, 'Please enter names of parents: ')
    dlg2.ShowModal()
    BN.parentsSave.append(dlg2.GetValue)
    dlg2.Destroy()

    #Input States - same as parents (ask for number first)
    #Input cpts (ideally grab parent states and create table to allow user to enter)
 
def Refresh():
    main()   

def main():
    bn = wx.App()
    g = BNGUI(None)
    panel_one(g)
    # panel_two(g)
    bn.MainLoop()    
       
if __name__ == '__main__':
     main()
