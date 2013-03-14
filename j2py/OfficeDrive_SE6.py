#!/usr/bin/env python
""" generated source for module OfficeDrive_SE6 """

import os
import sys

appdir = "C:\\Users\\simon\\My Documents\\Aptana Studio 3 Workspace\\OfficeDrive_Daemon"
sys.path.append(os.path.join(appdir))

import time
import io
import subprocess
import ctypes
import json
import wx
import urllib2
import urllib
import socket

from threading import Thread

from j2py import UploadFilesTree
from j2py import DesEncrypter
from j2py.OS import OS
from j2py import FileChangeChecker
from j2py import Browser
from j2py.FileActions import FileActions

class FileChooser(wx.FileDialog):
    pass

class JSObject(object):
    def getWindow(self):
        pass
    
    def eval(self, code):
        pass
    pass
    
class OfficeDrive_SE6():
    """ generated source for class OfficeDrive_SE6 """
    serialVersionUID = 5661817414202376045L
    javaVersion = "1.6"
    tempFolder = str()
    appFolder = str()
    appRootFolder = str()
    s = str()
    commandChecker = CommandChecker()
    cmds = []
    encryptorKey = None
    encrypter = DesEncrypter()
    maxEncryptionFileSize = 1024 * 1024 * 3
    fileChecker = Thread()
    jsObj = str()
    selectedFiles = []
    selectedFilesInfo = None
    hasFilesInSelection = False
    existingDirectorySelected = False
    BROWSE_TYPE_ONE_FILE = 1
    BROWSE_TYPE_ONE_FILE_OR_FOLDER = 2
    BROWSE_TYPE_MULTIPLE_FILES = 3
    BROWSE_TYPE_MULTIPLE_FOLDERS = 4
    BROWSE_TYPE_ONE_FOLDER = 5
    BROWSE_TYPE_MULTIPLE_FILES_OR_FOLDERS = 6
    progressTotal = 0
    progressDone = 0
    progressDescription = ""
    error = str()
    execContent = ""
    uploadBufferSize = 15 * 1024
    uploadInfo = {}
    downloadInfo = {}
    cancel = False
    starting = False
    started = False
    busy = False
    alive = False
    saving = False
    dmsInfo = {}
    dmsId = ""
    userId = ""
    userIsWheel = False
    hostName = ""
    uniqueUserId = ""
    maxUploadMb = 1024 * 1024 * 1024
    rootUrl = str()
    transponderUrl = str()
    sid = str()
    # useNaiveSSL = false;
    cookie = str()
    browser = Browser()
    # _useXdelta = null;
    _useXFileDialog = None
    xFileDialogLibrary = str()
    xDelta3Exe = ""
    windowsStartupJar = "netuse.startup.1.2.jar"
    sleeperJar = "sleeper.1.0.jar"
    settings = {}
    language = str()
    locks = {}
    fileChooser = FileChooser()
    myNetUseLetter = str()
    netUseLetters = {}
    currentNetUseLetter = ""
    currentNetUseIsPersistent = False
    currentMountNode = ""
    currentMountIsPersistent = False

    def encrypter(self):
        """ generated source for method encrypter """
        return self.encrypter
    
    def dmsId(self):
        """ generated source for method dmsId """
        return self.dmsId

    def userId(self):
        """ generated source for method userId """
        return self.userId
    
    def transponderUrl(self):
        """ generated source for method transponderUrl """
        return self.transponderUrl

    def sid(self):
        """ generated source for method sid """
        return self.sid
    
    def start(self):
        """ generated source for method start """
        tryCount = 0
        while not self.starting and tryCount < 3:
            print "start OfficeDrive.6 #" + tryCount
            # print "start "+this.__class__.__name__+" #"+tryCount;
            try:
                self._start()
            except Exception as e:
                e.printStackTrace()
                print "waiting 2 seconds to retry starting applet..."
                try:
                    time.sleep(2)
                    #*se* time.sleep(2)
                except (Exception) as ee:
                    ee.printStackTrace()

    def _start(self):
        """ generated source for method _start """
        self.starting = True
        #  create or get permanent temp folder
        #*se* self.s = File.separator
        self.s = os.pathsep
        #version = System.getProperty("java.version")
        #print "Java Runtime version: " + version
        
        print "OS: " + OS.description()
        
        #  parameters
        self.jsObj = self.getParam("jsObj")
        browserjson = self.getParam("browserjson")
        if browserjson != None and not browserjson == "":
            self.browser = Browser(json.loads(browserjson))
        cb = self.getCodeBase()
        self.rootUrl = cb.getProtocol() + "://" + cb.getHost() + (":" + cb.getPort() if cb.getPort() > -1 else "") + self.getParam("rootFolder")
        self.transponderUrl = self.rootUrl + "/transponder.php"
        print self.rootUrl
        #  test permission
        try:
            FileActions.setContents(self.testFile, "permission test")
            self.testFile.delete()
        except Exception as e:
            try:
                print "... waining 2 seconds to retry permission test"
                time.sleep(2)
                FileActions.setContents(self.testFile, "permission test")
                os.remove(self.testFile)
            except (Exception) as ee:
                ee.printStackTrace()
                print "Security level to low. Java is stopped"
                self.evalJs("window['" + self.jsObj + "'].permissionFailure()")
                return
        #  check connection
        contact = False
        if cb.getProtocol() == "https":
            try:
                contact = self.doFilePut("connection test", self.transponderUrl + "?action=test")
                print "use verified SSL"
            except Exception as e:
                pass
            if not contact:
                # 				useNaiveSSL = true;
                # 				try{
                # 					// Install the all-trusting trust manager
                # 					TrustManager[] trustAllCerts = new TrustManager[]{
                # 						new X509TrustManager(){
                # 							public java.security.cert.X509Certificate[] getAcceptedIssuers() {
                # 								return null;
                # 							}
                # 							public void checkClientTrusted(java.security.cert.X509Certificate[] certs, String authType){}
                # 							public void checkServerTrusted(java.security.cert.X509Certificate[] certs, String authType){}
                # 						}
                # 					};
                # 					SSLContext sc = SSLContext.getInstance("SSL");
                # 					sc.init(null, trustAllCerts, new java.security.SecureRandom());
                # 					HttpsURLConnection.setDefaultSSLSocketFactory(sc.getSocketFactory() );
                # 					
                # 					contact = doFilePut("hello world!", transponderUrl+"?action=test");
                # 					if(contact) print "use naive SSL";
                # 				}
                # 				catch(Exception e){}
                # 				
                # 				if(!contact){
                # 					transponderUrl = transponderUrl.replaceAll("^https", "http");
                # 					try{
                # 						contact = doFilePut("hello world!", transponderUrl+"?action=test");
                # 						print "use non SSL!";
                # 					}
                # 					catch(Exception e){}
                # 					if(!contact){
                print "no contact possible with transponder"
                return
                # 					}
                # 				}
        else:
            try:
                contact = self.doFilePut("hello world!", self.transponderUrl + "?action=test")
                print "contact to server tested"
            except Exception as e:
                pass
            if not contact:
                print "no contact possible with transponder"
                return
        self.sid = self.getParam("sid")
        self.cookie = self.getParam("cookie")
        self.language = self.getParam("language")
        if not self.getParam("maxUploadMb") == "":
            self.maxUploadMb = long(self.getParam("maxUploadSize"))
            if self.maxUploadMb < 1024:
                self.maxUploadMb = 1024
        if not self.getDmsInfo() or self.dmsId == "" or self.dmsId == None:
            self.evalJs("window['" + self.jsObj + "'].connectionFailure()")
            print "dmsId not found"
            return
        try:
            self.createLocalFolders()
        except (IOError) as e:
            e.printStackTrace()
            print "error: " + e.getMessage()
            return
        self.settings = json.load(os.path.join(self.appFolder, "settings.json"))
        if self.encryptorKey == None:
            self.encryptorKey = self.getTransponderContent("action=getDESKey").trim()
            if self.encryptorKey == "":
                print "could not get key"
                return
        self.encrypter = DesEncrypter(self.encryptorKey)
       
        self.fileChooser = FileChooser() 
        self.fileChooser.DragAcceptFiles(True)
        self.fileChooser.ShowModal(True)
        self.fileChooser.CanDoLayoutAdaptation(True)
        self.fileChooser.CenterOnParent(True)
            
        if sys.platform.startswith("linux"):
            self.fileChooser.SetPath(os.environ.get("HOME", "/home"))
        
        if sys.platform == "win32":
            self.fileChooser.SetPath(os.environ.get("USERPROFILE", "."))
            netUseInfo = json.load(os.path.join(self.appRootFolder, "netuse", self.uniqueUserId))
            if self.netUseInfo != None and netUseInfo.has_key("letter"):
                self.myNetUseLetter = netUseInfo.get("letter").__str__().toUpperCase()
                if not self.myNetUseLetter.matches("^[D-Z]$"):
                    self.myNetUseLetter = ""
                if not self.myNetUseLetter == "":
                    if netUseInfo.has_key("persistent") and netUseInfo.get("persistent") == "true":
                        self.currentNetUseIsPersistent = True
                        if not self.execCommand("net use " + self.myNetUseLetter + ":"):
                            self._createNetUse(self.myNetUseLetter, True)
                        elif self.execContent.index("\\webdav") > -1:
                            print "reconnected to persistent net use " + self.myNetUseLetter + ":"
                            self.currentNetUseLetter = self.myNetUseLetter
                    elif self.execCommand("net use " + self.myNetUseLetter + ":") and self.execContent.index("\\webdav") > -1:
                        print "reconnected to net use " + self.myNetUseLetter + ":"
                        self.currentNetUseLetter = self.myNetUseLetter
                    if not self.currentNetUseLetter == "" and self.currentNetUseIsPersistent:
                        print "this._resetStartupLink()"
                        self._resetStartupLink()
                    self.netUseLetters = self._getNetUseLetters()
                    
        if sys.platform == "mac":
            self.fileChooser.MacGetTopLevelWindowRef()
            self.fileChooser.MacGetMetalAppearance()
            self.fileChooser.MacGetUnifiedAppearance()
            
            mountInfo = dict(json.load(os.path.join(self.appFolder, self.dmsId, "mount_%s.jsoin" %self.userId)))
            
            if not mountInfo:
                sys.stdout.write("no mount into found.\n")
            if mountInfo and mountInfo.has_key("node"):
                mountNode = mountInfo["node"]
                if os.path.exists(mountNode):
                    sys.stdout.write("reconnect to existing mount: %s\n" %mountNode)
                    if mountInfo.has_key("persistent"):
                        self.currentMountIsPersistent = mountInfo.get("persistent", False) 
                    self.currentMountNode = mountNode.__str__()
                elif mountInfo.has_key("persistent") and self.currentMountIsPersistent:
                    sys.stdout.write("recreate persistent mount\n")
                    self._createMount(True)
        self.evalJs("window['" + self.jsObj + "'].onload('" + self.version + "')")
        if not self.currentNetUseLetter == "":
            self.evalJs("window['" + self.jsObj + "'].netUseOnload()")
        try:
            self.fileChecker = Thread(target=FileChangeChecker.FileChangeChecker)
            self.fileChecker.setDaemon(True)
            self.fileChecker.start()
        except (IOError) as e:
            e.printStackTrace()
            print "error: " + e.getMessage()
        try:
            self.commandChecker = self.CommandChecker(self)
            self.commandChecker.start()
        except (IOError) as e:
            e.printStackTrace()
            sys.stdout.write("error: %s\n" + e)
        self.alive = True
        self.started = True

    def getDmsInfo(self):
        """ generated source for method getDmsInfo """
        
        jsonString = self.getTransponderLine("action=getDmsInfo&javaVersion=%s" %self.javaVersion)
        
        if not jsonString.startsWith("{"):
            sys.stdout.write("dms info not found. JSON: %s\n" %jsonString)
            return False
        info = dict(json.loads(jsonString))
        if not info or not info.has_key("dmsId"):
            sys.stdout.write("dms info not found in JSON: %s\n" %jsonString)
            return False
        self.dmsId = info.get("dmsId")
        self.userId = info.get("userId")
        if info.has_key("hostName") and not info.get("hostName", None):
            self.hostName = info.get("hostName")
        self.uniqueUserId = ("" if self.hostName == "" else self.hostName + ".") + self.dmsId + "." + self.userId
        self.userIsWheel = True if info.has_key("wheel") and info.get("wheel") == "true" else False
        if info.has_key("DESKey") and not info.get("DESKey") == "":
            self.encryptorKey = str(info.get("DESKey"))
            info.remove("DESKey")
        self.dmsInfo = info
        return True

    def createLocalFolders(self):
        """ generated source for method createLocalFolders """
        pathbase = os.environ.get("TEMP", os.environ.get("TMP", "."))
        path = os.path.join(pathbase, "OfficeDrive")
        if not self.hostName == "":
            path = os.path.join(path, self.hostName)
        dir_ = os.path.abspath(path)
        if not os.path.exists(path) and not os.mkdir(dir_):
            sys.stdout.write("could not create %s\n" % path)
        self.tempFolder = path
        path = FileActions.getWorkingDirectory("OfficeDrive")
        self.appRootFolder = path
        if OS.isWindows():
            dir_ = os.path.join(self.appRootFolder, "netuse")
            if not dir.isDirectory():
                dir.mkdir()
        if not self.hostName == "":
            path = path, self.hostName
        dir_ = os.path.abspath(path)
        if not os.path.isdir(dir_):
            os.mkdir(dir_)
        self.appFolder = path
        dir_ = os.path.join(self.tempFolder, self.dmsId)
        if not os.path.isdir(dir_):
            os.mkdir(dir_)
        dir_ = os.path.join(self.appFolder, self.dmsId)
        if not os.path.isdir(dir_):
            os.mkdir(dir_)
        dir_ = os.path.join(self.appFolder,self.dmsId, "cache")
        if not os.path.isdir(dir_):
            os.mkdir(dir_)
        dir_ = os.path.join(self.tempFolder, self.dmsId, "open_%s" %self.userId)
        if not os.path.isdir(dir_):
            os.mkdir(dir_)
        if self.appFolder == self.tempFolder:
            sys.stdout.write("application and temp data in: %s\n" %os.path.join(self.appFolder, self.dmsId))
        else:
            sys.stdout.write("application data in: %s\n"  %os.path.join(self.appFolder, self.dmsId))
            sys.stdout.write("temp data in: %s\n" %os.path.join(self.tempFolder, self.dmsId))

    def useXFileDialog(self):
        """ generated source for method useXFileDialog """
        if self._useXFileDialog != None:
            return self._useXFileDialog
        elif not OS.isWindows():
            self._useXFileDialog = False
            return self._useXFileDialog
        
        self._useXFileDialog = True
        
        self.xFileDialogLibrary = "xfiledialog64.0.63.dll" if OS.is64bits() else "xfiledialog.0.63.dll"
        xfiledialog = os.path.join(self.appFolder, self.xFileDialogLibrary)
        if not xfiledialog.exists():
            FileActions.downloadUrlToFile(self.rootUrl + "/" + self.xFileDialogLibrary, xfiledialog)
        xFileDialogFile = os.path.join(self.appFolder, self.xFileDialogLibrary)
        if os.path.isfile(xfiledialog):
            try:
                os.system(os.path.abspath(xFileDialogFile))
                sys.stdout.write("file dialog plugin %s loaded\n" %xFileDialogFile)
                self.XFileDialog.nativeEnabled = True
                self._useXFileDialog = True
            except (Exception) as e:
                sys.stdout.write("Exception: %s\n" %e)
            
            libraries = []
            for lib in libraries:
                if lib.endsWith(self.xFileDialogLibrary):
                    print self.xFileDialogLibrary + " found"
                    break
                
            if self.xFileDialogDllLoaded:
                self.XFileDialog.nativeEnabled = True
                self._useXFileDialog = True
            else:
                self.XFileDialog.nativeEnabled = False
                self._useXFileDialog = True
            self.XFileDialog.initOnce = True
        return self._useXFileDialog

    def useXdelta(self):
        """ generated source for method useXdelta """
        return False

    def evalJs(self, code_):
        """ generated source for method evalJs """
        try:
            window = JSObject.getWindow(self);
            window.eval(code_)
        except (Exception) as e:
            sys.stdout.write("Exception: %s\nCould not use window.eval(%s)\n" %(e, code_))
            if not self.browser.isIE():
                try:
                    self.getAppletContext().showDocument(("javascript:" + code_).toURL())
                except Exception as ee:
                    sys.stdout.write("Exception: %s\nCould not use showDocument('javascript:%s\n" %(ee, code_) )
                    try:
                        self.getAppletContext().showDocument("%s/js.eval.html?%s" %(self.rootUrl, code_).toURL(), "%s_jsEvalFrame" %self.jsObj)
                    except Exception as eee:
                        sys.stdout.write("%s\nCould not use showDocument(%s/js.eval.html?%s\n" %(eee, self.rootUrl, code_))
                        sys.stdout.write("Given up to eval javascript.\n")
            else:
                try:
                    self.getAppletContext().showDocument("%s/js.eval.html?%s" %(self.rootUrl,code_).toURL(), "%s_jsEvalFrame" %self.jsObj)
                except Exception as ee:
                    sys.stdout.write("Exception: %s\nCould not use showDocument(%s/js.eval.html?%s\n" %(ee, self.rootUrl, code_ ))
                    sys.stdout.write("Given up to eval javascript.\n")

    def getTransponderContent(self, urlAttributes):
        """ generated source for method getTransponderContent """
        try:
            url = self.transponderUrl+"?holder-type=java&sid=" + self.sid + "&dmsId=" + self.dmsId +"&" + self.urlAttributes

            req = urllib2.Request(url, "GET")
            req.add_header("Cookie", self.cookie)
            conn = urllib2.urlopen(req)
            
            if conn.code < 0:
                sys.stdout.write("... waining 2 seconds to retry: %s\n" %url)
                conn.close()
                time.sleep(2)
                conn = urllib2.urlopen(req)
                if conn.code < 0:
                    self.error = "connection failed"
                    sys.stdout.write(conn.read())
                    self.evalJs("window['" + self.jsObj + "'].connectionFailure()")
                    return None
            
            if conn.code == 304:
                self.error = "session failed"
                sys.stdout(self.error)
                self.evalJs("window['" + self.jsObj + "'].sessionFailure()")
                return None
            
            if conn.code / 100 != 2:
                self.error = conn.read()
                sys.stdout.write(self.error)
                self.evalJs("window['" + self.jsObj + "'].connectionFailure()")
                return None
            
            lines = []
            for line in conn.readlines():
                lines.append(line)
                
            conn.close()
            content = str()
            for line in lines:
                content += "%s\n" %line
            return content
        
        except (urllib2.HTTPError) as e:
            try:
                self.evalJs("window['" + self.jsObj + "'].connectionTimeout()")
            except:
                pass
            finally: return ""
        except (Exception) as e:
            sys.stdout.write("getTransponderLines failed: %s\n" %e)
            return ""

    def getTransponderLine(self, urlAttributes):
        """ generated source for method getTransponderLine """
        content = self.getTransponderLines(urlAttributes)
        if content == None or len(content) < 1:
            return ""
        else:
            return content.get(0).__str__()

    def getTransponderLines(self, urlAttributes):
        """ generated source for method getTransponderLines """
        content = self.getTransponderContent(urlAttributes)
        if content == None or content == "":
            return None
        list_ = []
        lines = content.split("\n")
        i = 0
        while len(lines):
            if lines[i] != None and not lines[i].trim() == "":
                list_.add(lines[i].trim())
            i += 1
        return list_

    def getParam(self, name):
        """ generated source for method getParam """
        val = self.getParameter(name)
        if val == None:
            return ""
        else:
            return val

    def getItemInfo(self, itemId):
        """ generated source for method getItemInfo """
        jsonString = self.getTransponderLine("action=getItemInfo&itemId=" + itemId)
        if not jsonString or not jsonString.startsWith("{"):
            sys.stdout.write("invalid item info on item %s\n" %itemId)
            sys.stdout.write(jsonString)
            return None
        info = dict(json.loads(jsonString))
        return info

    def getCacheInfo(self, itemId):
        """ generated source for method getCacheInfo """
        infoFile = os.path.join(self.appFolder, self.dmsId, "cache", itemId, ".json")
        if not os.path.exists(infoFile):
            return None
        info = dict(json.load(infoFile))
        
        if info and not info.has_key("encrypted"):
            info["encrypted"] = True
        return info

    def downloadItemToCashe(self, itemId):
        """ generated source for method downloadItemToCashe """
        phrases = []
        phrases.append("downloading")
        phrases.append("download $1")
        phrases.append("saving file")
        phrases.append("server is processing data")
        tr(phrases)
        try:
            remoteInfo = dict(self.getItemInfo(itemId))
            if not remoteInfo:
                return False

            cacheFile = os.path.join(self.appFolder, self.dmsId, "cache", itemId)

            if os.path.exists(cacheFile):
                cacheInfo = self.getCacheInfo(itemId)
                if cacheInfo and cacheInfo.has_key("md5"):
                    localMd5 = str(cacheInfo.get("md5"))
                    if not localMd5 == "":
                        if remoteInfo.has_key("md5") and remoteInfo.get("md5", "") == localMd5:
                            cacheFile.setLastModified(time.ctime())
                            remoteInfo["encrypted"] = cacheInfo.get("encrypted", False)
                            fp = open(os.path.join(self.appFolder, self.dmsId, "cache", itemId + ".json"), "w")
                            json.dump(remoteInfo, fp)
                            fp.close()
                            print remoteInfo.get("name", "none") + " loaded from cache"
                            self.progressDone = long(cacheInfo.get("size").__str__()) / 1024
                            self.progressTotal = self.progressDone
                            return True
            
            self.progressDescription = tr("server is processing data")
            
            print "downloading " + remoteInfo.get("name") + " to cache..."
            
            downloadOut = open(os.path.join("download", ".tmp"), "w")
            
            if localMd5 != "" and OS.isWindows():
                u = self.transponderUrl+"?holder-type=java&sid="+self.sid+"&dmsId="+self.dmsId+"&action=downloadItem&itemId="+itemId
                u += "&sourceMd5=" + localMd5
                
            req = urllib2.Request(u, "GET")
            req.add_header("Cookie", self.cookie)
            conn = urllib2.urlopen(req)
            
            if conn.code == 304:
                self.evalJs("window['" + self.jsObj + "'].sessionFailure()")
                self._kill()
                sys.exit(1)
            if conn.getResponseCode() / 100 != 2:
                print "response code: " + conn.getResponseCode()
                self.error = "could not download file from %s" %u
                return False
            contentLength = conn.headers.get("Content-Length", 0)
            self.progressTotal = contentLength / 1024 if contentLength > 0 else 0
            self.progressDescription = tr("download $1", "$1", remoteInfo.get("name").__str__())
            
            bufferSize = 1024*7;
            data = conn.read(bufferSize)
            while data:
                if self.cancel:
                    sys.stdout.write("        > canceled\n")
                    conn.close()
                    os.remove(downloadOut.name)
                    self.progressDescription = "cancelled"
                    self.cancel = False
                    return False
                downloadOut.write(data)
                
                self.progressDone += float(bufferSize) / 1024
                
                data = conn.read(bufferSize)
                #if currSecond != Math.floor(System.currentTimeMillis() / 2000):
                # try:
                #     Thread.sleep(100)
                # except InterruptedException as e:
                #      pass
                #  currSecond = Math.floor(System.currentTimeMillis() / 2000)
            conn.close()
            downloadOut.close()
            if conn.headers['Content-Type'] == "gzip":
                print "gunzip file"
                FileActions.ungzip(downloadOut.name)
            md5Check = FileActions.MD5(downloadOut.name)
            if remoteInfo.has_key("size") and remoteInfo.get("size",0) > 0 and not remoteInfo.get("md5", False):
                print "        > md5 error: remote md5 (" + remoteInfo.get("md5") + ") != local check (" + md5Check + ")"
                self.error = "file was corrupted"
                os.remove(downloadOut.name)
                return False
            print "        > completed"
            
            self.progressDescription = tr("saving file")
            
            cache = os.path.join(self.appFolder, self.dmsId, "cache", itemId)
            if os.path.exists(cache):
                os.removedirs(cache)
            if self.maxEncryptionFileSize < os.stat(downloadOut.name)[6]:
                self.encrypter.encrypt(downloadOut.name, cache)
                remoteInfo.put("encrypted", "true")
            else:
                remoteInfo.put("encrypted", "false")
                os.rename(downloadOut.name, cache)
            if os.path.exists(downloadOut.name):
                os.remove(downloadOut.name)
                
            FileActions.saveHashMap(remoteInfo, self.appFolder, self.dmsId, "cache", itemId + ".json")
            return True
        except (Exception) as e:
            e.printStatckTrace()
            try:
                self.evalJs("window['" + self.jsObj + "'].connectionTimeout()")
            except (Exception) as ee:
                ee.printStackTrace()
                pass
            finally:
                return False
        
    def removeFromCashe(self, itemId):
        """ generated source for method removeFromCashe """
        file_ = os.path.join(self.appFolder, self.dmsId, "cache", itemId)
        if os.path.exists(file_):
            file_.delete()
        jsonFile = os.path.join(self.appFolder, self.dmsId, "cache", itemId, ".json")
        if os.path.exists(jsonFile):
            os.remove(jsonFile)

#   @overloaded
    def openItemOnDesktop(self, itemId, method):
        """ generated source for method openItemOnDesktop """
        openByForce = method != None and method == "force"
        readOnly = method != None and method == "readOnly"
        phrases = []
        phrases.append("opening document")
        phrases.append("opening $1")
        phrases.append("copying $1")
        tr(phrases)
        if int(itemId) < 2:
            self.error = "invalid itemId : " + itemId
            return "error"
        if self.fileChecker == None or not self.fileChecker.isAlive():
            try:
                self.fileChecker = Thread(FileChangeChecker(self))
                self.fileChecker.start()
            except (IOError) as e:
                print e
                self.error = "could not run file checker thread"
                return "error"
        try:
            dir_ = os.path.join(self.tempFolder, self.dmsId, "open_%s" %self.userId)
            if not os.path.isdir(dir_):
                os.mkdir(dir_)
            dir_ = os.path.join(self.tempFolder, self.dmsId, "open_%s" %self.userId, itemId)
            if not os.path.exists(dir_):
                os.mkdir(dir_)
            self.progressDescription = tr("opening document")
            jsonFile = os.path.join(self.tempFolder, self.dmsId, "open_%s" %self.userId, "%s.json" %itemId)
            fp = open(jsonFile)
            jsonString = json.load(fp)
            openInfo = dict(json.loads(jsonString))
            if not readOnly and not openByForce:
                if  jsonString.startsWith("not found"):
                    self.error = "item not found"
                    print "could not find item to lock\n" + json
                    return "not found"
                #else if  jsonString.startsWith("null"):
                else:
                    if not  jsonString.startswith("{"):
                        self.error = "invalid lock return: " + json
                        print "could not find lock\n" + json
                    else:
                        l = dict(json.loads(jsonString))
                        if l.has_key("userFk") and l.has_key("owner") and l.has_key("token"):
                            print "found lock on " + itemId + " for " + l.get("owner") + " (" + l.get("token") + ")"
                            openInfo.put("lockUserId", l.get("userFk"))
                            lock = {}
                            lock["userId"] = l.get("userFk")
                            lock["stamp"] = time.ctime()
                            self.locks.put(itemId, lock)
                        if not l.isEmpty() and not l.get("userFk") == self.userId:
                            print "item is locked by: " + l.get("owner")
                            self.error = "this document is locked by " + l.get("owner")
                            return "locked"
            if not openInfo.isEmpty():
                file_ = os.path.join(self.tempFolder, self.dmsId, "open_" + self.userId, itemId, openInfo.get("name"))
                if FileActions.isLockedByTmpFile(file_):
                    print "open file info is found. file is locked with lock file"
                    lockFile = FileActions.getLockFile(file_)
                    if lockFile != None:
                        if openByForce:
                            print "trying to delete lock file " + lockFile.name
                            if lockFile.delete():
                                print " - succeded"
                            else:
                                print " - failed"
                                self.error = "unable to delete lock file " + lockFile.getAbsolutePath()
                                return "locallyLocked"
                        else:
                            self.error = "This document is locked with a lock file."
                            return "locked"
                if os.path.exists(file_) and FileActions.isLockedByAnyMethod(file_):
                    localInfo = FileActions.loadHashMap(self.appFolder, self.dmsId, "cache", itemId + ".json")
                    if localInfo.has_key("expectFileLock") and not localInfo.get("expectFileLock") == "no":
                        print "file is already opened"
                        self.error = "this document was already open"
                        return "locallyOpen"
                    else:
                        print "file is locked on local system"
                        self.error = "this document was already open"
                        return "locallyLocked"
            self.progressTotal = 0
            self.progressDone = 0
            if not self.downloadItemToCashe(itemId):
                self.unlockItem(itemId)
                if self.progressDescription == "cancelled":
                    return "cancelled"
                else:
                    return "notFound"
            self.progressDone = self.progressTotal
            localInfo = self.getCacheInfo(itemId)
            self.progressDescription = tr("opening $1", "$1", localInfo.get("name").__str__())
            fileName = localInfo.get("name", "")
            file_ = os.path.join(self.tempFolder, self.dmsId, "open_" + self.userId, itemId, fileName)
            if FileActions.isLockedByTmpFile(file_):
                print "file is locked with lock file"
                if lockFile != None:
                    if openByForce:
                        print "trying to delete lock file " + lockFile.getName()
                        if lockFile.delete():
                            print " - succeded"
                        else:
                            print " - failed"
                            self.error = "unable to delete lock file " + lockFile.getAbsolutePath()
                            return "locallyLocked"
                    else:
                        self.error = "This document is locked with a lock file."
                        return "locked"
            if os.path.exists(file_) and FileActions.isLockedByAnyMethod(file_):
                if localInfo.has_key("expectFileLock") and not localInfo.get("expectFileLock") == "no":
                    print "file is already opened"
                    self.error = "this document was already open"
                    return "locallyOpen"
                else:
                    print "file is locked on local system"
                    self.error = "this document was already open"
                    return "locallyLocked"
            if not os.path.exists(file_) or not localInfo.get("size").__str__() == "" + len(file_) or (500 * 1024 < len(file_) and not FileActions.MD5(file_) == localInfo.get("md5")):
                if localInfo.get("encrypted").__str__() == "true":
                    if not os.path.exists(file_):
                        cache = os.path.join(self.appFolder, self.dmsId, "cache", itemId)
                    print "decrypt cache/" + itemId + " to " + file_.__name__
                    self.encrypter.decrypt(cache, file_)
                else:
                    if 1024 * 1024 * 5 > len(cache):
                        self.progressDescription = tr("copying $1", "$1", localInfo.get("name").__str__())
                    print "copy cache/" + itemId + " to " + file_.__name__
                    FileActions.copy(cache, file_)
            self.progressDescription = tr("opening $1", "$1", localInfo.get("name").__str__())
            openedFile = FileActions.openOnDesktop(file, readOnly);
            if openedFile != None:
                file_ = openedFile
                fileName = file_.__name__
                opened = True
            openInfo.put("mtime", file_.lastModified() + "")
            openInfo.put("md5", FileActions.MD5(file_))
            openInfo.put("name", fileName)
            openInfo.put("readOnly", ("true" if readOnly else "false"))
            if opened == True:
                print "local file " + file_.__name__ + " opened" + (" read-only" if readOnly else "")
                self.getTransponderLine("action=notifyOpenDocument&method=" + method + "&itemId=" + itemId)
                if FileActions.isLockedByTmpFile(file_):
                    openInfo.put("expectFileLock", "tmpFile")
                    print "track file locking by locking file"
                elif FileActions.isLockedByFileSystem(file_):
                    openInfo.put("expectFileLock", "fileSystem")
                    print "track file locking by file system lock"
                else:
                    openInfo.put("expectFileLock", "no")
                FileActions.saveHashMap(openInfo, self.tempFolder, self.dmsId, "open_" + self.userId, itemId + ".json")
                return "ok"
            else:
                print "could not open local file" + file_.__name__
                self.error = "could not open " + openInfo.get("name")
                openInfo.put("expectFileLock", "no")
                FileActions.saveHashMap(None, self.tempFolder, self.dmsId, "open_" + self.userId, itemId + ".json")
                return "failed"
        except Exception as e:
            e.printStackTrace()
            return "error"

    @openItemOnDesktop.register(object, str)
    def openItemOnDesktop_0(self, itemId):
        """ generated source for method openItemOnDesktop_0 """
        return self.openItemOnDesktop(itemId, "")

##    @overloaded
    def deleteOpenItem(self, itemId, force):
        """ generated source for method deleteOpenItem """
        
        openFolder = os.path.join(self.tempFolder, self.dmsId, "open_" + self.userId)
        dir_ = os.path.join(openFolder, itemId)
        file_ = ""
        if not os.path.exists(dir_):
            file_ = os.path.join(openFolder, itemId + ".json")
            file_.delete()
            return False
        try:
            openInfo = {}
            if openInfo == None or not openInfo.has_key("name"):
                return False
            file_ = os.path.join(openFolder, itemId, openInfo.get("name"))
            if force or not FileActions.isLockedByAnyMethod(file_):
                try:
                    file_.delete()
                    if not os.path.exists(file_):
                        print "delete " + openInfo.get("name")
                        FileActions.deleteDir(dir)
                        if not os.path.exists(dir_):
                            file_ = os.path.join(openFolder, itemId + ".json")
                            file_.delete()
                    return True
                except (Exception):
                    return False
            else:
                return False
        except (Exception):
            return False

    @deleteOpenItem.register(object, str)
    def deleteOpenItem_0(self, itemId):
        """ generated source for method deleteOpenItem_0 """
        return self.deleteOpenItem(itemId, False)

##    @overloaded
    def deleteOpenItems(self, force):
        """ generated source for method deleteOpenItems """
        openDir = os.path.join(self.tempFolder, self.dmsId, "open_" + self.userId)
        files = []
        if os.path.isdir(openDir):
            files = os.listdir(openDir)
            for i in files:
                if os.path.isdir(i):
                    os.removedirs(i)
                                
            try:
                os.removedirs(openDir)
            except (Exception) as e:
                sys.stdout.write(e + "\n")
        return True

    @deleteOpenItems.register(object)
    def deleteOpenItems_0(self):
        """ generated source for method deleteOpenItems_0 """
        return self.deleteOpenItems(False)

    def hasOpenItems(self):
        """ generated source for method hasOpenItems """
        openDir = os.path.join(self.tempFolder, self.dmsId, "open_" + self.userId)
        if os.path.isdir(openDir):
            files = os.listdir(openDir)
            for i in files:
                if os.path.isdir(i):
                    return True
        return False

    def cleanCash(self):
        """ generated source for method cleanCash """
        files = os.path.join(self.appFolder, self.dmsId, "cache").listFiles()
        file_ = ""
        TwoWeeksAgo = time.time() - 2 * 7 * 24 * 60 * 60
        i = 0
        while len(files):
            file_ = files[i]
            if not file_.__name__.endsWith(".json") and file_.lastModified() <= TwoWeeksAgo:
                self.removeFromCashe(file_.__name__)
            i += 1
        return True

    def lockItem(self, itemId):
        """ generated source for method lockItem """
        
        lock = dict(self.locks.get(itemId))
        if self.locks.has_key(itemId):
            if not lock.get("userId") == self.userId:
                if long(str(lock.get("stamp"))) < time.time() - (60 * 2):
                    ret = self.getTransponderLine("action=setItemLock&itemId=" + itemId)
                    if ret == "true":
                        lock["stamp"] = time.time()
                        lock["userId"] =  self.userId
                        self.locks[itemId] = lock
                        sys.stdout.write("item lock created: %s\n" %itemId)
                        self.evalJs("window['%s'].notifieLockChange(%s)" %(self.jsObj, itemId))
                        return True
                    elif ret == "false":
                        ret = self.getTransponderLine("action=getItemInfo&itemId=" + itemId)
                        if ret == "null":
                            self.deleteOpenItem(itemId, True)
                        elif ret.startsWith("{"):
                            itemInfo = dict(json.loads(ret))
                            if itemInfo.has_key("writable") and itemInfo.get("writable") == "false":
                                self.deleteOpenItem(itemId, True)
                    else:
                        if ret.startsWith("{"):
                            remoteLock = dict(json.loads(ret))
                            lock["stamp"] = time.time()
                            lock["userId"] = remoteLock.get("userFk")
                            self.locks.put(itemId, lock)
                            self.evalJs("window['%s'].notifieLockChange(%s)" %(self.jsObj, itemId))
                            return False
                        else:
                            lock["stamp"] = time.time()
                            lock["userId"] = "unknown"
                            self.lock[itemId] = lock
                            self.evalJs("window['%s'].notifieLockChange(%s)" %(self.jsObj, itemId))
                            return False
            else:
                if long(str(lock.get("stamp"))) < time.time() * 60 * 4:
                    if ret == "true":
                        lock["stamp"] = time.time()
                        self.locks[itemId] = lock
                        print "item lock refreshed: " + itemId
                        self.evalJs("window['" + self.jsObj + "'].notifieLockChange(" + itemId + ")")
                        return True
                    elif ret == "false":
                        ret = self.getTransponderLine("action=getItemInfo&itemId=" + itemId)
                        if ret == "null":
                            self.deleteOpenItem(itemId, True)
                        elif ret.startsWith("{"):
                            itemInfo = dict(json.loads(ret))
                            if itemInfo.has_key("writable") and itemInfo.get("writable") == "false":
                                self.deleteOpenItem(itemId, True)
                    else:
                        if ret.startsWith("{"):
                            remoteLock = dict(json.loads(ret))
                            lock["stamp"] = time.time()
                            lock["userId"] = remoteLock.get("userFk")
                            self.locks[itemId] = lock
                            self.evalJs("window['%s'].notifieLockChange(%s)" %(self.jsObj, itemId))
                            return False
                        else:
                            lock["stamp"] = time.time()
                            lock["userId"] = "unknown"
                            self.locks[itemId] = lock
                            return False
        else:
            if ret == "true":
                lock["stamp"] = time.time()
                lock["userId"] = self.userId
                self.locks[itemId] = lock
                print "item locked: " + itemId
                self.evalJs("window['%s'].notifieLockChange(%s)" %(self.jsObj, itemId))
                return True
            elif ret == "false":
                ret = self.getTransponderLine("action=getItemInfo&itemId=" + itemId)
                if ret == "null":
                    self.deleteOpenItem(itemId, True)
                elif ret.startsWith("{"):
                    if itemInfo.has_key("writable") and itemInfo.get("writable") == "false":
                        self.deleteOpenItem(itemId, True)
            else:
                if remoteLock == None or not remoteLock.has_key("userId"):
                    self.locks.remove(itemId)
                    return False
                else:
                    lock["stamp"] = time.time()
                    lock["userId"] = remoteLock.get("userFk")
                    self.locks[itemId] = lock
                    return False
        return False

    def unlockItem(self, itemId):
        """ generated source for method unlockItem """
        lock = self.locks.get(itemId)
        if lock == None or not lock.has_key("userId"):
            return
        if lock.get("userId") == self.userId:
            self.locks.remove(itemId)
            print "item unlocked " + itemId
            self.evalJs("window['" + self.jsObj + "'].notifieLockChange(" + itemId + ")")

#    @overloaded
    def doFilePut(self, file_, url, headers, ret):
        """ generated source for method doFilePut """
        if 1024 / len(file_) / 1024 > self.maxUploadMb:
            ret.put("status", "file to big")
            return False
        bytesAvailable = int()
        bytesRead = int()
        bufferSize = int()
        bytesWritten = 0
        buffer_ = []
        status = int()
        statusLine = str()
        headerLines = []
        bodyLines = []
        if ret == None:
            ret = dict()
        ret.clear()
        phrases = []
        phrases.append("canceled")
        tr(phrases)
        try:
            if url.getProtocol() == "https":
                conn = url.openConnection()
            else:
                conn = url.openConnection()
            conn.setUseCaches(False)
            conn.setDoOutput(True)
            conn.setDoInput(True)
            ret.put("status", "unknown")
            ret.put("host", url.getHost())
            ret.put("port", url.getPort() + "")
            ret.put("content-length", "" + len(file_))
            conn.setRequestMethod("PUT")
            headerKeys = conn.headers.keys()
            if headers:
                for key in headerKeys:
                    conn.setRequestProperty(headers[key], headers.get(key))
                                            
                    
            conn.setRequestProperty("Content-length", "" + len(file_))
            conn.setRequestProperty("X-content-length", "" + len(file_))
            conn.setRequestProperty("Cookie", self.cookie)
            conn.setRequestProperty("Connection", "close")
            conn.setChunkedStreamingMode(3 * 1024)
            conn.connect()
            # bytesAvailable = 
            fileInputStream = io.open(file_)
            out = io.BufferedWriter()
            bufferSize = min(bytesAvailable, self.uploadBufferSize)
            buffer_ = [None]*bufferSize
            currSecond = float(time.time() / 2000)
            bytesRead = fileInputStream.read(buffer_, 0, bufferSize)
            while bytesRead >= 0:
                if self.cancel:
                    break
                out.write(buffer_, 0, bufferSize)
                out.flush()
                bytesWritten += bufferSize
                self.progressDone += float(bufferSize) / 1024
                bytesAvailable = fileInputStream.available()
                bufferSize = min(bytesAvailable, self.uploadBufferSize)
                if currSecond != float(time.time() / 2):
                    try:
                        time.sleep(0.1)
                    except (Exception) as e:
                        pass
                    currSecond = float(time.time() / 2000)
            out.close()
            if self.cancel:
                conn.disconnect()
                self.progressDescription = tr("canceled")
                self.cancel = False
                ret.put("status", "canceled")
                return False
            in_ = io.BufferedReader(conn.fp)
            try:
                status = conn.getResponseCode()
                statusLine = conn.getResponseMessage()
                for line in in_.readlines():
                    bodyLines.add(line)
                in_.close()
            except (IOError) as e:
                status = conn.getResponseCode()
                statusLine = conn.getResponseMessage()
                if status == 409:
                    ret.put("status", "full")
                    self.error = statusLine
                    print "insufficiant disk space"
                    return False
            ret.put("headers", headerLines)
            ret.put("body", bodyLines)
            ret.put("status", bodyLines.get(0))
        except (Exception) as e:
            self.progressDone -= float(bytesWritten) / 1024
            ret.put("status", "exception")
            ret.put("exception", e.getMessage())
            self.error = str(e.getMessage())
            print "timeout while uploading:"
            e.printStackTrace()
            return False
        except Exception as e:
            self.progressDone -= float(bytesWritten) / 1024
            ret.put("status", "exception")
            ret.put("exception", e.getMessage())
            self.error = str(e.getMessage())
            print "error while uploading:"
            e.printStackTrace()
            return False
        if status == 304:
            self.progressDone -= float(bytesWritten) / 1024
            self.evalJs("window['" + self.jsObj + "'].sessionFailure()")
            return False
        elif status == 200:
            return True
        else:
            self.progressDone -= float(bytesWritten) / 1024
            self.error = statusLine + " => " + bodyLines.get(0)
            print "error while uploading: " + self.error
            return False

    #@doFilePut.register(object, File, URL)
    def doFilePut_0(self, file_, url):
        """ generated source for method doFilePut_0 """
        return self.doFilePut(file_, url, None, None)

    def uploadSelectedFiles(self, folderId):
        """ generated source for method uploadSelectedFiles """
        remoteFileInfo = dict()
        localFileInfo = dict()
        i = int()
        gzip = None
        file_ = open(os.path.join("test", ".tmp"))
        currFilesRoot = file_.getCanonicalPath().substring(0, 1)
        file_.delete()
        file_ = None
        fileSize = 0
        self.uploadInfo.clear()
        bytesAvailable = int()
        bytesRead = int()
        bufferSize = int()
        buffer_ = []
        line = str()
        phrases = []
        phrases.append("preparing upload")
        phrases.append("$1 files")
        phrases.append("uploading information for $1 files")
        phrases.append("downloading file information for $1 files")
        phrases.append("comparing file $1 of $2 ($3%)")
        phrases.append("compressing")
        phrases.append("compressing $1")
        phrases.append("uploading $1")
        phrases.append("server is processing data")
        phrases.append("insufficiant disk space")
        tr(phrases)
        repl = dict()
        self.resetProgress()
        self.progressDescription = tr("preparing upload")
        if not self.hasFilesInSelection:
            self.error = "no files selected"
            return False
        try:
            if self.cancel:
                self.cancel = False
                print "cancelled during walking files..."
                self.error = "canceled by user"
                return False
            self.resetProgress()
            localInfo = UploadFilesTree(self.selectedFiles)
            remoteInfo = {}
            url = self.transponderUrl+"?holder-type=java&sid="+self.sid+"&dmsId="+self.dmsId+"&action=getFolderSyncInfo&folderId="+folderId
            self.progressDescription = tr("preparing upload")
            self.uploadInfo["files"] = int(localInfo.fileCount)
            self.uploadInfo["folders"] = int(localInfo.folderCount)
            self.uploadInfo["uploads"] = int()
            self.uploadInfo["unchangeds"] = int()
            self.uploadInfo["failures"] = int()
            self.uploadInfo["kb"] = float()
            if url.getProtocol() == "https":
                conn = url.openConnection()
            else:
                conn = url.openConnection()
            conn.setUseCaches(False)
            conn.setDoOutput(True)
            conn.setDoInput(True)
            conn.setRequestMethod("POST")
            conn.setRequestProperty("Cookie", self.cookie)
            conn.setChunkedStreamingMode(3 * 1024)
            contentLength = 0
            for k in localFileInfo.keys():
                line = localFileInfo.get(k) + "\n"
                contentLength += len(line)
            conn.setRequestProperty("X-content-length", contentLength + "")
            self.progressDescription = tr("uploading information for $1 files", "$1", len(localInfo) + "")
            self.progressTotal = contentLength / 1024
            conn.connect()
            up = io.BufferedWriter()
            contentLength = 0
            for k in localFileInfo.keys():
                if self.cancel:
                    self.cancel = False
                    print "cancelled during writing data to server..."
                    self.error = "canceled by user"
                    return False
                line = localFileInfo.get(k) + "\n"
                up.write(line.getBytes(), 0, )
                up.flush()
                contentLength += len(line)
                self.progressDone = contentLength / 1024
            line = "0\n"
            up.write(line.getBytes(), 0, )
            up.close()
            self.resetProgress()
            contentLength = 0
            i = 0
            self.progressDescription = tr("downloading file information for $1 files", "$1", len(localInfo) + "")
            down = io.BufferedReader(conn.fp)
            for line in down.readlines():
                if self.cancel:
                    self.progressDescription = "cancelled"
                    down.close()
                    self.cancel = False
                    print "cancelled during reading data from server..."
                    self.error = "canceled by user"
                    return False
                if line.startsWith("{"):
                    remoteFileInfo = dict(json.loads(line))
                    if remoteFileInfo != None:
                        localInfo.remoteInfo.put(remoteFileInfo.get("path"), remoteFileInfo)
                elif line == "0":
                    break
                contentLength += len(line)
                i += 1
                if contentLength > 0:
                    self.progressTotal = contentLength / i * len(localInfo) / 1024
                    self.progressDone = contentLength / 1024
            down.close()
            self.resetProgress()
            self.progressTotal = localInfo.kb
            #i = 0
            uploads = []
            for i in uploads:
                if self.cancel:
                    self.progressDescription = "cancelled"
                    self.cancel = False
                    print "cancelled during comparing data..."
                    self.error = "canceled by user"
                    return False
                #i += 1
                file_ = str(localFileInfo.get("path"))
                fileSize = len(file_)
                hidden = False
           
                if sys.platform == "win32":
                    attrs = ctypes.windll.kernel32.GetFileAttributesW(unicode(os.path.abspath(file_)))
                    assert attrs != -1
                    hidden = bool(attrs & 2)
                
                tests = [os.path.isfile(file_), not os.access(file_, os.R_OK) or hidden,
                         os.path.basename(file_.startsWith(".")) or os.path.basename(file_).startsWith("~"),
                         file_.__name__.endsWith(".lnk")]
                
                if True in tests:
                    self.progressTotal -= fileSize / 1024
                    continue 
                repl = dict()
                repl.append("$1", i + "")
                repl.append("$2", len(localInfo) + "")
                repl.append("$3", round(float(i) / len(localInfo) * 100) + "")
                self.progressDescription = tr("comparing file $1 of $2 ($3%)", repl)
                
                
                remoteFileInfo = remoteInfo.get(str(localFileInfo.get("key")))
                if remoteFileInfo == None and self.userIsWheel:
                    uploads.append(localFileInfo)
                elif remoteFileInfo == None:
                    print "no info found for: " + localFileInfo.get("key")
                    self.progressTotal -= fileSize / 1024
                elif (remoteFileInfo.has_key("size") and remoteFileInfo.get("size").__str__() == "0") and fileSize == 0:
                    if remoteFileInfo.has_key("size") and not remoteFileInfo.get("size").__str__() == fileSize + "":
                        if remoteFileInfo.get("writable") == "true":
                            uploads.add(localFileInfo)
                    else:
                        self.progressTotal -= fileSize / 1024
                elif remoteFileInfo.has_key("size") and fileSize > 500 * 1024 and remoteFileInfo.get("size").__str__() == fileSize + "":
                    self.progressTotal -= fileSize / 1024
                elif remoteFileInfo.has_key("md5") and not remoteFileInfo.get("md5") == FileActions.MD5(file_):
                    if remoteFileInfo.get("writable") == "true":
                        uploads.add(dict(localFileInfo))
                    else:
                        self.progressTotal -= fileSize / 1024
                elif not remoteFileInfo.has_key("md5"):
                    if remoteFileInfo.get("writable") == "true":
                        uploads.add(dict(localFileInfo))
                    else:
                        self.progressTotal -= fileSize / 1024
                else:
                    print "ignore unchanged local file: " + localFileInfo.get("key")
                    self.progressTotal -= fileSize / 1024
                localFileInfo.clear()
                if remoteFileInfo != None:
                    remoteFileInfo.clear()
            remoteInfo.clear()
            localInfo.clear()
            
            uploadReturn = {}
            uploadHeaders = {}
            ret = False
            tryCount = int()
            status = str()
            
            if uploads.isEmpty():
                self.progressTotal = 0
                return True
            self.progressDescription = tr("uploading")
            if localInfo.kb > 1024:
                if self.getTransponderLine(self.transponderUrl + "?holder-type=java&sid=" + self.sid + "&dmsId=" + self.dmsId + "&action=checkAvailableSpace&kb=" + localInfo.kb) == "true":
                    diskSpaceAbundant = True
                else:
                    print "insufficiant disk space for complete upload of " + len(uploads) + " files with total size of " + str(float(localInfo.kb) * 1024)
                    if len(uploads) == 1:
                        self.error = tr("insufficiant disk space")
                        return False
                print "sufficiant disk space return: " + line
                diskSpaceAbundant = line == "true"
            while i < len(uploads):
                if self.cancel:
                    self.progressDescription = "cancelled"
                    for u in uploads:
                        upload = uploads.get(u)
                        if upload.has_key("gzip"):
                            file_ = str(upload.get("gzip"))
                            if os.path.exists(file_):
                                file_.delete()
                        
                    self.cancel = False
                    print "cancelled during uploading..."
                    self.error = "canceled by user"
                    return False
                upload = uploads.get(i)
                gzip = None
                file_ = str(upload.get("path"))
                fileSize = len(file_)
                if not file_.isFile() or not file_.canRead() or file_.isHidden() or file_.__name__.startsWith(".") or file_.__name__.startsWith("~") or file_.__name__.endsWith(".lnk"):
                    if file_.isFile():
                        self.progressTotal -= fileSize / 1024
                    continue 
                name = file_.name
                if not diskSpaceAbundant and fileSize > 1024 * 1024 and not self.getTransponderLine(self.transponderUrl + "?holder-type=java&sid=" + self.sid + "&dmsId=" + self.dmsId + "&action=checkAvailableSpace&kb=" + (fileSize / 1024)) == "true":
                    print "insufficiant diskspace for " + name
                    self.error = tr("insufficiant disk space")
                    return False
                
                extensions = [".zip", ".gz", ".rar", ".jar", ".bz2",  ".gif", ".png", ".jpg",
                              ".jpeg", ".tif", ".tiff", ".psd", ".ai", ".gz", ".tgz", ".mp3", 
                              ".mpeg", ".wav", ".mp4", ".m4a", ".m4p", ".avi", ".fla", ".flv", 
                              ".exe", ".msi", ".xlsx", ".docx", ".pptx", ".wma", ".wmv", ".mpg"]
                
                tests = [fileSize < 5 * 1024 * 1024, fileSize > 1024 * 10, 
                         os.path.dirname(file_) == currFilesRoot, 
                         os.path.splitext(name)[1] not in extensions]
                if not False in tests:
                    print "compressing " + upload.get("key")
                    self.progressDescription = tr("compressing $1", "$1", name)
                    gzip = FileActions.gzip(file_)
                    fileSize = float(len(gzip))
                    self.progressDone += (float(fileSize) / 1024) - (fileSize / 1024)
                if fileSize / 1024 / 1024 > self.maxUploadMb:
                    self.progressDescription = "cancelled"
                    if gzip != None:
                        gzip.delete()
                    self.error = file_.getAbsolutePath() + " is to big"
                    return False
                print "start uploading " + upload.get("key") + " - " + str(fileSize) + "..."
                self.progressDescription = tr("uploading $1", "$1", name)
                uploadHeaders.put("X-path", upload.get("key").__str__())
                uploadReturn.clear()
                uploadReturn.put("status", "none")
                tryCount = 0
                ret = False
                while not ret and tryCount < 2:
                    if gzip != None:
                        url = self.transponderUrl + "?holder-type=java&sid=" + self.sid + "&dmsId=" + self.dmsId + "&action=uploadFileInFolder&uploadSeries=" + i + "-" + len(uploads) + "&folderId=" + folderId + "&path=" + urllib.urlencode(str(upload.get("key")), "UTF-8") + "&contentType=gzip"
                        ret = self.doFilePut(gzip, url, uploadHeaders, uploadReturn)
                        gzip.delete()
                    else:
                        url = self.transponderUrl + "?holder-type=java&sid=" + self.sid + "&dmsId=" + self.dmsId + "&action=uploadFileInFolder&uploadSeries=" + i + "-" + len(uploads) + "&folderId=" + folderId + "&path=" + urllib.urlencode(str(upload.get("key")), "UTF-8")
                        ret = self.doFilePut(file_, url, uploadHeaders, uploadReturn)
                    tryCount += 1
                    if uploadReturn.get("status") == "canceled":
                        break
                    if uploadReturn.get("status") == "full":
                        break
                    elif not ret:
                        print " retry upload ... ",
                        try:
                            time.sleep(1)
                        except (Exception) as e:
                            e.printStackTrace()
                status = str(uploadReturn.get("status"))
                upload.put("status", status)
                print "       > " + status
                if not ret:
                    if status == "canceled":
                        print "upload canceled by user"
                        self.error = tr("the upload was canceled by the user")
                    elif status == "exception":
                        self.error = str(uploadReturn.get("exception"))
                    else:
                        print "upload failure status: " + status
                    return False
                upload.put("ret", status)
                self.uploadInfo["uploads"] = int(self.uploadInfo.get("uploads",0)) + 1
                i += 1
                
            self.uploadInfo["kb"] = float(self.progressDone)
            self.progressDone = self.progressTotal
            upload.clear()
        except (Exception) as e:
            if "timeout in e":
                print "connection timeout error..."
                self.error = "error: connection timed out"
            e.printStackTrace()
           
            return False
        # except OutOfMemoryError as e:
        #     print "out of memory error..."
        #     e.printStackTrace()
        #     self.error = "error: memory overload (to many files)"
        #     return False
        # except Exception as e:
        #    print "Exception in uplaodSelectedFiles: " + e.getMessage()
        #   self.error = e.getMessage()
        #  e.printStackTrace()
        # return False
        return True

#    @doFilePut.register(object, File, str)
    def doFilePut_1(self, file_, url):
        """ generated source for method doFilePut_1 """
        realUrl = urllib.urlencode(url)
        return self.doFilePut(file_, realUrl)

#    @doFilePut.register(object, File, str, HashMap, HashMap)
    def doFilePut_2(self, file_, url, headers, ret):
        """ generated source for method doFilePut_2 """
        realUrl = url.urlencode(url)
        return self.doFilePut(file_, realUrl, headers, ret)

#    @doFilePut.register(object, str, str, HashMap, HashMap)
    def doFilePut_3(self, contents, url, headers, ret):
        """ generated source for method doFilePut_3 """
        file_ = None
        try:
            file_ = open(os.path.join("content", ".tmp"), "w")
            #file_.deleteOnExit()
            FileActions.setContents(file_, contents)
            #os.remove(file_)
            return True
        except Exception as e:
            sys.stdout.write(e)
            if file_ != None and os.path.exists(file_):
                os.remove(file_)
            return False

#    @doFilePut.register(object, str, str)
    def doFilePut_4(self, contents, url):
        """ generated source for method doFilePut_4 """
        return self.doFilePut(contents, url, None, None)

    
    class fileSelectionInfo(object):
        """ generated source for class fileSelectionInfo """
        files = []
        selection = []
        totalKb = 0
        fileCount = 0
        dirCount = 0

        def __init__(self, files):
            """ generated source for method __init__ """
            self.files.clear()
            self.selection.clear()
            self.files.clear()
            self.totalKb = 0
            self.fileCount = 0
            self.dirCount = 0
            if files == None or len(files):
                return
            fileName = str()
            fileSize = long()
            file_ = ""
            i = 0
            while len(files):
                file_ = files[i]
                fileName = file_.name
                fileSize = len(file_)
                if fileName.index(".") == 0 or fileName.index("~") == 0:
                    continue 
                if not file_.isDirectory():
                    self.fileCount += 1
                    self.selection.add(fileName)
                    self.totalKb += fileSize / 1024
                else:
                    self.dirCount += 1
                    self.selection.add(fileName)
                    self.addList(file_.listFiles())
                i += 1

        def addList(self, files):
            """ generated source for method addList """
            fileSize = long()
            file_ = ""
            i = 0
            while len(files):
                file_ = files[i]
                fileSize = len(file_)
                if not file_.isDirectory():
                    self.fileCount += 1
                    self.totalKb += fileSize / 1024
                else:
                    self.dirCount += 1
                    self.addList(file_.listFiles())
                i += 1

        def toJSON(self):
            """ generated source for method toJSON """
            info = dict()
            info["selection"] = self.selection
            info["fileCount"] = str(self.fileCount)
            info["dirCount"] = str(self.dirCount)
            info["totalKb"] = str(self.totalKb)
            return json.dumps(info)

#    @overloaded
    def hasFilesInSelection(self):
        """ generated source for method hasFilesInSelection """
        return self.hasFilesInSelection(self.selectedFiles)

#    @hasFilesInSelection.register(object, File)
    def hasFilesInSelection_0(self, files):
        """ generated source for method hasFilesInSelection_0 """
        if not files:
            return False
        for f in files:
            if os.path.isfile(f):
                return True
            if os.path.isdir(f) and self.hasFilesInSelection(f):
                return True
        return False

#    @overloaded
    def execCommand(self, command, wait):
        """ generated source for method execCommand """
        
        try:
            if OS.isWindows() and command:
                pr = subprocess.Popen(["cmd.exe", "/C", command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            elif OS.isMac() and command:
                pr = subprocess.Popen(["bash", "-c", command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            else:
                pr = os.system(command)
                return pr
            if not wait:
                pr.terminate()
                return True
            pr.wait()
            output = pr.stdout.readlines()
            pr.terminate()
            if pr.returncode == 0:
                return True
            else:
                if output:
                    for line in output:
                        sys.stdout.write(line)
                return False
        except (Exception) as e:
            e.printStackTrace()
            self.execContent = e
            return False

#    @execCommand.register(object, str, bool)
    def execCommand_0(self, command, wait):
        """ generated source for method execCommand_0 """
        return self.execCommand(command, wait)

#    @execCommand.register(object, str)
    def execCommand_1(self, command):
        """ generated source for method execCommand_1 """
        return self.execCommand(command, True)

    def _restartNetUseServices(self):
        """ generated source for method _restartNetUseServices """
        resultIndex = ("success", "failed")
        cmds = ["net stop mrxdav", 
                "net stop webclient", 
                "net start mrxdav", 
                "net start webclient"]
        
        sys.stdout.write("try to restart webclient and mrxdav services")
        for cmd in cmds:
            sys.stdout.write("%s: %s\n" %(cmd, resultIndex[self.execCommand(cmd)]))
        
    def _createNetUse(self, letter, persistent):
        """ generated source for method _createNetUse """
        if not OS.isWindows() or not letter.matches("^[D-Z]$"):
            return False
        jsonString = self.getTransponderLine("action=getWebDavCredentials")
        if 1 < len(json):
            print "WebDAV credentials JSON not found"
            return False
        cred = dict(json.loads(jsonString))
        if cred == None or (not cred.has_key("http") and not cred.has_key("https")) or not cred.has_key("userName") or not cred.has_key("password"):
            print "incorrect webdav credentials"
            return False
        httpUrl = ""
        if cred.has_key("netUseHttp"):
            httpUrl = str(cred.get("netUseHttp"))
        elif cred.has_key("http"):
            httpUrl = str(cred.get("http"))
        httpsUrl = ""
        if cred.has_key("netUseHttps"):
            httpsUrl = str(cred.get("netUseHttps"))
        elif cred.has_key("https"):
            httpsUrl = str(cred.get("https"))
        loginUrl = ""
        if cred.has_key("webInterface"):
            loginUrl = str(cred.get("webInterface"))
        if httpUrl == "" and httpsUrl == "" and not cred.has_key("aux"):
            print "no webdav url found"
            return False
        if OS.version() < 6 and httpUrl == "":
            self.error = "this version of Windows is not able to use WebDAV over SSL"
            return False
        self.execCommand("net use " + letter + ": /DELETE")
        success = False
        clientsRestartedTried = False
        url = ""
        uri = ""
        if not httpsUrl == "" and OS.version() >= 6:
            url = httpsUrl
            print "try to create net use to " + url
            success = self.execCommand("net use " + letter + ": \"" + url + "\" /USER:" + cred.get("userName") + " " + cred.get("password") + " /PERSISTENT:no")
            if not success and not clientsRestartedTried:
                self._restartNetUseServices()
                clientsRestartedTried = True
                success = self.execCommand("net use " + letter + ": \"" + url + "\" /USER:" + cred.get("userName") + " " + cred.get("password") + " /PERSISTENT:no")
        if not success:
            if not httpUrl == "" and not httpUrl == httpsUrl:
                url = httpUrl
                print "try to create net use to " + url
                success = self.execCommand("net use " + letter + ": \"" + url + "\" /USER:" + cred.get("userName") + " " + cred.get("password") + " /PERSISTENT:no")
                if not success and not clientsRestartedTried:
                    self._restartNetUseServices()
                    clientsRestartedTried = True
                    success = self.execCommand("net use " + letter + ": \"" + url + "\" /USER:" + cred.get("userName") + " " + cred.get("password") + " /PERSISTENT:no")
            if not success:
                try:
                    if not httpsUrl == "" and OS.version() >= 6:
                        uri = urllib2.Request()
                        url = uri.getProtocol() + "://" + socket.gethostbyname(uri.getHost()).getHostAddress() + (":" + uri.getPort() if uri.getPort() > -1 and uri.getPort() != 443 else "") + uri.getPath()
                        print "try to create net use to " + url
                        success = self.execCommand("net use " + letter + ": \"" + url + "\" /USER:" + cred.get("userName") + " " + cred.get("password") + " /PERSISTENT:no")
                        if not success and not clientsRestartedTried:
                            self._restartNetUseServices()
                            clientsRestartedTried = True
                            success = self.execCommand("net use " + letter + ": \"" + url + "\" /USER:" + cred.get("userName") + " " + cred.get("password") + " /PERSISTENT:no")
                    if not success and not httpUrl == "" and not httpUrl == httpsUrl:
                        try:
                            uri = urllib.urlencode(httpUrl)
                            url = uri.getProtocol() + "://" + socket.gethostbyname(uri.getHost()).getHostAddress() + (":" + uri.getPort() if uri.getPort() > -1 and uri.getPort() != 80 else "") + uri.getPath()
                            print "try to create net use to " + url
                            success = self.execCommand("net use " + letter + ": \"" + url + "\" /USER:" + cred.get("userName") + " " + cred.get("password") + " /PERSISTENT:no")
                            if not success and not clientsRestartedTried:
                                self._restartNetUseServices()
                                clientsRestartedTried = True
                                success = self.execCommand("net use " + letter + ": \"" + url + "\" /USER:" + cred.get("userName") + " " + cred.get("password") + " /PERSISTENT:no")
                        except Exception as e:
                            pass
                except Exception as e:
                    pass
        if success:
            print "created net use " + letter + ": " + cred.get("userName") + "@" + url
            try:
                vbsFile = os.path.join(self.tempFolder, "netuserename.vbs")
                #vbsFile.deleteOnExit()
                FileActions.setContents(vbsFile, "mDrive = \"" + letter + ":\\\"\nSet oShell = CreateObject(\"Shell.Application\")\noShell.NameSpace(mDrive).Self.Name = \"OfficeDrive - " + cred.get("userName") + "\"")
                vbsFile.delete()
                self.execCommand("wscript //B //T:2 \"" + vbsFile.getAbsolutePath() + "\"")
            except Exception as e:
                pass
            if persistent:
                netUseStartupJar = os.path.join(appdir, self.windowsStartupJar)
                if not netUseStartupJar.exists():
                    FileActions.downloadUrlToFile(self.rootUrl + "/" + self.windowsStartupJar, netUseStartupJar)
                if os.path.exists(netUseStartupJar):
                    vbScript = "Set objShell = WScript.CreateObject(\"WScript.Shell\")\n"\
                        + "strStartupFolder = objShell.SpecialFolders(\"Startup\")\n"\
                        + "Set objShortCut = objShell.CreateShortcut(strStartupFolder & \"\\OfficeDrive remote disk "+letter+".lnk\")\n"\
                        + "objShortCut.WorkingDirectory = \""+self.appFolder+"\"\n"\
                        + "objShortCut.TargetPath = \"java\"\n"\
                        + "objShortCut.Arguments = \"-jar \" & chr(34) & \""\
                        + os.path.abspath(netUseStartupJar)\
                        + "\" & chr(34) & \" "+letter+" "+url+" "+cred.get("userName")+" "+cred.get("password")+" "+loginUrl+"\"\n"\
                        + "objShortCut.WindowStyle = 7\n"\
                        + "objShortCut.Description = \"OfficeDrive Create remote disk "+letter+": for "\
                        + self.uniqueUserId+"\"\n"\
                        + "objShortCut.Save\n"
                    vbsFile = os.path.join(self.tempFolder, "createstartupshortcut.vbs")
                    vbsFile.deleteOnExit()
                    FileActions.setContents(vbsFile, vbScript)
                    self.execCommand("cscript /nologo \"" + vbsFile.getAbsolutePath() + "\"", True)
                    vbsFile.delete()
                else:
                    print "could not get " + self.rootUrl + "/" + self.windowsStartupJar
            try:
                info = {}
                info["letter"] = letter
                info["persistent"] = persistent
                info["name"] = cred.get("userName") + "@" + url
                FileActions.saveHashMap(info, self.appRootFolder, "netuse", self.uniqueUserId)
                FileActions.setContents(self.appRootFolder, "netuse", letter, self.uniqueUserId)
            except Exception as e:
                sys.stdout.write(e)
                pass
        else:
            self.getTransponderLine("action=reportNetUseError&error=" + urllib.urlencode(self.execContent))
            file_ = os.path.join(self.appRootFolder, "netuse", self.uniqueUserId)
            if os.path.exists(file_):
                os.remove(file_)
            if self.myNetUseLetter != None and self.myNetUseLetter.matches("^[D-Z]$"):
                file_ = os.path.join(self.appRootFolder, "netuse", self.myNetUseLetter)
                if os.path.exists(file_):
                    file_.delete()
            self.myNetUseLetter = self.currentNetUseLetter = ""
            print "exec error: " + self.execContent
            self.error = "could not create net use " + letter + " on " + url + " with user " + cred.get("userName") + ")\n\n" + self.execContent
            return False
        self.myNetUseLetter = self.currentNetUseLetter = letter
        self.currentNetUseIsPersistent = persistent
        return True

    def _removeNetUse(self):
        """ generated source for method _removeNetUse """
        if not self.currentNetUseLetter == "":
            vbScript = "Set objShell = WScript.CreateObject(\"WScript.Shell\")\n"\
                + "Set objFSO = CreateObject(\"Scripting.FileSystemObject\")\n"\
                + "objFSO.DeleteFile(objShell.SpecialFolders(\"Startup\") & \"\\OfficeDrive remote disk "\
                + self.currentNetUseLetter + ".lnk\")\n"
            
            vbsFile = os.path.join(self.tempFolder, "createstartupshortcut.vbs")
            vbsFile.deleteOnExit()
            FileActions.setContents(vbsFile, vbScript)
            self.execCommand("cscript /nologo \"" + vbsFile.getAbsolutePath() + "\"", True)
            os.remove(vbsFile)
        if not self.currentNetUseLetter == "" and (self.execCommand("net use " + self.currentNetUseLetter + ": /DELETE") or not self.execCommand("net use " + self.currentNetUseLetter)):
            try:
                info = FileActions.loadHashMap(os.path.join(self.appRootFoldernetuse, self.uniqueUserId))
                if info:
                    info["persistent"] = False
                    FileActions.saveHashMap(info, self.appRootFolder, "netuse", self.uniqueUserId)
            except Exception as e:
                sys.stdout.write("%s\n" %e)
                pass
            self.currentNetUseLetter = ""
            self.myNetUseLetter = self.currentNetUseLetter
            return True
        else:
            return False

    def _getNetUseLetters(self):
        """ generated source for method _getNetUseLetters """
        letters = dict()
        file_ = ""
        info = dict()
        dir_ = os.path.join(self.appRootFolder, "netuse")
        if not os.path.exists(dir_):
            return letters
        files = dir.listFiles()
        i = 0
        while len(files):
            file_ = files[i]
            if file_.__name__.matches("^[D-Z]$"):
                try:
                    info = FileActions.loadHashMap(self.appRootFolder, "netuse", FileActions.getContents(file_))
                    if info != None and info.has_key("name"):
                        letters.put(info.get("letter"), info.get("name"))
                except Exception as e:
                    pass
            i += 1
        return letters

    def _resetStartupLink(self):
        """ generated source for method _resetStartupLink """
        if self.currentNetUseLetter == "" or not self.currentNetUseIsPersistent:
            return False
        vbScript = "Set objShell = WScript.CreateObject(\"WScript.Shell\")\n" + "Set objFSO = CreateObject(\"Scripting.FileSystemObject\")\n" + "objFSO.DeleteFile(objShell.SpecialFolders(\"Startup\") & \"\\OfficeDrive remote disk " + self.currentNetUseLetter + ".lnk\")\n"
        vbsFile = os.path.join(self.tempFolder, "createstartupshortcut.vbs")
        vbsFile.deleteOnExit()
        FileActions.setContents(vbsFile, vbScript)
        self.execCommand("cscript /nologo \"" + vbsFile.getAbsolutePath() + "\"", True)
        jsonString = self.getTransponderLine("action=getWebDavCredentials")
        if 1 < len(json):
            return False
        cred = json.loads(jsonString)
        if cred == None:
            return False
        url = None
        user = None
        pass_ = None
        loginUrl = None
        if OS.version() < 6:
            if cred.has_key("netUseHttp"):
                url = str(cred.get("netUseHttp"))
            elif cred.has_key("http"):
                url = str(cred.get("http"))
        else:
            if cred.has_key("netUseHttps"):
                url = str(cred.get("netUseHttps"))
            elif cred.has_key("https"):
                url = str(cred.get("https"))
        if cred.has_key("userName"):
            user = str(cred.get("userName"))
        if cred.has_key("password"):
            pass_ = str(cred.get("password"))
        if cred.has_key("webInterface"):
            loginUrl = str(cred.get("webInterface"))
        if url != None and user != None and pass_ != None and loginUrl != None:
            uploadFilesTree = UploadFilesTree()
            if not os.path.exists(uploadFilesTree.netUseStartupJar):
                FileActions.downloadUrlToFile(self.rootUrl + "/" + self.windowsStartupJar, uploadFilesTree.netUseStartupJar)
            if not os.path.exists(uploadFilesTree.netUseStartupJar):
                return False
            vbScript = "Set objShell = WScript.CreateObject(\"WScript.Shell\")\n"\
                        + "strStartupFolder = objShell.SpecialFolders(\"Startup\")\n"\
                        + "Set objShortCut = objShell.CreateShortcut(strStartupFolder & \"\\OfficeDrive remote disk "\
                        + self.currentNetUseLetter + ".lnk\")\n"\
                        + "objShortCut.WorkingDirectory = \""\
                        + self.appFolder + "\"\n" + "objShortCut.TargetPath = \"java\"\n"\
                        + "objShortCut.Arguments = \"-jar \" & chr(34) & \""\
                        + os.path.abspath(uploadFilesTree.netUseStartupJar) + "\" & chr(34) & \" "\
                        + self.currentNetUseLetter + " " + url + " " + cred.get("userName") + " "\
                        + cred.get("password") + " " + loginUrl + "\"\n" + "objShortCut.WindowStyle = 7\n"\
                        + "objShortCut.Description = \"OfficeDrive Create remote disk "\
                        + self.currentNetUseLetter + ": for " + self.uniqueUserId + "\"\n" + "objShortCut.Save\n"
                        
            vbsFile = os.path.join(self.tempFolder, "createstartupshortcut.vbs")
            vbsFile.deleteOnExit()
            FileActions.setContents(vbsFile, vbScript)
            self.execCommand("cscript /nologo \"" + vbsFile.getAbsolutePath() + "\"", True)
            vbsFile.delete()
            return True
        else:
            vbsFile.delete()
            return False

    def _createMount(self, persistent):
        """ generated source for method _createMount """
        if not OS.isMac():
            return False
        jsonString = self.getTransponderLine("action=getWebDavCredentials")
        if json == None or 1 < len(json) or not  jsonString.startsWith("{"):
            self.error = "JSON for webdav credentials not found"
            print self.error
            return False
        cred = dict(json.loads(jsonString))
        if cred == None or (not cred.has_key("mac") and not cred.has_key("http") and not cred.has_key("https")) or not cred.has_key("userName") or not cred.has_key("password"):
            self.error = "incorrect webdav credentials"
            print self.error
            return False
        webdavUrl = None
        if cred.has_key("mac"):
            webdavUrl = cred.get("mac").__str__()
        elif cred.has_key("https"):
            webdavUrl = cred.get("https").__str__()
        elif cred.has_key("http"):
            webdavUrl = cred.get("http").__str__()
        if webdavUrl == None or 5 < len(webdavUrl):
            self.error = "webdav URL not found in credentials"
            print self.error
            return False
        
        url = webdavUrl
        path = url.getPath().split("/");
        if path[len(path) - 1]:
            volumeName = path[:path.length - 2]
        else:
            volumeName = path[:path.length - 1]
            
        node = os.path.join("/Volumes/", volumeName)
        
        try:
            print "try to connect to " + webdavUrl + " with applescript"
            
            if node.exists():
                self.execCommand("/sbin/umount -f " + node.getAbsolutePath())
            self.execCommand("defaults write com.apple.desktopservices DSDontWriteNetworkStores true")
            self.execCommand("security -v add-internet-password -a \"" + cred.get("userName") + "\" -d " + url.getHost() + " -r " + url.getProtocol() + " -s " + url.getHost() + " -p " + url.getPath() + " -t 0 -w \"" + cred.get("password") + "\" -T /sbin/mount_webdav", True)
            
            applescript = "tell application \"Finder\"\n"\
                + "    if exists disk \""+volumeName+"\" then\n"\
                + "        beep 2\n"\
                + "    else\n"\
                + "        try\n"\
                + "            mount volume \""+webdavUrl+"\" as user name \""+cred.get("userName")+"\" with password \""+cred.get("password")+"\"\n"\
                + "            on error\n"\
                + "                activate\n"\
                + "                display dialog \"Autentication failed, exiting\" buttons \"Cancel\"\n"\
                + "        end try\n"\
                + "        delay 1\n"\
                + "        repeat until (list disks) contains \""+volumeName+"\"\n"\
                + "            delay 1\n"\
                + "        end repeat\n"\
                + "    end if\n"\
                + "end tell"
            success = self.execCommand(applescript, True)
            if success:
                success = os.path.exists(node)
            if success:
                print "mounted " + webdavUrl + " on " + os.path.abspath(node)
                info = {}
                info["node"] = os.path.abspath(node)
                info["persistent"] = persistent
                FileActions.saveHashMap(info, self.appFolder, self.dmsId, "mount_" + self.userId + ".json")
                self.currentMountIsPersistent = persistent
                self.currentMountNode = node.getAbsolutePath()
                if persistent:
                    print "try to add login item... ",
                    applescript = "tell application \"System Events\"\n"\
                     + "	get the name of every login item\n"\
                      + "	if login item \"" + volumeName + "\" exists then\n"\
                       + "		-- do nothing\n"\
                        + "	else \n"\
                         + "		make login item at end with properties {path: \"/Volumes/" + volumeName\
                          + "\", kind: Volume}\n"\
                           + "	end if\n"\
                            + "end tell\n"
                    success = self.execCommand(applescript, True)
                    sys.stdout.write("%s\n" %("success", "failed")[success])
                    
                else:
                    sys.stdout.write("try to remove login item if exists... \n")
                    applescript = "tell application \"System Events\"\n"\
                     + "	get the name of every login item\n"\
                      + "	if login item \"" + volumeName + "\" exists \n"\
                       + "		delete login item \"" + volumeName + "\"\n"\
                        + "	else \n"\
                         + "		-- do nothing\n"\
                          + "	end if\n"\
                           + "end tell\n"
                    success = self.execCommand(applescript, True)
                    sys.stdout.write("%s\n" %("success", "failed")[success])
            else:
                sys.stdout.write("cannot mount: %s\n" %webdavUrl)
                sys.stdout.write("%s\n" %self.execContent)
                if os.path.exists(os.path.abspath(node)):
                    self.execCommand("/sbin/umount -f " + os.path.abspath(node.name))
                    os.remove(os.path.abspath(node))
                self.currentMountIsPersistent = False
                self.currentMountNode = ""
            return success
        except Exception as e:
            e.printStackTrace()
            self.error = e.getMessage()
            return False

    def _removeMount(self):
        """ generated source for method _removeMount """
        info = FileActions.loadHashMap(os.path.join(self.appFolder, self.dmsId, "mount_" + self.userId + ".json"))
        success = False
        
        if info != None and info.has_key("node"):
            if success:
                print "umounted -f " + info.get("node")
                node = info.get("node","")
                node.delete()
                FileActions.saveHashMap(None, self.appFolder, self.dmsId, "mount_" + self.userId + ".json")
                self.execCommand("disktool -r")
                self.currentMountNode = ""
                self.currentMountIsPersistent = False
            else:
                print "cannot umounted " + info.get("node")
            print "try to remove login item if exists... ",
            path = info.get("node").split("/")
            if path[len(path) - 1]:
                volumeName = path[:path.length - 2]
            else:
                volumeName = path[:path.length - 1]
            #node = os.path.join("/Volumes/", volumeName)
            
            applescript = "tell application \"System Events\"\n"\
                + "    get name of every login item\n"\
                + "    if login item \""+volumeName+"\" exists \n"\
                + "        delete login item \""+volumeName+"\"\n"\
                + "    else \n"\
                + "        -- do nothing\n"\
                + "    end if\n"\
                + "end tell\n"
            success = self.execCommand({"osascript", "-e", applescript}, True)
            sys.stdout.write("%s\n" %("succeeded", "failed")[success])
            return success
        return False

    def _openMount(self):
        """ generated source for method _openMount """
        node = self.currentMountNode
        success = False
        
        mountName = "/Volumes/".replace("", node)
        applescript = "tell application \"Finder\"\n"\
                + "    make new Finder window to disk \""+mountName+"\"\n"\
                + "    activate\n"\
                + "end tell"
            
        if not self.currentMountNode == "":
            if not node.exists():
                self.currentMountNode = ""
                self._createMount(False)
                success = True
                if not node.exists():
                    success = False
                    return success
                
            if success:
                print "opened " + self.currentMountNode
            else:
                print self.execContent
                print "cannot open disk " + mountName
            return success
        else:
            print "no mount found"
            success = False
        return success

    @classmethod
    def parseLongFromString(cls, str_):
        """ generated source for method parseLongFromString """
        if str_ == None or str_.matches(""):
            return 0
        if not str_.matches("^[-]?\\d+$"):
            print str_ + " cannot be cast to long"
            return 0
        return long(str_)

    @classmethod
#    @overloaded
    def isMore(cls, a, b):
        """ generated source for method isMore """
        return cls.parseLongFromString(a) > b

    @classmethod
    @isMore.register(object, str, long)
    def isMore_0(cls, a, b):
        """ generated source for method isMore_0 """
        return cls.parseLongFromString(a) > b

    @classmethod
#    @overloaded
    def doesNotEqual(cls, a, b):
        """ generated source for method doesNotEqual """
        return cls.parseLongFromString(a) != b

    @classmethod
    @doesNotEqual.register(object, str, long)
    def doesNotEqual_0(cls, a, b):
        """ generated source for method doesNotEqual_0 """
        return cls.parseLongFromString(a) != b

    @classmethod
    def strReplace(cls, search, replace, subject):
        """ generated source for method strReplace """
        return subject.replace(search, replace)

    @classmethod
    def getFileNameExtension(cls, fileName):
        """ generated source for method getFileNameExtension """
        dot = fileName.lastIndexOf(".")
        extension = fileName.substring(dot + 1)
        if extension != None and 5 <= len(extension):
            return extension
        else:
            return ""

    @classmethod
#    @overloaded
    def bitesToStr(cls, bites):
        """ generated source for method bitesToStr """
        if bites < 1024:
            return bites + " bites"
        elif bites < 1024 * 1024:
            return (bites / 1024) + " Kb"
        elif bites < 1024 * 1024 * 1024:
            return (bites / 1024 / 1024) + " Mb"
        elif bites < 1024 * 1024 * 1024 * 1024:
            return (bites / 1024 / 1024 / 1024) + " Gb"
        elif bites < 1024 * 1024 * 1024 * 1024 * 1024:
            return (bites / 1024 / 1024 / 1024 / 1024) + " Tb"
        else:
            return bites + ""

    @classmethod
    @bitesToStr.register(object, float)
    def bitesToStr_0(cls, bitesFloat):
        """ generated source for method bitesToStr_0 """
        return long(round(bitesFloat) + "")

    _tr = dict()

#    @overloaded
    def tr(self, phrases, replaces):
        """ generated source for method tr """
        tr = dict()
        if self._tr == None:
            self._tr = dict()
        get = []
        i = 0
        while i < len(phrases):
            if self._tr.has_key(phrases.get(i)):
                tr.put(phrases.get(i), self._tr.get(phrases.get(i)))
            else:
                get.add(phrases.get(i))
            i += 1
        q = str()
        phrase = str()
        line = str()
        jsonString = self.getTransponderContent("action=translate"+q)
        newTr = dict(json.loads(jsonString))
        if len(get) > 0:
            while i < len(get):
                pass
                i += 1
            if newTr != None:
                while i < len(get):
                    phrase = get.get(i).__str__()
                    if newTr.get(phrase) == None:
                        line = phrase
                    else:
                        newTr.get(phrase).__str__()
                    print "translate '" + phrase + "' to '" + line + "'"
                    self._tr[phrase] = line
                    tr[phrase] = self._tr.get(phrase)
                    i += 1
            else:
                while i < len(get):
                    phrase = get.get(i).__str__()
                    self._tr[phrase] = phrase
                    tr[phrase] = self._tr.get(phrase)
                    i += 1
        if replaces != None:
            while i < len(phrases):
                r = replaces.get(i)
                if r != None and not r.isEmpty():
                    phrase = phrases.get(i).__str__()
                    line = tr.get(phrase).__str__()
                    ii = 0
                    while ii < len(r):
                        search = r.keySet().toArray()[ii].__str__()
                        replace = r.get(search).__str__()
                        if search and replace:
                            line = self.strReplace(search, replace, line)
                        ii += 1
                    tr.put(phrase, line)
                i += 1
        return tr

    #@tr.register(object, ArrayList)
    def tr_0(self, phrases):
        """ generated source for method tr_0 """
        return self.tr(phrases, None)

    #@tr.register(object, str, HashMap)
    def tr_1(self, phrase, replace):
        """ generated source for method tr_1 """
        phrases = []
        phrases.append(phrase)
        replaces = []
        replaces.add(replace)
        tr = self.tr(phrases, replaces)
        return tr.get(phrase).__str__()

    @tr.register(object, str, str, str)
    def tr_2(self, phrase, search, replace):
        """ generated source for method tr_2 """
        phrases = []
        phrases.append(phrase)
        replaces = []
        r = dict()
        r.put(search, replace)
        replaces.add(r)
        tr = self.tr(phrases, replaces)
        return tr.get(phrase).__str__()

    @tr.register(object, str)
    def tr_3(self, phrase):
        """ generated source for method tr_3 """
        phrases = []
        phrases.append(phrase)
        tr = self.tr(phrases, None)
        return tr.get(phrase).__str__()

    def getParentFrame(self):
        """ generated source for method getParentFrame """
        c = self
        while c != None:
            if isinstance(c, wx.Frame):
                return c
            c = c.getParent()
        return None

    def getJavaVersion(self):
        """ generated source for method getJavaVersion """
        v = self.javaVersion
        if v.matches("^(\\d+\\.\\d+).*$"):
            return float(v.replaceAll("^(\\d+\\.\\d+).*$", "$1"))
        else:
            return -1

    def getFullJavaVersion(self):
        """ generated source for method getFullJavaVersion """
        return self.javaVersion

    def getProgress(self):
        """ generated source for method getProgress """
        pmap = dict()
        pmap["description"] = self.progressDescription
        pmap["total"] = str(self.progressTotal)
        pmap["done"] = self.progressDone
        pmap["totalKb"] = str(self.progressTotal)
        pmap["doneKb"] = self.progressDone
        pmap["totalMb"] = str(self.progressTotal / 1024)
        pmap["doneMb"] = str(self.progressDone / 1024)
        return json.dumps(pmap)

    def resetProgress(self):
        """ generated source for method resetProgress """
        self.progressDescription = ""
        self.progressDone = 0
        self.progressTotal = 0

    def isBusy(self):
        """ generated source for method isBusy """
        return self.busy

    class commandTransporter(object):
        """ generated source for class commandTransporter """
        name = ""
        parameters = []

        def __init__(self, name):
            """ generated source for method __init__ """
            self.name = name

        def addParameter(self, par):
            """ generated source for method addParameter """
            self.parameters.add(par.__str__())
            return len(self.parameters) - 1

        def getParameter(self, i):
            """ generated source for method getParameter """
            return self.parameters.get(i).__str__()

        def equals(self, n):
            """ generated source for method equals """
            return False if n == None else n == self.name

    def addCommandTransporter(self, cmd):
        """ generated source for method addCommandTransporter """
        if not self.cmds.contains(cmd):
            self.cmds.add(cmd)

    def browseAndUploadInDmsFolder(self, browseType, browseTitle, folderId):
        """ generated source for method browseAndUploadInDmsFolder """
        cmd = self.commandTransporter("browseAndUploadInDmsFolder")
        cmd.addParameter(browseType)
        cmd.addParameter(browseTitle)
        cmd.addParameter(folderId)
        self.addCommandTransporter(cmd)
        self.busy = True
        return True

    def browseAndUploadItemVersion(self, itemId):
        """ generated source for method browseAndUploadItemVersion """
        cmd = self.commandTransporter("browseAndUploadItemVersion")
        cmd.addParameter(itemId)
        self.addCommandTransporter(cmd)
        self.busy = True
        return True

    def getUploadInfo(self):
        """ generated source for method getUploadInfo """
        return json.dumps(self.uploadInfo)

    def browseAndDownloadItems(self, itemsJson):
        """ generated source for method browseAndDownloadItems """
        cmd = self.commandTransporter("browseAndDownloadItems")
        cmd.addParameter(itemsJson)
        self.addCommandTransporter(cmd)
        self.busy = True
        return True

#    @overloaded
    def openDmsItem(self, itemId):
        """ generated source for method openDmsItem """
        cmd = self.commandTransporter("openItem")
        cmd.addParameter(itemId)
        cmd.addParameter("")
        self.addCommandTransporter(cmd)
        self.busy = True
        return True

    @openDmsItem.register(object, str, str)
    def openDmsItem_0(self, itemId, mode):
        """ generated source for method openDmsItem_0 """
        cmd = self.commandTransporter("openItem")
        cmd.addParameter(itemId)
        cmd.addParameter(mode)
        self.addCommandTransporter(cmd)
        self.busy = True
        return True

    def printDmsItem(self, itemId):
        """ generated source for method printDmsItem """
        cmd = self.commandTransporter("printItem")
        cmd.addParameter(itemId)
        self.addCommandTransporter(cmd)
        self.busy = True
        return True

    def getSetting(self, name):
        """ generated source for method getSetting """
        if name != None and not name == "" and self.settings.has_key(name) and self.settings != None:
            return self.settings.get(name).__str__()
        return ""

    def setSetting(self, name, value):
        """ generated source for method setSetting """
        if name == None or name == "":
            return False
        if self.settings == None:
            self.settings = dict()
        if value == None or value == "":
            self.settings.remove(name)
        else:
            self.settings.put(name, value)
        cmd = self.commandTransporter("updateSettings")
        self.addCommandTransporter(cmd)
        return True

    def getMyNetUseLetter(self):
        """ generated source for method getMyNetUseLetter """
        return self.myNetUseLetter

    def getCurrentNetUseLetter(self):
        """ generated source for method getCurrentNetUseLetter """
        return self.currentNetUseLetter

    def currentNetUseIsPersistent(self):
        """ generated source for method currentNetUseIsPersistent """
        return self.currentNetUseIsPersistent

    def getNetUse(self):
        """ generated source for method getNetUse """
        if not OS.isWindows():
            return False
        cmd = self.commandTransporter("getNetUse")
        self.addCommandTransporter(cmd)
        return True

    def getNetUseLetters(self):
        """ generated source for method getNetUseLetters """
        if not OS.isWindows():
            return ""
        return json.dumps(self.netUseLetters)

#    @overloaded
    def createNetUse(self, letter, persistent="no"): 
        """ generated source for method createNetUse """
        if not OS.isWindows():
            return False
        if 1 != len(letter):
            return False
        cmd = self.commandTransporter("createNetUse")
        cmd.addParameter(letter)
        cmd.addParameter(("yes" if persistent == "yes" else "no"))
        self.addCommandTransporter(cmd)
        return True

    @createNetUse.register(object, str)
    def createNetUse_0(self, letter):
        """ generated source for method createNetUse_0 """
        return self.createNetUse(letter, "no")

    def openNetUse(self, letter):
        """ generated source for method openNetUse """
        if not OS.isWindows():
            return False
        letter = letter.toUpperCase()
        if not letter.matches("^[D-Z]$"):
            return False
        cmd = self.commandTransporter("openNetUse")
        cmd.addParameter(letter)
        self.addCommandTransporter(cmd)
        return True

    def removeNetUse(self):
        """ generated source for method removeNetUse """
        if not OS.isWindows():
            return False
        if self.currentNetUseLetter.matches(""):
            return False
        cmd = self.commandTransporter("removeNetUse")
        self.addCommandTransporter(cmd)
        return True

    def createMount(self, persistent):
        """ generated source for method createMount """
        if OS.isWindows():
            return False
        cmd = self.commandTransporter("createMount")
        cmd.addParameter(persistent)
        self.addCommandTransporter(cmd)
        return True

    def removeMount(self):
        """ generated source for method removeMount """
        if OS.isWindows():
            return False
        cmd = self.commandTransporter("removeMount")
        self.addCommandTransporter(cmd)
        return True

    def openMount(self):
        """ generated source for method openMount """
        if OS.isWindows():
            return False
        cmd = self.commandTransporter("openMount")
        self.addCommandTransporter(cmd)
        return True

    def isMounted(self):
        """ generated source for method isMounted """
        return False if self.currentMountNode == "" else True

    def mountIsPersistent(self):
        """ generated source for method mountIsPersistent """
        return True if self.isMounted() and self.currentMountIsPersistent else False

    def resetStartupLink(self):
        """ generated source for method resetStartupLink """
        cmd = self.commandTransporter("resetStartupLink")
        self.addCommandTransporter(cmd)
        return True

    def cancel(self):
        """ generated source for method cancel """
        self.cancel = True
        self.progressDescription = "cancelling"
        return True

    def hasLockedItems(self):
        """ generated source for method hasLockedItems """
        if self.saving:
            return True
        lockAr = self.locks.keySet().toArray()
        lock = dict()
        i = 0
        while len(lockAr):
            lock = self.locks.get(lockAr[i])
            if lock.get("userId") == self.userId:
                return True
            i += 1
        return False

    def getLastError(self):
        """ generated source for method getLastError """
        return self.error

    def getExecContent(self):
        """ generated source for method getExecContent """
        return self.execContent + ""

    def setCookie(self, c):
        """ generated source for method setCookie """
        if not self.cookie == c:
            self.cookie = c

    class CommandChecker(Thread):
        """ generated source for class CommandChecker """
        #app = OfficeDrive_SE6()

        def __init__(self, app):
            """ generated source for method __init__ """
            super(__class__.__class___, self).__init__()
            self.app = app

        def run(self):
            """ generated source for method run """
            try:
                time.sleep(0.1)
            except Exception as e:
                Thread.__stop(self)
                e.printStackTrace()
            cmd = None
            while True:
                cmd = None
                if self.app.cmds.isEmpty():
                    try:
                        time.sleep(0.1)
                    except Exception as e:
                        Thread.__stop(self)
                        break
                    continue 
                else:
                    cmd = self.app.cmds.remove(0)
                self.app.cancel = False
                browseTypeStr = cmd.getParameter(0)
                if cmd == "browseAndUploadInDmsFolder":
                    if browseTypeStr == "files":
                        browseType = self.BROWSE_TYPE_MULTIPLE_FILES
                    elif browseTypeStr == "folder":
                        browseType = self.BROWSE_TYPE_ONE_FOLDER
                    elif browseTypeStr == "folders":
                        browseType = self.BROWSE_TYPE_MULTIPLE_FOLDERS
                    elif browseTypeStr == "fileAndFolder":
                        browseType = self.BROWSE_TYPE_ONE_FILE_OR_FOLDER
                    elif browseTypeStr == "filesAndFolders":
                        browseType = self.BROWSE_TYPE_MULTIPLE_FILES_OR_FOLDERS
                    else:
                        browseType = self.BROWSE_TYPE_ONE_FILE
                    
                    browseTitle = cmd.getParameter(1);
                    folderId = cmd.getParameter(2);
                    
                    self.app.browseForUpload(browseType, browseTitle)
                    if self.app.hasFilesInSelection:
                        self.app.evalJs("window['" + self.app.jsObj + "'].browseAndUploadInDmsFolder_onStart()")
                        try:
                            success = self.app.uploadSelectedFiles(folderId)
                            self.app.busy = False
                        except Exception as e:
                            print e.getMessage()
                        self.app.busy = False
                        self.app.evalJs("window['" + self.app.jsObj + "'].browseAndUploadInDmsFolder_onFinish(" + ("true" if success else "false") + ")")
                    else:
                        self.app.busy = False
                        self.app.evalJs("window['" + self.app.jsObj + "'].browseAndUploadInDmsFolder_onFinish(null)")
                    continue 
                itemId = cmd.getParameter(0);
                """
                elif cmd == "browseAndUploadItemVersion":
                    jsonString = self.app.getTransponderLine("action=getItemInfo&itemId=" + itemId);
                    if  jsonString.startsWith("{"):
                        remoteInfo = json.loads(jsonString)
                    if remoteInfo != None and remoteInfo.get("type").__str__() == "doc" and remoteInfo.get("writable").__str__() == "true":
                        ext = self.getFileNameExtension(remoteInfo.get("name").toString());
                        print "ext: " + ext
                        if ext != None and not ext.matches(""):
                            self.app.browseForUpload(self.BROWSE_TYPE_ONE_FILE, "upload", ext, "")
                        else:
                            self.app.browseForUpload(self.BROWSE_TYPE_ONE_FILE, "upload")
                        if self.app.selectedFiles[0].isFile() and len(length):
                            self.app.evalJs("window['" + self.app.jsObj + "'].browseAndUploadItemVersion_onStart()")
                            try:
                                success = self.app.uploadItemVersion(itemId)
                            except Exception as e:
                                print e.getMessage()
                            self.app.busy = False
                            self.app.evalJs("window['" + self.app.jsObj + "'].browseAndUploadItemVersion_onFinish(" + ("true" if success else "false") + ")")
                        else:
                            self.app.busy = False
                            self.app.evalJs("window['" + self.app.jsObj + "'].browseAndUploadItemVersion_onFinish(null)")
                    self.app.busy = False
                    """
                itemId = cmd.getParameter(0)
                force = cmd.getParameter(1)
                mode = ""
                if cmd == "openItem":
                    if force == "force":
                        mode = "force"
                    elif force == "readOnly":
                        mode = "readOnly"
                    if mode == "":
                        ret = self.app.openItemOnDesktop(itemId)
                    else:
                        ret = self.app.openItemOnDesktop(itemId, mode)
                    self.app.busy = False
                    self.app.evalJs("window['" + self.app.jsObj + "'].openDmsItem_ret(\"" + ret + "\")")
                elif cmd == "createNetUse":
                    self.app.evalJs("window['" + self.app.jsObj + "'].createNetUse_ret(" + (1 if ret else 0) + ")")
                    self.app.busy = False
                elif cmd == "removeNetUse":
                    self.app.evalJs("window['" + self.app.jsObj + "'].removeNetUse_ret(" + (1 if ret else 0) + ")")
                    self.app.busy = False
                elif cmd == "openNetUse":
                    letter = cmd.getParameter(0)
                    persistent = cmd.getParameter(1)
                    try:
                        ret = FileActions.openOnDesktop(os.path.join(letter, ":\\"))
                        if ret != None:
                            print "open " + letter + ":\\"
                    except Exception as e:
                        pass
                    self.app.evalJs("window['" + self.app.jsObj + "'].openNetUse_ret(" + (1 if ret != None else 0) + ")")
                    self.app.busy = False
                elif cmd == "getNetUse":
                    self.app.evalJs("window['" + self.app.jsObj + "'].getNetUse_ret(" + (1 if ret else 0) + ")")
                    self.app.busy = False
                elif cmd == "resetStartupLink":
                    self.app.evalJs("window['" + self.app.jsObj + "'].resetStartupLink_ret(" + (1 if ret else 0) + ")")
                    self.app.busy = False
                elif cmd == "createMount":
                    self.app.evalJs("window['" + self.app.jsObj + "'].createMount_ret(" + (1 if ret else 0) + ")")
                    self.app.busy = False
                elif cmd == "removeMount":
                    self.app.evalJs("window['" + self.app.jsObj + "'].removeMount_ret(" + (1 if ret else 0) + ")")
                    self.app.busy = False
                elif cmd == "openMount":
                    self.app.evalJs("window['" + self.app.jsObj + "'].openMount_ret(" + (1 if ret else 0) + ")")
                    self.app.busy = False
                elif cmd == "updateSettings":
                    FileActions.saveHashMap(self.app.settings, self.appFolder, "settings.json")

    _killed = False

    def _kill(self):
        """ generated source for method _kill """
        if self._killed:
            return
        print self.__class__.__name__ + ".kill()"
        try:
            if self.commandChecker != None and self.commandChecker.isAlive():
                self.commandChecker.interrupt()
        except Exception as e:
            pass
        try:
            if self.fileChecker != None and self.fileChecker.isAlive():
                self.fileChecker.interrupt()
        except Exception as e:
            pass
        try:
            self.deleteOpenItems(True)
        except Exception as e:
            pass
        if OS.isWindows() and not self.currentNetUseLetter == "" and not self.currentNetUseIsPersistent:
            try:
                self.execCommand("net use " + self.currentNetUseLetter + ": /DELETE")
            except Exception as e:
                pass
        if self.isMounted() and not self.currentMountIsPersistent:
            try:
                self._removeMount()
            except Exception as e:
                pass
        try:
            self.cleanCash()
        except Exception as e:
            pass
        self._killed = True

    def kill(self, returnValue):
        """ generated source for method kill """
        self._kill()

    def unload(self):
        """ generated source for method unload """
        self._kill()

    def stop(self):
        """ generated source for method stop """
        self._kill()

