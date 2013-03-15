'''
>midl c:\home\simon\src\asimpleapp\taskbar.idl /tlb TaskbarLib.tlb

Created on 8 mrt. 2013

@author: simon
'''
import os
import sys
import wx
import time
import comtypes.client as cc
import comtypes.gen.TaskbarLib as tbl
from threading import Thread

import urllib2
import urllib
import mimetypes

import SocketServer

TBPF_NOPROGRESS = 0
TBPF_INDETERMINATE = 0x1
TBPF_NORMAL = 0x2
TBPF_ERROR = 0x4
TBPF_PAUSED = 0x8

__version__ = "0.1"

cc.GetModule("c:\python27\Lib\TaskbarLib.tlb")
taskbar = cc.CreateObject("{56FDF344-FD6D-11d0-958A-006097C9A090}", interface=tbl.ITaskbarList3)

    
class ThreadingSocketServer (SocketServer.ThreadingMixIn,
                           SocketServer.TCPServer): pass
 
class SocketRequestHandler (SocketServer.BaseRequestHandler):
    __base = SocketServer.BaseRequestHandler
    __base_handle = __base.handle

    server_version = 'OfficeDrive Daemon' + __version__
    rbufsize = 8192                        # self.rfile Be unbuffered
 
    def handle(self):
        (ip, port) =  self.client_address
        
        sys.stdout.write("Connection from: %s:%s\n" %(ip, port))
        while True:
            try:
                data = self.request.recv(8192)
            except (Exception) as e:
                pass
            if data:
                sys.stdout.write(data)
                try:
                    self.request.send("cmd: %s\n" %data)
                except (Exception) as e:
                    pass
        self.__base_handle()


class MyRequest(urllib2.Request):
    GET =   'GET'
    POST =  'POST'
    PUT =   'PUT'
    DELETE ='DELETE'

    def __init__(self, url, data=None, headers={},
        origin_req_host=None, unverifiable=False, method=None):
        urllib2.Request.__init__(self, url, data, headers, origin_req_host, unverifiable)
        self.method = method

    def get_method(self):
        if self.method:
            return self.method

        return urllib2.Request.get_method(self)


class ConsoleWindow(wx.Frame):
    TBMENU_RESTORE = wx.NewId()
    TBMENU_CLOSE   = wx.NewId()
    TBMENU_UPLOAD  = wx.NewId()
    TBMENU_REMOVE  = wx.NewId()
    WINDOW_CLOSE   = wx.NewId()
    
    def __init__(self, parent, ID, title):
        """
        Constructor for ConsoleWindow class
        """
        wx.Frame.__init__(self, parent, ID, title)
        icon = wx.Icon("../res/logo officedrive light beveled64.ico")
        self.statusicon = wx.TaskBarIcon()
        self.statusicon.SetIcon(icon)
        self.SetIcon(icon)
        
        self.statusicon.Bind(wx.EVT_MENU, self.OnStatusIconClose, id=self.TBMENU_CLOSE)
        self.statusicon.Bind(wx.EVT_MENU, self.launchFileSelect, id=self.TBMENU_UPLOAD)
        self.statusicon.Bind(wx.EVT_TASKBAR_RIGHT_DOWN, self.OnStatusIconRightClick)
         
        self.console = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_AUTO_URL)
        self.console.SetInitialSize(self.Size)
        
        self.fileDialog = wx.FileDialog(self)
        
        dWidth, dHeight = wx.GetClientDisplayRect()[-2:]
        wWidth, wHeight = self.GetSize()
        
        self.MoveXY(dWidth - wWidth, dHeight - wHeight)
        
        self.socketserver = ThreadingSocketServer(("127.0.0.1", 8000), SocketRequestHandler)
        self.socketserverThread = Thread(target=self.socketserver.handle_request)
        self.socketserverThread.setDaemon(True)
        self.socketserverThread.start()
        
        self.console.AppendText("Accepting connections on: %s:%s\n" %self.socketserver.server_address)
        self.Show()
       
    
    def __del__(self, evt=None):
        self.statusicon.RemoveIcon()
        self.statusicon.Destroy()

    def launchFileSelect(self, evt):
        self.uploader = Thread(target=self.fileSelect)
        self.uploader.setDaemon(True)
        self.uploader.start()

    def CreatePopupMenu(self, evt=None):
        """
        This method is called by the base class when it needs to popup
        the menu for the default EVT_RIGHT_DOWN event.
        """
        menu = wx.Menu()
        menu.Append(self.TBMENU_UPLOAD, "&Upload File")
        #menu.Append(self.TBMENU_CHANGE, "Show all the Items")
        menu.AppendSeparator()
        menu.Append(self.TBMENU_CLOSE,   "&Exit Program")
        
        return menu    
gi
    def OnStatusIconRightClick(self, evt):
        """
        Create the right-click menu
        """
        menu = self.CreatePopupMenu()
        self.statusicon.PopupMenu(menu)
        menu.Destroy()

    def OnStatusIconClose(self, evt):
        """
        Destroy the taskbar icon and console window
        """
        self.Close()
        

    def uploadFile(self, fileName):
        hWnd = self.GetHandle()
        taskbar.HrInit()
        taskbar.SetProgressState(hWnd, TBPF_NORMAL)
        
        progress_ascii = ["|", "/", "-", "\\" ]
        
        host = "test.officedrive.net"
        urlext = "/fileuploader/transponder.php?sid=LxN2TjrqmppGCCA4lQhOp2WUEx10rG&action=uploadFileInFolder&folderId=1&" + urllib.urlencode( [("path", os.path.basename(fileName))])
        chunk_size = 16384
        f = open(fileName,"rb")
        filesize = os.stat(fileName)[6]
        sent_bytes = 0
        self.console.Disable()
        self.console.WriteText("Uploading: %s (%d)\n" %(fileName, filesize))
        self.console.Update()
                
        conn = urllib2.httplib.HTTPSConnection(host, 443)
        conn.putrequest("PUT", "%s" %urlext)
        conn.putheader("Cookie","LxN2TjrqmppGCCA4lQhOp2WUEx10rG=S9wn0yYl-oxCEebaGnPVqzwRP3dD_md9cfpRrMTrShwwIdfR6WSzCvvI-NRngbko4H7M-R1KPDxo1ko8FA_6mdHdhd-sAj6-Zzi6ut9jWbKsFyepsth1Gqk8Y80gUxLrGGsUZ47SMiVEyqRvkt_sNW2NU1uXt-Y4RuHazEL6XoOm1Xw_gEqWTDhD_gHhjET2-OFyTFlg;")
        #conn.putheader("Cookie", "mzMTnrwjDB2W1oYoGIVme6SLehHvDA=fcTH9Q6e3Cn4zrGbuIaPaiJzWLx-0NHTVHE52YBfZmqNMFD_5MiGeImb-JUSaJzJsrC1HXYIt84CuVE_cj-Lbi-OyFSmsqTGa562u0AdPCqMaDWRnAkHSDy5mZ7i9VU6NNv1KzDbPS3-VEnVLOtIUGQFiNaH03G3Cd01TaktcdASYnXYNlH_SeEQwpXH8fW5GeLR5ILj;")
        conn.putheader("Content-Length", filesize)
        #conn.putheader("Transfer-Encoding", "chunked")
        #conn.putheader("Content-Type", "application/zip")
        conn.putheader("Content-Type", mimetypes.guess_type(fileName))
        conn.endheaders()
        pos = len(self.console.Value)
        
        while sent_bytes < filesize:
            data = f.read(chunk_size)
            conn.send(data)
            sent_bytes += len(data)
            
            taskbar.SetProgressValue(hWnd, sent_bytes, filesize)
            #self.console.Remove(pos, pos + 1)
            self.console.AppendText("#")
            #self.console.AppendText(progress_ascii[0])
            pos += 1
            
            #progress_ascii.insert(0, progress_ascii.pop())
            self.console.Update()
            
        
        res = conn.getresponse() 
        self.console.AppendText("\n%s\n" %res.read())
        
        
    def fileSelect(self):
        self.fileDialog.ShowModal()
        fileName = self.fileDialog.GetPath()
        if fileName:
            self.uploadFile(fileName)
            
                    


if __name__ == '__main__':
    app = wx.App()
    w = ConsoleWindow(None, wx.ID_ANY, "OfficeDrive Console")
    app.SetTopWindow(w)
    app.MainLoop()
    
    