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
<<<<<<< HEAD
        fileMenu.Append(wx.ID_SAVE, '&Save')
        fileMenu.AppendSeparator()
        
        qmi = wx.MenuItem(fileMenu, wx.ID_EXIT, '&Quit\tCtrl+W')
        fileMenu.Append(qmi)
        
        self.Bind(wx.EVT_MENU, self.OnQuit, qmi)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
=======
        menuSave = fileMenu.Append(wx.ID_SAVE, '&Save')
        fileMenu.AppendSeparator()
        
        qmi = fileMenu.Append(wx.ID_EXIT, '&Quit\tCtrl+W')
        
        self.Bind(wx.EVT_MENU, self.OnQuit, qmi)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnSave, menuSave)
>>>>>>> 6dce7e03e8ca7e4c25107363ec9206c0a19235e9

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

        self.SetSize((700, 600))
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
<<<<<<< HEAD

    def OnSave(self,e):
        '''Save JSON file'''
        pass
=======
        
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
>>>>>>> 6dce7e03e8ca7e4c25107363ec9206c0a19235e9

#Panel within frame - special type of panel for painting objects on
class DrawPanel(wx.Panel):
    P = [200] 
    Qc = [200] 
    Qb = [200]  #where to draw circle on canvas
    r = 80 #circle radius
    dim = len(P) 
    j = 0 #not sure what these are for
    t = 0 
    d = 0

    def __init__(self, parent): 
        wx.Panel.__init__(self, parent) 

        # 'Add node' button (calls AddNode function)
        AddNodeBtn = wx.Button(self, label="Add Node")
        AddNodeBtn.Bind(wx.EVT_BUTTON, self.AddNode)

        # 'Do Inference' button (will eventually call DoInference Function from BN)
        InfBtn = wx.Button(self, label="Do Inference")
        InfBtn.Bind(wx.EVT_BUTTON, self.OnInfBtn)

        #Align buttons top left
        Sizer = wx.BoxSizer(wx.HORIZONTAL)
        Sizer.Add(AddNodeBtn, 0, wx.ALIGN_LEFT|wx.ALL, 5)
        Sizer.Add(InfBtn, 0, wx.ALIGN_TOP|wx.ALL, 5)

        self.SetSizerAndFit(Sizer)
        self.InitBuffer() 
        self.Buffer = None 
        #self.SetBackgroundColour("white")
        self.SetSize((700, 600))

    def InitBuffer(self):
        '''Setup canvas for circle drawing''' 
        size=self.GetClientSize() 
        self.Buffer = wx.EmptyBitmap(size.width, size.height) 
        self.dc = wx.MemoryDC() 
        self.dc.SelectObject(self.Buffer) 
        
    def OnPaint(self, evt):
        '''Called when AddNode button is clicked - draw circle and line''' 
        self.dc = wx.PaintDC(self)       
        self.drawCircle() 
        self.Refresh() 
        self.InitBuffer 
        self.drawLine() 

    def drawCircle(self): 
        self.dc.SetPen(wx.Pen("black", style=wx.SOLID)) 
        #self.dc.SetBrush(wx.Brush("red", wx.TRANSPARENT)) 
        for i in range(self.dim):
            self.dc.DrawCircle(self.P[i], self.Qc[i], self.r)  

    def drawLine(self): 
        '''Connect circles'''
        self.dc.SetPen(wx.Pen('#4c4c4c', 1, wx.SOLID)) 

        for i in range(1,self.dim): #will need to store circle dimensions in array so lines can be drawn
            self.dc.DrawLine(self.P[i-1], self.Qc[i-1], self.P[i], self.Qc[i])  

    def MouseMove(self, e): 
        '''Drag circles and lines'''
        x, y = e.GetPosition() 

        if self.d == 1: 
            if self.t == 0: 
                self.P[self.j] = x 
                self.Qc[self.j] = y 
            elif self.t == 1: 
                self.P[self.j] = x 
                self.Qb[self.j] = y 
            else: pass 

            self.drawCircle() 
            self.drawLine() 
            self.Refresh() 
            self.InitBuffer 
        
        else: pass 
        

    def MouseUp(self, e): 
        '''Drag circles and lines'''
        self.d = 0 

    def MouseDown(self, e): 
        '''Drag circles and lines'''
        self.d = 1 

        x, y = e.GetPosition() 
        
        for i in range(self.dim): 
            P = abs(self.P[i]-abs(x))//self.r 
            Qb = abs(self.Qb[i]-abs(y))//self.r 
            Qc = abs(self.Qc[i]-abs(y))//self.r 

            if P == 0: 
                if Qb == 0: 
                    self.j = i 
                    self.t = 1 
                elif Qc == 0: 
                    self.j = i 
                    self.t = 0 
                else: pass 
            else: pass 

    def AddNode(self, e):
        '''Create a node from scratch - Only draws circle right now (won't draw multiple circles if you click button multiple times)'''
        getInputs() #get info needed - eventually display within circles (maybe), or try and allow for right clicking in circle and open 'properties'
        self.Bind(wx.EVT_PAINT, self.OnPaint) #draw circles 
        self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown) #allow for moving of cirlces/lines
        self.Bind(wx.EVT_LEFT_UP, self.MouseUp) 
        self.Bind(wx.EVT_MOTION, self.MouseMove)
    
    def OnInfBtn(self, event=None):
        """Show results (eventually)."""
        #this will call BN.doInference eventually and display results - need to think about display
        dlg = wx.MessageDialog(self,
                               message='Here is your answer',
                               caption='Inference',
                               style=wx.OK|wx.ICON_INFORMATION
                               )
        dlg.ShowModal()
        dlg.Destroy()

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

 
def main():
    bn = wx.App()
    g = BNGUI(None)
<<<<<<< HEAD
    DrawPanel(g)
    bn.MainLoop()    
    
if __name__ == '__main__':
     main()
=======
    #DrawPanel(g)
    bn.MainLoop()    
    
if __name__ == '__main__':
     main()
>>>>>>> 6dce7e03e8ca7e4c25107363ec9206c0a19235e9
