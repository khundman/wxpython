#Testing a commit

import wx
import BayesianNetwork as BN

class BNGUI(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(BNGUI,self).__init__(*args,**kwargs)
        
        self.InitUI()
        
    def InitUI(self):
        menubar = wx.MenuBar()
        
        #File Menubar
        fileMenu = wx.Menu()
        fileMenu.Append(wx.ID_NEW, '&New')
        fileMenu.Append(wx.ID_OPEN, '&Open')
        fileMenu.Append(wx.ID_SAVE, '&Save')
        fileMenu.AppendSeparator()
        
        qmi = wx.MenuItem(fileMenu, wx.ID_EXIT, '&Quit\tCtrl+W')
        fileMenu.AppendItem(qmi)
        
        self.Bind(wx.EVT_MENU, self.OnQuit, qmi)

        menubar.Append(fileMenu, '&File')
        
        #View Menubar
        viewMenu = wx.Menu()
        self.shnw = viewMenu.Append(wx.ID_ANY, 'Show Network', 
            'Show Statusbar', kind=wx.ITEM_CHECK)
        
        viewMenu.Check(self.shnw.GetId(), True)
        
        self.Bind(wx.EVT_MENU, self.ToggleStatusBar, self.shnw)
        
        menubar.Append(viewMenu, '&View')
        self.SetMenuBar(menubar)
        
        self.toolbar = self.CreateToolBar()
        self.toolbar.Realize()

        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText('Ready')

        self.SetSize((350, 250))
        self.SetTitle('Check menu item')
        self.Centre()
        self.Show(True)
        
        
    def ToggleStatusBar(self, e):
        
        if self.shnw.IsChecked():
            self.statusbar.Show()
        else:
            self.statusbar.Hide()

    def OnQuit(self, e):
        self.Close()
 
def main():
    
    bn = wx.App()
    BNGUI(None)
    bn.MainLoop()    
    
if __name__ == '__main__':
    main()