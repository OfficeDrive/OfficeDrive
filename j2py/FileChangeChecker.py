#!/usr/bin/env python
""" generated source for module FileChangeChecker """
import io
import OfficeDrive_SE6
from threading import  Thread

class FileChangeChecker(Thread):
    """ generated source for class FileChangeChecker """
    #app = OfficeDrive_SE6()

    def __init__(self, officeDriveSE5):
        """ generated source for method __init__ """
        super(FileChangeChecker, self).__init__()
        self.app = officeDriveSE5

    def dmsId(self):
        """ generated source for method dmsId """
        return self.app.dmsId()

    def userId(self):
        """ generated source for method userId """
        return self.app.userId()

    # @Override
    def run(self):
        """ generated source for method run """
        s = File.separator
        myTempFolder = self.app.tempFolder + s + self.dmsId()
        myAppFolder = self.app.appFolder + s + self.dmsId()
        openDir = File(myTempFolder + s + "open_" + self.userId())
        name = str()
        newName = str()
        baseName = str()
        ext = str()
        newExt = str()
        itemId = str()
        currentMd5 = str()
        cacheMd5 = str()
        n = str()
        uploadContentType = ""
        storedMtime = long()
        currentMtime = long()
        file_ = File()
        dir = File()
        tmp = File()
        tmp2 = File()
        delta = File()
        upload = None
        files = []
        in_ = FileInputStream()
        out = FileOutputStream()
        uploadSuccess = bool()
        uploadRet = HashMap()
        uploadErrorCount = 0
        tmpFileSize = long()
        if not openDir.isDirectory():
            return
        while True:
            try:
                Thread.sleep(1000)
            except InterruptedException as e:
                Thread.currentThread().interrupt()
                return
            if openDir.isDirectory() == False:
                continue 
            files = openDir.listFiles()
            while len(files):
                dir = files[i]
                if dir.isDirectory():
                    itemId = dir.__name__
                    newName = ""
                    newExt = ""
                    #  load info
                    if openInfo == None or openInfo.isEmpty():
                        if dir.lastModified() < System.currentTimeMillis() - 1000 * 60 * 60:
                            print "no open file info found for " + itemId
                            self.app.deleteOpenItem(itemId)
                            if dir.exists():
                                dir.setLastModified(System.currentTimeMillis())
                        continue 
                    if cacheInfo == None or cacheInfo.isEmpty():
                        print "no cache info found for " + itemId
                        self.app.deleteOpenItem(itemId)
                        continue 
                    storedMtime = Long.parseLong(openInfo.get("mtime") + "")
                    name = str(openInfo.get("name"))
                    baseName = name.substring(0, name.lastIndexOf(".")) if name.lastIndexOf(".") > -1 else name
                    ext = name.substring(name.lastIndexOf(".") + 1, len(name)) if name.lastIndexOf(".") > -1 else ""
                    file_ = File(myTempFolder + s + "open_" + self.userId() + s + itemId + s + name)
                    if not ext == "" and File(file_.getAbsolutePath() + "x").exists():
                        #  file name has changed to docx, xlsx, enz
                        newName = name + "x"
                        newExt = newName.substring(newName.lastIndexOf(".") + 1, len(newName))
                    if not newExt == "" and not newExt == ext and (not openInfo.containsKey("readOnly") or not openInfo.get("readOnly") == "true"):
                        #  file extension has changed on writable document
                        self.app.getTransponderLine("action=alterItemExtension&itemId=" + itemId + "&ext=" + newExt)
                    if not newName == "" and not newName == name:
                        #  name has changed
                        openInfo.put("name", newName)
                        FileActions.saveHashMap(openInfo, myTempFolder + s + "open_" + self.userId() + s + itemId + ".json")
                        file_ = File(myTempFolder + s + "open_" + self.userId() + s + itemId + s + newName)
                        name = newName
                    if not file_.exists():
                        continue 
                    if not openInfo.containsKey("readOnly") or not openInfo.get("readOnly") == "true":
                        #  lock or refresh lock if autoLocking is on and item is not read-only
                        if openInfo.containsKey("expectFileLock") and not openInfo.get("expectFileLock") == "no":
                            fileIsLocked = FileActions.isLockedByFileSystem(file_) if openInfo.get("expectFileLock") == "fileSystem" else FileActions.isLockedByTmpFile(file_)
                            #  files that are locked by the client when opened
                            if fileIsLocked and (lock == None or not lock.containsKey("userId") or not lock.get("userId") == self.userId() or Long.parseLong(lock.get("stamp") + "") < System.currentTimeMillis() - 4 * 60 * 1000):
                                #  lock item if not locked or not locked by me or lock is old
                                self.app.lockItem(itemId)
                            elif not fileIsLocked and lock != None and lock.containsKey("userId") and lock.get("userId") == self.userId():
                                #  unlock if file is not locked and current lock is mine
                                self.app.unlockItem(itemId)
                                deleteItem = True
                        elif (not openInfo.containsKey("expectFileLock") or not openInfo.get("expectFileLock") == "tmpFile") and FileActions.isLockedByTmpFile(file_):
                            print "update track file locking by temp file"
                            openInfo.put("expectFileLock", "tmpFile")
                            FileActions.saveHashMap(openInfo, myTempFolder + s + "open_" + self.userId() + s + itemId + ".json")
                    if openInfo.containsKey("readOnly") and openInfo.get("readOnly") == "true" and openInfo.containsKey("expectFileLock") and not openInfo.get("expectFileLock") == "no":
                        #  read only docs can alsow be deleted when lock is lifted
                        fileIsLocked = FileActions.isLockedByFileSystem(file_) if openInfo.get("expectFileLock") == "fileSystem" else FileActions.isLockedByTmpFile(file_)
                        if not fileIsLocked:
                            deleteItem = True
                    #  check if file is changed
                    currentMtime = file_.lastModified()
                    if file_.exists() and currentMtime > storedMtime:
                        try:
                            #  check if file is in rest
                            tmpFileSize = len(file_)
                            Thread.sleep(200)
                            if tmpFileSize == len(file_) and file_.lastModified() == currentMtime:
                                #  copy current file
                                tmp = FileActions.copy(file_)
                                currentMd5 = FileActions.MD5(tmp)
                                cacheMd5 = str(cacheInfo.get("md5"))
                                if not currentMd5 == cacheMd5:
                                    #  file change found
                                    if openInfo.containsKey("readOnly") and openInfo.get("readOnly") == "true":
                                        #  read only
                                        self.app.evalJs("window['" + self.app.jsObj + "'].notifieReadOnlyFileChange(" + itemId + " , '" + cacheInfo.get("name") + "')")
                                        self.app.getTransponderLine("action=notifyEditOnReadOnly&itemId=" + itemId)
                                        #  update open info
                                        # openInfo.put("md5", currentMd5);
                                        openInfo.put("mtime", currentMtime + "")
                                        FileActions.saveHashMap(openInfo, myTempFolder + s + "open_" + self.userId() + s + itemId + ".json")
                                    else:
                                        #  save change
                                        uploadSuccess = False
                                        self.app.saving = True
                                        self.app.resetProgress()
                                        if self.app.language == "nl":
                                            self.app.progressDescription = "upload veranderingen in " + cacheInfo.get("name")
                                        else:
                                            self.app.progressDescription = "uploading changes in " + cacheInfo.get("name")
                                        self.app.evalJs("window['" + self.app.jsObj + "'].notifieAutoUploadStart(" + itemId + " , '" + cacheInfo.get("name").__str__().replaceAll("'", "") + "')")
                                        if not uploadSuccess:
                                            n = file_.__name__
                                            if 1024 < len(tmp) or n.endsWith(".zip") or n.endsWith(".gz") or n.endsWith(".rar") or n.endsWith(".jar") or n.endsWith(".bz2") or n.endsWith(".gif") or n.endsWith(".png") or n.endsWith(".jpg") or n.endsWith(".jpeg") or n.endsWith(".tif") or n.endsWith(".tiff") or n.endsWith(".psd") or n.endsWith(".ai") or n.endsWith(".gz") or n.endsWith(".tgz") or n.endsWith(".mp3") or n.endsWith(".mpeg") or n.endsWith(".wav") or n.endsWith(".mp4") or n.endsWith(".m4a") or n.endsWith(".m4p") or n.endsWith(".avi") or n.endsWith(".fla") or n.endsWith(".flv") or n.endsWith(".exe") or n.endsWith(".xlsx") or n.endsWith(".docx") or n.endsWith(".pptx") or n.endsWith(".wma") or n.endsWith(".wmv"):
                                                upload = tmp
                                                uploadContentType = ""
                                            else:
                                                upload = FileActions.gzip(tmp)
                                                uploadContentType = "gzip"
                                            self.app.cancel = False
                                            self.app.progressDone = 0
                                            self.app.progressTotal = float(len(upload)) / 1024
                                            if uploadContentType == "gzip":
                                                print "upload gzip for " + file_.__name__ + " - " + OfficeDrive_SE6.bitesToStr(len(upload)) + " = " + Math.round(float(len(upload)) / len(tmp) * 100) + "% of origional..."
                                            else:
                                                print "upload " + file_.__name__ + " - " + OfficeDrive_SE6.bitesToStr(len(upload)) + "..."
                                            if self.app.language == "nl":
                                                self.app.progressDescription = "upload " + cacheInfo.get("name")
                                            else:
                                                self.app.progressDescription = "uploading " + cacheInfo.get("name")
                                            uploadSuccess = self.app.doFilePut(upload, self.app.transponderUrl() + "?holder-type=java&sid=" + self.app.sid() + "&dmsId=" + self.dmsId() + "&action=updateItem&userMethod=autosave&itemId=" + itemId + "&contentType=" + uploadContentType + "&sourceMd5=" + cacheMd5 + "&targetMd5=" + currentMd5)
                                            if not uploadSuccess and uploadRet.get("status") == "canceled":
                                                if tmp.exists():
                                                    tmp.delete()
                                                if upload.exists():
                                                    upload.delete()
                                                print "       > canceled"
                                                print "cancel auto save"
                                                openInfo.put("md5", currentMd5)
                                                openInfo.put("mtime", currentMtime + "")
                                                FileActions.saveHashMap(openInfo, myTempFolder + s + "open_" + self.userId() + s + itemId + ".json")
                                                continue 
                                        if not uploadSuccess:
                                            if tmp.exists():
                                                tmp.delete()
                                            if upload.exists():
                                                upload.delete()
                                            uploadErrorCount += 1
                                            if uploadErrorCount > 2:
                                                print "        > failed and quitting"
                                                self.app.evalJs("window['" + self.app.jsObj + "'].notifieAutoUploadEnd(false)")
                                                self.app.progressDescription = "failed"
                                                System.exit(1)
                                            else:
                                                print "        > failed and retrying"
                                                Thread.sleep(2 * 1000)
                                        else:
                                            uploadErrorCount = 0
                                            print "        > completed"
                                            if Math.round(self.app.progressDone) < 1:
                                                self.app.progressTotal = self.app.progressDone = 1
                                            if self.app.language == "nl":
                                                self.app.progressDescription = "gereed"
                                            else:
                                                self.app.progressDescription = "done"
                                            self.app.evalJs("window['" + self.app.jsObj + "'].notifieAutoUploadEnd(true)")
                                            if self.app.maxEncryptionFileSize < len(tmp):
                                                cacheInfo.put("encrypted", "true")
                                                self.app.encrypter().encrypt(tmp, File(myAppFolder + s + "cache" + s + itemId))
                                                tmp.delete()
                                            else:
                                                cacheInfo.put("encrypted", "false")
                                                FileActions.move(tmp, File(myAppFolder + s + "cache" + s + itemId))
                                            cacheInfo.put("md5", currentMd5)
                                            cacheInfo.put("mtime", currentMtime + "")
                                            if not newExt == "" and cacheInfo.containsKey("name"):
                                                cacheInfo.put("name", cacheInfo.get("name").__str__().substring(0, cacheInfo.get("name").__str__().lastIndexOf(".")) + "." + newExt)
                                            FileActions.saveHashMap(cacheInfo, myAppFolder + s + "cache" + s + itemId + ".json")
                                            openInfo.put("md5", currentMd5)
                                            openInfo.put("mtime", currentMtime + "")
                                            FileActions.saveHashMap(openInfo, myTempFolder + s + "open_" + self.userId() + s + itemId + ".json")
                                            if upload.exists():
                                                upload.delete()
                                        self.app.saving = False
                                else:
                                    openInfo.put("mtime", currentMtime + "")
                                    FileActions.saveHashMap(openInfo, myTempFolder + s + "open_" + self.userId() + s + itemId + ".json")
                                    tmp.delete()
                        except Exception as e:
                            print e.getMessage()
                    if deleteItem:
                        self.app.deleteOpenItem(itemId)
                i += 1

