from PyQt4 import QtGui
from threading import Thread
import time
import sys
import comtypes.client as cc
import comtypes.gen.TaskbarLib as tbl

TBPF_NOPROGRESS = 0
TBPF_INDETERMINATE = 0x1
TBPF_NORMAL = 0x2
TBPF_ERROR = 0x4
TBPF_PAUSED = 0x8

cc.GetModule("c:\python27\Lib\TaskbarLib.tlb")
taskbar = cc.CreateObject("{56FDF344-FD6D-11d0-958A-006097C9A090}", interface=tbl.ITaskbarList3)

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setWindowTitle("Test")
        self.statusicon = QtGui.QSystemTrayIcon(self)
        icon = QtGui.QIcon()
        icon.addFile("c:\\home\\simon\\src\\firebreath-dev\\projects\\officedrive\\logo officedrive light beveled64.ico") 
        icon.name = "Foobar"
        self.setWindowIcon(icon)
                
        self.statusicon.setIcon(icon)
        
        self.progress_bar = QtGui.QProgressBar(self)
        self.setCentralWidget(self.progress_bar)
        self.progress_bar.setRange(0, 100)

        self.progress = 0
        #self.counter = 1
        self.show()
        self.statusicon.show()
        thread = Thread(target=self.counter)
        thread.setDaemon(True)
        thread.start()

    def counter(self):
        while True:
            self.progress += 1
            if self.progress > 100:
                self.progress = 0

            time.sleep(.2)

            self.progress_bar.setValue(self.progress)

            taskbar.HrInit()
            hWnd = self.winId()
            taskbar.SetProgressState(hWnd, TBPF_NORMAL)        
            taskbar.SetProgressValue(hWnd, self.progress, 100)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ui = MainWindow()
    sys.exit(app.exec_())