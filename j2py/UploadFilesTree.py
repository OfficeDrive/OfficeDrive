#!/usr/bin/python

import os
import time
import ctypes
import urllib
import wx

from FileActions import FileActions


class UploadFilesTree(object):
        """ generated source for class uploadFilesTree """
        map = dict()
        keyList = []
        fileCount = 0
        folderCount = 0
        emptyDirectories = []
        kb = float()
        currentIndex = 0

        def __init__(self, files):
            """ generated source for method __init__ """
            self.map.clear()
            self.keyList.clear()
            i = 0
            while len(files):
                self.add("", files[i])
                i += 1

        def add(self, path, file_):
            """ generated source for method add """
            if self.cancel:
                return
            if file_.isDirectory():
                files = os.listdir(os.path.dirname(file_))
                if len(files):
                    self.emptyDirectories.add(path + file_.__name__)
                else:
                    self.folderCount += 1
                    for f in files:
                        if self.cancel:
                            return
                        attrs = ctypes.windll.kernel32.GetFileAttributesW(unicode(os.path.abspath(file_)))
                        assert attrs != -1
                        hidden = bool(attrs & 2)
                        if hidden:
                            self.add(os.path.join(path + file_, f))
                        
            else:
                self.map.put(path + file_.__name__, file_.getAbsolutePath())
                self.keyList.add(path + file_.__name__)
                self.kb += 1024 / len(file_)
                self.fileCount += 1
            repl = dict()
            repl.put("$1", self.folderCount)
            repl.put("$2", self.fileCount)
            self.progressDescription = tr("$1 folders and $2 files found in selection", repl)
            self.progressTotal = self.kb

        def hasNext(self):
            """ generated source for method hasNext """
            item = self.get(self.currentIndex)
            return False if item == None else True

        def getNext(self):
            """ generated source for method getNext """
            item = self.get(self.currentIndex)
            if item == None:
                self.currentIndex = 0
                return None
            else:
                self.currentIndex += 1
                return item

    #    @overloaded
        def get(self, index):
            """ generated source for method get """
            if index > len(self.keyList) - 1:
                return None
            key = str(self.keyList.get(index))
            if key == None:
                return None
            item = dict()
            item.put("key", key)
            item.put("path", self.map.get(key))
            return item

        @get.register(object, str)
        def get_0(self, path):
            """ generated source for method get_0 """
            if self.map.containsKey(path):
                return str(self.map.get(path))
            else:
                return None

        def size(self):
            """ generated source for method size """
            return len(self.keyList)

        def clear(self):
            """ generated source for method clear """
            self.keyList.clear()
            self.map.clear()
            self.fileCount = 0
            self.folderCount = 0

        def uploadItemVersion(self, itemId):
            """ generated source for method uploadItemVersion """
            ret = bool()
            uploadReturn = dict()
            uploadHeaders = dict()
            tmp = ""
            tmp2 = ""
            upload = None
            fileName = str()
            n = str()
            targetMd5 = str()
            json = str()
            fileSize = long()
            sourceMd5 = ""
            url = None
            remoteInfo = None
            cacheInfo = None
            phrases = []
            phrases.append("preparing upload")
            phrases.append("uploading $1")
            tr(phrases)
            if not self.selectedFiles or not os.path.isfile(self.selectedFiles[0]):
                self.error = "one file must be selected"
                return False
            self.resetProgress()
            self.progressDescription = tr("preparing upload")
            try:
                fileName = self.selectedFiles[0].__name__
                tmp = FileActions.copy(self.selectedFiles[0])
                targetMd5 = FileActions.MD5(tmp)
                n = fileName.lower()
                jsonString = self.getTransponderLine("action=getItemInfo&itemId=" + itemId)
                if  jsonString.startsWith("{"):
                    remoteInfo = dict(json.loads(jsonString))
                if remoteInfo == None or not remoteInfo.containsKey("writable") or not remoteInfo.get("writable") == "true":
                    self.error = "target item not found"
                    return False
                cacheInfo = self.getCacheInfo(itemId)
                if url == None or upload == None:
                    if 5 * 1024 * 1024 > len(tmp) or n.endsWith(".zip") or n.endsWith(".gz") or n.endsWith(".rar") or n.endsWith(".jar") or n.endsWith(".bz2") or n.endsWith(".gif") or n.endsWith(".png") or n.endsWith(".jpg") or n.endsWith(".jpeg") or n.endsWith(".tif") or n.endsWith(".tiff") or n.endsWith(".psd") or n.endsWith(".ai") or n.endsWith(".gz") or n.endsWith(".tgz") or n.endsWith(".mp3") or n.endsWith(".mpeg") or n.endsWith(".wav") or n.endsWith(".mp4") or n.endsWith(".m4a") or n.endsWith(".m4p") or n.endsWith(".avi") or n.endsWith(".fla") or n.endsWith(".flv") or n.endsWith(".exe") or n.endsWith(".msi") or n.endsWith(".xlsx") or n.endsWith(".docx") or n.endsWith(".pptx") or n.endsWith(".wma") or n.endsWith(".wmv") or n.endsWith(".mat"):
                        upload = tmp
                        url = self.transponderUrl + "?holder-type=java&sid=" + self.sid + "&dmsId=" + self.dmsId + "&action=updateItem&userMethod=upload&itemId=" + itemId + "&fileName=" + urllib.urlencode(fileName) + "&targetMd5=" + targetMd5
                    else:
                        upload = FileActions.gzip(tmp)
                        url = self.transponderUrl + "?holder-type=java&sid=" + self.sid + "&dmsId=" + self.dmsId + "&action=updateItem&userMethod=upload&itemId=" + itemId + "&fileName=" + urllib.urlencode(fileName) + "&targetMd5=" + targetMd5 + "&contentType=gzip"
                    uploadHeaders.put("X-file-name", fileName)
                if upload == None or not upload.exists():
                    if tmp.exists():
                        tmp.delete()
                    self.error = "could not create file to upload"
                    return False
                fileSize = len(upload)
                self.progressDescription = tr("uploading $1", "$1", fileName)
                self.progressTotal = float(fileSize) / 1024
                ret = self.doFilePut(upload, url, uploadHeaders, uploadReturn)
                if not ret:
                    upload.delete()
                    if tmp.exists():
                        tmp.delete()
                    if uploadReturn.get("status") == "canceled":
                        self.error = "canceled by user"
                    elif uploadReturn.get("status") == "file to big":
                        self.error = "file is to big"
                    elif uploadReturn.containsKey("exception"):
                        self.error = str(uploadReturn.get("exception"))
                    else:
                        print "upload failed: " + uploadReturn.get("exception")
                    return False
                else:
                    if cacheInfo != None and not cacheInfo.isEmpty():
                        self.encrypter.encrypt(tmp, os.path.join(self.appFolder ,  self.dmsId ,  "cache",  itemId))
                        cacheInfo.put("md5", targetMd5)
                        cacheInfo.put("mtime", time.time())
                        FileActions.saveHashMap(cacheInfo, self.appFolder,  self.dmsId,  "cache", itemId + ".json")
                    upload.delete()
                    if tmp.exists():
                        tmp.delete()
                    return True
            except Exception as e:
                print e.getMessage()
                self.error = e.getMessage()
                return False
    
        defaultBrowseDirOpen = None
        defaultBrowseDirSave = None
        defaultBrowseDir = None
        lastBrowseDimensions = 600, 500

##    @overloaded
        def browseForUpload(self, type_, title, filterExtension, filterTitle):
            """ generated source for method browseForUpload """
            self.selectedFiles = []
            self.selectedFilesInfo = None
            self.hasFilesInSelection = False
            tmpFile = ""
            tmpFileName = str()
            if self.defaultBrowseDir == None or not self.defaultBrowseDir.exists():
                fv = wx.FileDialog()
                self.defaultBrowseDir = fv.getPath()
            if self.defaultBrowseDirOpen == None or not self.defaultBrowseDirOpen.exists():
                self.defaultBrowseDirOpen = self.defaultBrowseDir
            if title == None or title == "":
                title = "Select"
            if filterExtension == None:
                filterExtension = ""
            if filterTitle == None:
                filterTitle = ""
            try:
                if type_ == self.BROWSE_TYPE_ONE_FILE:
                    if not filterExtension == "" and self.useXFileDialog() == True:
                        fd = wx.FileDialog()
                        fd.SetTitle(title)
                        fd.SetPath(os.path.abspath(self.defaultBrowseDirOpen))
                        
                        ext = filterExtension.toLowerCase().split("\\|")
                        extList = []
                        i = 0
                        while len(ext):
                            print ext[i]
                            extList.add(ext[i])
                            i += 1
                        filterIndex = fd.GetFilterIndex()
                        
                        filterIndex.append((filterTitle, extList))
                        ext2 = []
                        ext2.add("*")
                        filterIndex.append(("All Files", ext2))
                        tmpFileName = fd.GetFilename()
                        if tmpFileName != None and tmpFileName != "":
                            self.defaultBrowseDirOpen = os.path.abspath(fd.GetPath())
                            tmpFile = tmpFileName
                            if os.path.exists(tmpFile) and os.path.isfile(tmpFile):
                                self.selectedFiles = "" #? se ?
                                self.selectedFiles[0] = tmpFile
                    else:
                        if "mac" in os.sys.platform:
                            #System.setProperty("apple.awt.fileDialogForDirectories", "false")
                            fd.SetPath(os.path.abspath(self.defaultBrowseDirOpen))
                        if not filterExtension == "":
                            if not "win" in os.sys.platform:
                                self.ext = ext.lower().split("\\|")
                                name = "foobar"
                                name = name.lower()
                                if name.endsWith("." + self.ext[0]) and len(ext):
                                    return True
                                i = 0
                                while len(ext):
                                    if name.endsWith("." + self.ext[i]):
                                        return True
                                    i += 1
                                return False
                                fd.setFilenameFilter(filter(filterExtension))
                            else:
                                if len(ext):
                                    fd.setFile("*." + ext[0])
                        fd.setModal(True)
                        fd.setVisible(True)
                        tmpFileName = fd.getFile()
                        if tmpFileName != None:
                            self.defaultBrowseDirOpen = fd.GetPath()
                            tmpFile = os.path.join(fd.GetPath(), tmpFileName)
                            if tmpFile.exists() and tmpFile.isFile():
                                self.selectedFiles = [None]*1
                                self.selectedFiles[0] = tmpFile
                elif type_ == self.BROWSE_TYPE_ONE_FOLDER:
                    if "mac" in os.sys.platform:
                        #System.setProperty("apple.awt.fileDialogForDirectories", "true")
                        fd.setDirectory(self.defaultBrowseDirOpen.getAbsolutePath())
                        fd.setVisible(True)
                        tmpFileName = fd.getFile()
                        if tmpFileName != None:
                            self.defaultBrowseDirOpen =  fd.GetPath()
                            tmpFile = os.path.join(fd.getDirectory(), tmpFileName)
                            if tmpFile.exists() and tmpFile.isDirectory():
                                self.selectedFiles = [None]*1
                                self.selectedFiles[0] = tmpFile
                    else:
                        if self.useXFileDialog() == True:
                            fd.setTitle(title)
                            fd.setDirectory(self.defaultBrowseDirOpen.getAbsolutePath())
                            file_ = fd.GetPath()
                            if file_ != None and file_ != "":
                                self.defaultBrowseDirOpen = fd.GetPath()
                                tmpFile = file_
                                if tmpFile.exists() and tmpFile.isDirectory():
                                    self.selectedFiles = [None]*1
                                    self.selectedFiles[0] = file_
                        else:
                            self.fileChooser.setPreferredSize(self.lastBrowseDimensions)
                            self.fileChooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY)
                            self.fileChooser.setMultiSelectionEnabled(False)
                            self.fileChooser.setCurrentDirectory(self.defaultBrowseDirOpen)
                            self.fileChooser.setSelectedFile(None)
                            if ret == JFileChooser.APPROVE_OPTION:
                                self.selectedFiles = [None]*1
                                self.selectedFiles[0] = self.fileChooser.getSelectedFile()
                                self.defaultBrowseDirOpen = self.fileChooser.getCurrentDirectory()
                                self.defaultBrowseDirOpen = self.fileChooser.getCurrentDirectory()
                                self.lastBrowseDimensions = self.fileChooser.getSize()
                elif type_ == self.BROWSE_TYPE_ONE_FILE_OR_FOLDER:
                    self.fileChooser.setCurrentDirectory(self.defaultBrowseDirOpen)
                    self.fileChooser.setPreferredSize(self.lastBrowseDimensions)
                    self.fileChooser.setFileSelectionMode(JFileChooser.FILES_AND_DIRECTORIES)
                    self.fileChooser.setMultiSelectionEnabled(False)
                    if ret == JFileChooser.APPROVE_OPTION:
                        self.selectedFiles = [None]*1
                        self.selectedFiles[0] = self.fileChooser.getSelectedFile()
                        self.defaultBrowseDirOpen = self.fileChooser.getCurrentDirectory()
                        self.lastBrowseDimensions = self.fileChooser.getSize()
                elif type_ == self.BROWSE_TYPE_MULTIPLE_FILES:
                    if self.useXFileDialog() == Boolean.TRUE:
                        fd.setTitle(title)
                        fd.setDirectory(self.defaultBrowseDirOpen.getAbsolutePath())
                        if files != None and len(files):
                            self.defaultBrowseDirOpen = File(fd.getDirectory())
                            while len(files):
                                tmpFile = os.path.join(self.defaultBrowseDirOpen, files[i])
                                if tmpFile.exists() and tmpFile.isFile() and realFiles.indexOf(tmpFile.getAbsolutePath()) < 0:
                                    realFiles.add(tmpFile.getAbsolutePath())
                                i += 1
                            self.selectedFiles = [None]*len(realFiles)
                            while i < len(realFiles):
                                self.selectedFiles[i] = File(str(realFiles.get(i)))
                                i += 1
                    else:
                        self.fileChooser.setCurrentDirectory(self.defaultBrowseDirOpen)
                        self.fileChooser.setPreferredSize(self.lastBrowseDimensions)
                        self.fileChooser.setFileSelectionMode(JFileChooser.FILES_ONLY)
                        self.fileChooser.setMultiSelectionEnabled(True)
                        self.fileChooser.setDialogType(0)
                        if ret == JFileChooser.APPROVE_OPTION:
                            self.selectedFiles = self.fileChooser.getSelectedFiles()
                            self.defaultBrowseDirOpen = self.fileChooser.getCurrentDirectory()
                            self.lastBrowseDimensions = self.fileChooser.getSize()
                elif type_ == self.BROWSE_TYPE_MULTIPLE_FOLDERS:
                    if self.useXFileDialog() == Boolean.TRUE:
                        fd.setTitle(title)
                        fd.setDirectory(self.defaultBrowseDirOpen.getAbsolutePath())
                        if files != None and len(files):
                            self.defaultBrowseDirOpen = File(fd.getDirectory())
                            while len(files):
                                tmpFile = File(files[i])
                                if tmpFile.exists() and tmpFile.isDirectory() and realFiles.indexOf(tmpFile.getAbsolutePath()) < 0:
                                    realFiles.add(tmpFile.getAbsolutePath())
                                i += 1
                            self.selectedFiles = [None]*len(realFiles)
                            while i < len(realFiles):
                                self.selectedFiles[i] = File(str(realFiles.get(i)))
                                i += 1
                    else:
                        self.fileChooser.setCurrentDirectory(self.defaultBrowseDirOpen)
                        self.fileChooser.setPreferredSize(self.lastBrowseDimensions)
                        self.fileChooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY)
                        self.fileChooser.setMultiSelectionEnabled(True)
                        self.fileChooser.setDialogType(0)
                        if ret == JFileChooser.APPROVE_OPTION:
                            self.selectedFiles = self.fileChooser.getSelectedFiles()
                            self.defaultBrowseDirOpen = self.fileChooser.getCurrentDirectory()
                            self.lastBrowseDimensions = self.fileChooser.getSize()
                elif type_ == self.BROWSE_TYPE_MULTIPLE_FILES_OR_FOLDERS:
                    self.fileChooser.setCurrentDirectory(self.defaultBrowseDirOpen)
                    self.fileChooser.setPreferredSize(self.lastBrowseDimensions)
                    self.fileChooser.setFileSelectionMode(JFileChooser.FILES_AND_DIRECTORIES)
                    self.fileChooser.setMultiSelectionEnabled(True)
                    self.fileChooser.setDialogType(0)
                    if ret == JFileChooser.APPROVE_OPTION:
                        self.selectedFiles = self.fileChooser.getSelectedFiles()
                        self.defaultBrowseDirOpen = self.fileChooser.getCurrentDirectory()
                        self.lastBrowseDimensions = self.fileChooser.getSize()
                self.hasFilesInSelection = (self.hasFilesInSelection() and len(length))
                self.existingDirectorySelected = self.selectedFiles[0].isDirectory() and len(length) and self.selectedFiles[0].exists()
            except Exception as e:
                print e.getMessage()
                self.selectedFiles = []
                self.selectedFilesInfo = None
            return self.selectedFiles

    #@browseForUpload.register(object, int, str)
        def browseForUpload_0(self, type_, title):
            """ generated source for method browseForUpload_0 """
            return self.browseForUpload(type_, title, "", "")
    
        def browseForDownload(self, type_, title, defaultFile, filterExtension, filterTitle):
            """ generated source for method browseForDownload """
            self.selectedFiles = []
            self.selectedFilesInfo = None
            self.hasFilesInSelection = False
            tmpFile = ""
            tmpFileName = str()
            if self.defaultBrowseDir == None or not self.defaultBrowseDir.exists():
                self.defaultBrowseDir = fv.getDefaultDirectory()
            if self.defaultBrowseDirSave == None or not self.defaultBrowseDirSave.exists():
                self.defaultBrowseDirSave = self.defaultBrowseDir
            if title == None or title == "":
                title = "Save"
            if defaultFile == None:
                defaultFile = ""
            if filterExtension == None:
                filterExtension = ""
            if filterTitle == None:
                filterTitle = ""
            try:
                if type_ == self.BROWSE_TYPE_ONE_FILE:
                    if OS.isMac():
                        System.setProperty("apple.awt.fileDialogForDirectories", "false")
                    fd.setDirectory(self.defaultBrowseDirSave.getAbsolutePath())
                    if not defaultFile == "":
                        fd.setFile(defaultFile)
                    if not filterExtension == "":
                        if not OS.isWindows():
                            self.ext = ext.lower().split("\\|")
                            name = name.lower()
                            if name.endsWith("." + self.ext[0]) and len(length):
                                return True
                            while len(length):
                                if name.endsWith("." + self.ext[i]):
                                    return True
                                i += 1
                            return False
                            fd.setFilenameFilter(filter(filterExtension))
                        elif defaultFile == None and defaultFile == "":
                            if len(ext):
                                fd.setFile("*." + ext[0])
                    fd.setModal(True)
                    fd.setVisible(True)
                    tmpFileName = fd.getFile()
                    if tmpFileName != None:
                        self.defaultBrowseDirSave = File(fd.getDirectory())
                        self.selectedFiles = [None]*1
                        self.selectedFiles[0] = File(fd.getDirectory(), tmpFileName)
                elif type_ == self.BROWSE_TYPE_ONE_FOLDER:
                    if OS.isMac():
                        System.setProperty("apple.awt.fileDialogForDirectories", "true")
                        fd.setDirectory(self.defaultBrowseDirSave.getAbsolutePath())
                        fd.setModal(True)
                        fd.setVisible(True)
                        tmpFileName = fd.getFile()
                        if tmpFileName != None:
                            self.defaultBrowseDirSave = File(fd.getDirectory())
                            self.selectedFiles = [None]*1
                            self.selectedFiles[0] = File(fd.getDirectory(), tmpFileName)
                    else:
                        if self.useXFileDialog() == Boolean.TRUE:
                            fd.setTitle(title)
                            fd.setDirectory(self.defaultBrowseDirSave.getAbsolutePath())
                            if file_ != None and file_ != "":
                                self.defaultBrowseDirSave = File(fd.getDirectory())
                                self.selectedFiles = [None]*1
                                self.selectedFiles[0] = File(file_)
                        else:
                            self.fileChooser.setPreferredSize(self.lastBrowseDimensions)
                            self.fileChooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY)
                            self.fileChooser.setMultiSelectionEnabled(False)
                            self.fileChooser.setCurrentDirectory(self.defaultBrowseDirSave)
                            self.fileChooser.setSelectedFile(None)
                            if ret == JFileChooser.APPROVE_OPTION:
                                self.selectedFiles = [None]*1
                                self.selectedFiles[0] = self.fileChooser.getSelectedFile()
                                self.defaultBrowseDirSave = self.fileChooser.getCurrentDirectory()
                                self.lastBrowseDimensions = self.fileChooser.getSize()
            except Exception as e:
                print e.getMessage()
                self.selectedFiles = []
                self.selectedFilesInfo = None
            return self.selectedFiles
