# -*- coding: utf-8 -*-
"""
Created on Sun May 25 13:23:21 2014

@author: labuser67
"""

import wx
# import wx.aui
import wx.grid as gridlib
import wx.lib.agw.aui as aui
import os
import BayesianNetwork2 as BN
import functools
import datetime
import numpy as np

evidenceHolder = [] 

#Frame - can't figure out how to change initial size
class BNGUI(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(BNGUI,self).__init__(*args,**kwargs)
        self.InitUI()
        self.SetBackgroundColour("white")
        del BN.nodesSave[:]
        del BN.parentsSave[:]
        del BN.statesSave[:]
        del BN.cptsSave[:]
        del BN.evidenceList[:]
        del BN.cpts[:]

    def InitUI(self):
        menubar = wx.MenuBar()
        
        #File Menubar
        fileMenu = wx.Menu()
        fileMenu.Append(wx.ID_NEW, '&New')
        menuOpen = fileMenu.Append(wx.ID_OPEN, '&Open')
        fileMenu.Append(wx.ID_SAVE, '&Save')
        fileMenu.AppendSeparator()
        
        qmi = wx.MenuItem(fileMenu, wx.ID_EXIT, '&Quit\tCtrl+W')
        fileMenu.AppendItem(qmi)
        
        self.Bind(wx.EVT_MENU, self.OnQuit, qmi)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        menuSave = fileMenu.Append(wx.ID_SAVE, '&Save')
        #fileMenu.AppendSeparator()
        
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
        #cpt menu
        cptMenu = wx.Menu()
        menubar.Append(cptMenu, '&CPT')
        cptsize=cptMenu.Append(wx.ID_ANY, 'Size')
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.Oncptinput, cptsize)
        
        cptread=cptMenu.Append(wx.ID_ANY, 'Input')
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.Oncptread, cptread)
        
        cptclear=cptMenu.Append(wx.ID_ANY, 'Clear')
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.Oncptclear, cptclear)

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

        #Panel Layout Management
        '''
        leftpanel = DrawPanel(self)
        rightpanel = InferencePanel(self)
        '''
        self.mgr = aui.AuiManager(self)


        
        #rightpanel = wx.Panel(self, -1, size = (200, 150))
        #bottompanel = wx.Panel(self, -1, size = (200, 100))
        self.centerpanel = DrawPanel(self)
        self.leftpanel = panel_one(self)
        self.bottompanel = CPTPanel(self)
        
        self.mgr.AddPane(self.bottompanel, aui.AuiPaneInfo().Bottom().MinSize((400,125)))
        self.mgr.AddPane(self.centerpanel, aui.AuiPaneInfo().Center().Layer(1))
        self.mgr.AddPane(self.leftpanel, aui.AuiPaneInfo().Left().
        Layer(2).MinSize((200,200)))
        self.mgr.Update()

        
    def Oncptinput(self,e):
        CPTsize()
    
    def Oncptread(self,e):
        getcptinput(self.bottompanel.grid)
        BN.cpts = np.split(inputs,column)
    
    def Oncptclear(self,e):
        global inputs
        inputs=[]
        global row
        row=[]
        global column
        column=[]
        self.bottompanel.grid.ClearGrid()    
    

    def ToggleStatusBar(self, e):
        if self.shnw.IsChecked():
            self.statusbar.Show()
        else:
            self.statusbar.Hide()

    def OnQuit(self, e):
        self.Close()

    def OnOpen(self,e):
        '''Load in existing JSON file - This works currently'''
        del BN.nodesSave[:]
        del BN.parentsSave[:]
        del BN.statesSave[:]
        del BN.cptsSave[:]
        del BN.evidenceList[:]
        del BN.cpts[:]
        dlg = wx.FileDialog(self, "Choose a file", style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFilename()
            dirname = dlg.GetDirectory()
            f= dirname + '/' + filename
            BN.load(f) #Load and parse network from properly-formatted JSON file
        dlg.Destroy()
        #self.Bind(wx.EVT_PAINT, self.centerpanel.OnPaint) #draw circles 
        #DrawPanel.Refresh(self.centerpanel)
        self.centerpanel.OnPaintNow()

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
        
        # self.SetSize((900, 200))

        # View Properties button
        ViewPropBtn = wx.Button(self, label="View Node Properties", pos = (0,0))
        ViewPropBtn.Bind(wx.EVT_BUTTON, self.ChooseNodeToView)

        # Set Evidence button
        EvidenceBtn = wx.Button(self, label="Set Evidence", pos = (0,30))
        EvidenceBtn.Bind(wx.EVT_BUTTON, self.ChooseEvidenceNode)

        # Clear Evidence button
        ClearEvidence = wx.Button(self, label="Delete Evidence", pos = (0,60))
        ClearEvidence.Bind(wx.EVT_BUTTON, self.DeleteEvidenceNode)

        # Sizer = wx.BoxSizer(wx.HORIZONTAL)
        # Sizer.Add(ViewPropBtn, 0, wx.ALIGN_LEFT|wx.ALL, 5)
        # #Sizer.Add(EvidenceBtn, 0, wx.ALIGN_LEFT|wx.ALL, 5)
        # Sizer.Add(self, 0, wx.EXPAND)
        # #Sizer.SetSizeHints(self)
        # self.SetSizer(Sizer)

        self.text = wx.StaticText(self, -1, "", (0, 90))
        self.prop = wx.StaticText(self, -1, "", (0, 90))
        self.ExitPropBtn = wx.StaticText(self, -1, "", (0, 90))
        # self.ch = wx.StaticText(self, -1, "", (0, 90))
        self.ch = wx.Choice(self, -1, (0, 120), choices = [])
        self.ch2 = wx.Choice(self, -1, (0, 120), choices = [])
        self.ch2.Hide()
        self.ch.Hide()
        
        self.SetBackgroundColour("white") 

    def ChooseNodeToView(self, e):
        self.HideEverything()
        #Choices
        if len(BN.nodesSave) > 0: 
            label3 = "Please select node to view:"
            self.text.SetLabel(label3)
            self.text.Show()
            size=self.GetClientSize() 
            sampleList = BN.nodesSave
            #self.ch2 = wx.Choice(self, -1, (0, 120), choices = sampleList)
            self.ch2.SetItems(sampleList)
            self.ch2.Show()
            self.Bind(wx.EVT_CHOICE, self.ViewNode, self.ch2)


    def ViewNode(self, event):
        self.HideEverything()
        # Button to erase properties and redraw everything else
        self.ExitPropBtn = wx.Button(self, label="Return to Home")
        self.ExitPropBtn.Bind(wx.EVT_BUTTON, self.ReturnToHome)

        Sizer = wx.BoxSizer(wx.VERTICAL)
        Sizer.Add(self.ExitPropBtn, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        self.SetSizerAndFit(Sizer)

        node = event.GetString() #this gets the value selected from the dropdown
        #List Control
        id=wx.NewId()
        self.prop=wx.ListCtrl(self,id, size=(500,100),pos = (0,200), style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        Sizer.Add(self.prop, 0, wx.ALIGN_BOTTOM|wx.ALL, 5)
        self.SetSizerAndFit(Sizer)
        self.prop.Show(True)

        bnIndex = BN.nodesSave.index(node)
        self.prop.InsertColumn(0,'Parent',width = 60)
        self.prop.InsertColumn(1,'States', width = 120)
        self.prop.InsertColumn(2,'CPT', width = 500)

        # 0 will insert at the start of the list
        pos = self.prop.InsertStringItem(0,str(BN.parentsSave[bnIndex]))
        # add values in the other columns on the same row
        self.prop.SetStringItem(pos,1,str(BN.statesSave[bnIndex]))
        self.prop.SetStringItem(pos,2,str(BN.cptsSave[bnIndex]))
        #text0.Destroy()
        #self.Refresh

    def ChooseEvidenceNode(self, event):
        #Choices
        #self.Refresh
        self.HideEverything()
        self.nodeList = BN.nodesSave
        label4 = "Please select node to set evidence on:"
        self.text.SetLabel(label4)
        self.text.Show()
        #self.ch = wx.Choice(self, -1, (0, 150), choices = self.nodeList)
        self.ch.SetItems(self.nodeList)
        self.ch.Show()
        #self.ch.CenterOnParent()
        self.Bind(wx.EVT_CHOICE, self.ChooseEvidenceState, self.ch)

    def ChooseEvidenceState(self, event):
        self.HideEverything()
        self.ch = wx.Choice(self, -1, (0, 120), choices = self.nodeList)
        evidenceNode = event.GetString()
        evidenceHolder.append(evidenceNode)
        stateList = BN.statesSave[BN.nodesSave.index(evidenceNode)]
        label = "Please select state for evidence:"
        self.text.SetLabel(label)
        self.text.Show()
        self.ch.SetItems(stateList) 
        self.Bind(wx.EVT_CHOICE, self.SetEvidence, self.ch)

    def SetEvidence(self, event):
        self.HideEverything()
        state = event.GetString()
        statePosition = []
        statePosition.append(len(BN.statesSave[BN.nodesSave.index(evidenceHolder[0])]))
        statePosition.append((BN.statesSave[BN.nodesSave.index(evidenceHolder[0])].index(state))+1) 
        BN.evidenceList.append({evidenceHolder[0]:statePosition})
        del evidenceHolder[:]
        self.ch.Hide()
        label2 = "Evidence set!"
        self.text.SetLabel(label2)
        self.text.CenterOnParent

    def DeleteEvidenceNode(self,event):
        self.HideEverything()
        self.hello = wx.TextEntryDialog(self, 'Please enter name of node for evidence removal: ')
        if self.hello.ShowModal() == wx.ID_OK:
            delete = self.hello.GetValue()
            if len(BN.evidenceList) == 0:
                lg = wx.MessageDialog(self, message='No evidence has been set.',
                caption='Error', style=wx.OK|wx.ICON_INFORMATION)
                lg.ShowModal()
                lg.Destroy()
            else:
                #print()
                found = False
                i = 0
                while found == False and i < len(BN.evidenceList):
                    if delete in BN.evidenceList[i].keys():
                        del BN.evidenceList[i]
                        dlg2 = wx.MessageDialog(self, message='Evidence removed.',
                        caption='Success', style=wx.OK|wx.ICON_INFORMATION)
                        dlg2.ShowModal()
                        dlg2.Destroy()
                        found = True  
                    else:
                        i = i+1
                if found == False:
                    dlg = wx.MessageDialog(self, message='Evidence was not set for this node.', caption='Error', style=wx.OK|wx.ICON_INFORMATION)
                    dlg.ShowModal()
                    dlg.Destroy()       

    def ReturnToHome(self, event):
        self.prop.Hide()
        self.ExitPropBtn.Hide()
        self.ch2.Hide()
        self.ch.Hide()

    def HideEverything(self):
        self.prop.Hide()
        self.ExitPropBtn.Hide()
        self.ch2.Hide()
        self.ch.Hide()
        self.text.Hide()



    def __del__( self ):
        pass

class DrawPanel(wx.Panel):
    P = [] 
    Qc = [] 
    Qb = []  
    r = 40 #circle radius
    dim = 0 #len(P) 
    j = 0 
    t = 0 
    d = 0
    
    def __init__(self, parent): 
        wx.Panel.__init__(self, parent) 

        AddNodeBtn = wx.Button(self, label="Add Node")
        AddNodeBtn.Bind(wx.EVT_BUTTON, self.AddNode)

        # InfBtn = wx.Button(self, label="Do Inference")
        # InfBtn.Bind(wx.EVT_BUTTON, self.OnInfBtn)

        #Align buttons top left
        # Sizer = wx.BoxSizer(wx.HORIZONTAL)
        # Sizer.Add(AddNodeBtn, 0, wx.ALIGN_LEFT|wx.ALL, 5)
        # Sizer.Add(InfBtn, 0, wx.ALIGN_TOP|wx.ALL, 5)
        

        # self.SetSizerAndFit(Sizer)
        # self.InitBuffer() 
        # self.Buffer = None 
        # self.SetSize((900, 500))

    def InitBuffer(self):
        '''Setup canvas for circle drawing'''

        size=self.GetClientSize() 
        self.Buffer = wx.EmptyBitmap(size.width, size.height) 
        self.dc = wx.MemoryDC() 
        self.dc.SelectObject(self.Buffer)
    
    def OnPaintNow(self):  #for the initial JSON load
        '''Called when AddNode button is clicked - draw circle and line''' 
        self.Bind(wx.EVT_PAINT, self.OnPaint)        
        self.Refresh()
        #self.dc = wx.PaintDC(self)       
               
        #self.drawCircle()
    
        
    def OnPaint(self, evt):
        '''Called when AddNode button is clicked - draw circle and line''' 
        
        self.dc = wx.PaintDC(self)       
               
        self.drawCircle() 

        #self.InitBuffer()


    def drawCircle(self): 
        node_place = []
        self.dc.SetPen(wx.Pen("black", style=wx.SOLID)) 
       
        self.dim = len(BN.nodesSave)
        j = 0
        for i in range(self.dim):
            online = 0
            node_prop = []
            if len(BN.parentsSave[i]) ==0:            
                self.dc.DrawCircle(100*(i+1),150, self.r)
                self.text = wx.StaticText(self, label=BN.nodesSave[i], pos=(100*(i+1),150))
                node_prop.append(BN.nodesSave[i])
                node_prop.append(100*(i+1))
                node_prop.append(150)
                node_place.append(node_prop)
            else:
                for l in range(len(node_place)):
                    for k in range(len(BN.parentsSave[i])):
                        if BN.parentsSave[i][k] == node_place[l][k]: 
                            temp = (node_place[l][k+2] - 50)/100                            
                            if temp > online:
                                online = temp
                j = j+1
                self.dc.DrawCircle(100+(j*120),150+(100*online) , self.r) 
                self.text =wx.StaticText(self, label=BN.nodesSave[i], pos=(100+(j*120),150+(100*online)))
                node_prop.append(BN.nodesSave[i])
                node_prop.append(100+(j*120))
                node_prop.append(150+(100*online))
                node_place.append(node_prop)
                self.drawLine(node_place,i)
            #print(node_place) 
            
    def drawLine(self,node_place,node_num): 
        '''Connect circles'''
        self.dc.SetPen(wx.Pen('#4c4c4c', 1, wx.SOLID)) 

        for node_name in range(len(node_place)):
            for index in range(len(BN.parentsSave[node_num])):            
                if  node_place[node_name][0] == BN.parentsSave[node_num][index]:
                    #self.dc.DrawLine(100+((j-1)*100), 150+(100*(online-1))+self.r, 100+(100*j) ,150+(online*100)-self.r)
                    self.dc.DrawLine(node_place[node_name][1], node_place[node_name][2]+self.r, node_place[node_num][1] ,node_place[node_num][2]-self.r)
            
    def AddNode(self, e):
        '''Create a node from scratch - Only draws circle right now (won't draw multiple circles if you click button multiple times)'''
        continue_draw = 0
        #self.P = [] 
        #self.Qc = [] 
        #self.Qb = []         
        continue_draw = getInputs() #get info needed - eventually display within circles (maybe), or try and allow for right clicking in circle and open 'properties'
        self.dim = len(BN.nodesSave)
        #print(self.dim)
        for i in range(self.dim):
            self.P.append(200+i*200)
            self.Qb.append(200)
            self.Qc.append(200)        
        
        #for n in BN.nodesSave:
            #self.drawCircle()
        if continue_draw == 0:        
            self.Bind(wx.EVT_PAINT, self.OnPaint) #draw circles 
            self.Refresh()
        #self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown) #allow for moving of cirlces/lines
        #self.Bind(wx.EVT_LEFT_UP, self.MouseUp) 
        #self.Bind(wx.EVT_MOTION, self.MouseMove)
        
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
        


class CPTPanel(wx.Panel):   
    def __init__(self,parent):
        wx.Panel.__init__(self,parent)
        hbox = wx.BoxSizer(wx.VERTICAL)
        size=self.GetClientSize()
        self.st1 = wx.StaticText(self,-1, label='',pos= (size.width*12,size.height*.1))
        self.st2 = wx.StaticText(self,-1, label='Results:',pos= (size.width*6,size.height*.3))
        self.Show(True) 
        
        # Do Inference button
        InferenceAll = wx.Button(self, label="Do Inference", pos = (0,0))
        InferenceAll.Bind(wx.EVT_BUTTON, self.DoAllInference)

        #Align buttons
        hbox.Add(InferenceAll, flag=wx.ALL, border=5)
        self.SetSizer(hbox)

    def DoAllInference(self,event):
        self.st1.SetLabel('')
        potentials = BN.cpts + BN.setEvidenceList(BN.evidenceList)
        printList = BN.doAllInference(potentials) 
        #Putting results on panel
        self.st1.SetLabel(printList)
        
def CPTsize(parent=None):
        #define the table size
    dlg = wx.TextEntryDialog(parent, 'What is the dimemsion of cpt? Enter the number of rows:')
    dlg.ShowModal()
    rowsize = int(dlg.GetValue())
    dlg.Destroy()
    
    dlg2 = wx.TextEntryDialog(parent, 'Enter the number of columns:')
    dlg2.ShowModal()
    columnsize = int(dlg.GetValue())
    dlg2.Destroy()
    return (rowsize,columnsize)        

def getcptinput(mygrid):
    #get input values
    for i in row:
        for j in column:
            value = mygrid.GetCellValue(i,j) 
            inputs.append(value)

def getInputs(parent = None):
    '''Get inputs needed to create node and add to inputs to global lists in BN'''
    #Input name
    parents = []
    states = []
    didicancel = 0    
    dlg = wx.TextEntryDialog(parent, 'Please enter name of node: ')
    if dlg.ShowModal() == wx.ID_OK:
        myaddednode = dlg.GetValue()
        name = myaddednode
    else:
        didicancel = 1
    #print(BN.nodesSave)
    #Input parents - CHANGE -> ask for number of parents and have new window pop up for each
    dlg.Destroy()
    dlg2 = wx.TextEntryDialog(parent, 'Please enter number of parents: ')
    
    if dlg2.ShowModal() == wx.ID_OK:
        parents_Num = int(dlg2.GetValue())
    else:
        parents_Num = -1
        didicancel = 1
        
    #print(parents_Num)
    dlg2.Destroy()
    for i in range(parents_Num):
        #print(i)
        dlg3 = wx.TextEntryDialog(parent,"Please enter name of parent %d: " %(i+1))
        if dlg3.ShowModal() == wx.ID_OK:
            parents.append(dlg3.GetValue())
        else:
            didicancel = 1
            
        dlg3.Destroy()
    parents.reverse() 
    parents = ''.join(parents)
    if parents_Num > 0:
        together = parents + name
    if parents_Num == 0:
        together = name
        
    dlg4 = wx.TextEntryDialog(parent, 'Please enter number of states: ')
    
    if dlg4.ShowModal() == wx.ID_OK:
        states_Num = int(dlg4.GetValue())
    else:
        states_Num = 0
        didicancel = 1
    #print(states_Num)
    dlg4.Destroy()
    for z in range(states_Num):
        #print(i)
        dlg5 = wx.TextEntryDialog(parent,"Please enter state %d: " %(z+1))
        if dlg5.ShowModal() == wx.ID_OK:
            states.append(dlg5.GetValue())
        else:
            didicancel = 1
            
        dlg5.Destroy()

    dlg6 = wx.TextEntryDialog(parent, 'Please enter probability distribution: ')  
    if dlg6.ShowModal() == wx.ID_OK:
        cpt_input = eval(dlg6.GetValue())
    else:
        didicancel = 1
    #print(cpt_input)
    dlg6.Destroy()
    
    if didicancel ==0:
                
        cpt = BN.TablePotential(together,cpt_input)
        BN.cpts.append(cpt)
        
        BN.parentsSave.append(parents)
        BN.statesSave.append(states)
        BN.nodesSave.append(myaddednode)
        BN.cptsSave.append(cpt_input)
    
    #print(BN.parentsSave)
    #print(BN.statesSave)
    return didicancel
    #Input States - same as parents (ask for number first)
    #Input cpts (ideally grab parent states and create table to allow user to enter)
def main():
    bn = wx.App()
    g = BNGUI(None)
    bn.MainLoop()    
       
if __name__ == '__main__':
     main()