#!/usr/bin/env python
""" generated source for module FileActions """

import os
import sys
import subprocess
import io
import gzip
import json
import urllib2
import urllib
import re
import md5

from shutil import copyfile
from shutil import move

from OS import OS

class FileActions(object):
    """ generated source for class FileActions """
    @classmethod
##   @overloaded
    def copy(cls, source, dest):
        """ generated source for method copy """
        try:
            if not dest.exists():
                dest.createNewFile()
            try:
                in_ = io.open(source, "r")
                out = io.open(dest, "w")
                out.write(in_.read())
                #out.transferFrom(in_, 0, len(in_))
            except (IOError) as e:
                e.printStackTrace()
            if in_ != None:
                in_.close()
            if out != None:
                out.close()
        except Exception as e:
            e.printStackTrace()

    @classmethod
#   @copy.register(object, File)
    def copy_0(cls, in_):
        """ generated source for method copy_0 """
        out = open(".tmp", "w")
        cls.copy(in_, out)
        return out

    @classmethod
#   @overloaded
    def move(cls, source, dest):
        """ generated source for method move """
        try:
            if os.path.exists(dest):
                os.remove(dest)
            move(source, dest)
            if not os.path.exists(source) and os.path.exists(dest):
                return dest
            else:
                return None
        except (Exception) as e:
            e.printStackTrace()
            return None

    @classmethod
 #   @move.register(object, str, str)
    def move_0(cls, source, dest):
        """ generated source for method move_0 """
        try:
            move(source, dest)
        except (Exception) as e:
            e.printStackTrace()
        return os.path.abspath(dest)

    @classmethod
 #   @overloaded
    def gzip(cls, inFile, outFile):
        """ generated source for method gzip """
        out = gzip.GzipFile(outFile, "w")
        in_ = open(inFile, "r")
        #buf = yourArbitraryBuffSizeHere
        len = int()
        #while (len = in_.read(buf)) > 0:
        out.write(in_.read())
        in_.close()
        out.close()
        
    @classmethod
#   @gzip.register(object, File)
    def gzip_0(cls, inFile):
        """ generated source for method gzip_0 """
        in_ = open(inFile, "r")
        outFile = gzip.GzipFile("./tmp/.gzip")
        outFile.write(in_.read())
        return outFile.name

    @classmethod
##   @overloaded
    def ungzip(cls, inFile, outFile):
        """ generated source for method ungzip """
        in_ = gzip.GzipFile(inFile, "r")
        out = open(outFile, "w")
        #buf = yourArbitraryBuffSizeHere
        #len = int()
        #while (len = in_.read(buf)) > 0:
        out.write(in_.read())
        out.close()
        in_.close()

    @classmethod
#    @ungzip.register(object, File)
    def ungzip_0(cls, inFile):
        """ generated source for method ungzip_0 """
        outFile = open("./tmp/.tmp", "w")
        cls.ungzip(inFile, outFile)
        os.remove(inFile)
        os.rename(outFile, inFile)

    @classmethod
#   @overloaded
    def openOnDesktop(cls, file_, readOnly):
        """ generated source for method openOnDesktop """
        if file_ == None or not file_.exists() or not file_.canRead():
            print "cannot find/read file " + file_
            return None
        #  SE 1.5 && SE 1.4{
        # 		return execOpenOnDesktop(file);
        #  }
        #  SE 1.6{
        Desktop = None
        try:
            if Desktop.isDesktopSupported():
                desktop = Desktop.getDesktop()
            desktop.open(file_.getCanonicalFile())
            return file_
        except Exception as e:
            sys.stdout.write("%s\n" %e)
            return cls.execOpenOnDesktop(file_)
        #  }

   # @classmethod
   # @openOnDesktop.register(object, File)
    def openOnDesktop_0(self, file_):
        """ generated source for method openOnDesktop_0 """
        return self.openOnDesktop(file_, False)

    @classmethod
    def execOpenOnDesktop(cls, file_):
        """ generated source for method execOpenOnDesktop """
        pattern = re.compile("[^a-zA-Z0-9_().-~]")
        matcher = pattern.matcher(file_.__name__)
        fileName = matcher.replaceAll("_")
        newFile = os.path.join(file_.getParent(), fileName)
        if not file_.__name__ == fileName:
            os.rename(file_, newFile)
            file_ = newFile
        f = os.path.abspath(file_)
        #r = Runtime.getRuntime()
        p = None
        if OS.isLinux():
            try:
                p = os.system("xdg-open \"%s\"" %f)
            except (Exception) as e:
                sys.stdout.write(e)
            # String subCmd = (exec) ? "exec" : "openURL";
        elif OS.isMac():
            try:
                p = os.system("open \"%s\"" %f)
            except (Exception) as e:
                sys.stdout.write(e)
        elif OS.isWindows():
            if OS.isWindows9X():
                try:
                    p = os.system("command.com /C start %s" %f)
                except (Exception) as e:
                    sys.stdout.write(e) 
                #  "command.com /C \"start " + f + "\""
            else:
                p = subprocess.Popen(["cmd.exe", "/C", "start", f], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                p.wait()
                res = p.stdout.readlines()
                if p.returncode:
                    for errLine in res:
                        if errLine.startswith("\\\\"):
                            UNCError = True
                        else:
                            sys.stdout.write(" >%s" %errLine)
                    return None
                else:
                    return file_
                    
                
    @classmethod
    def getLockFile(cls, file_):
        """ generated source for method getLockFile """
        if file_ == None:
            return None
        s = os.path.sep
        lockFile = None
        lockFile = os.path.join(file_.getParent(), "~$" + file_.__name__.substring(2))
        if lockFile.exists():
            return lockFile
        lockFile = os.path.join(file_.getParent(), "~$" + file_.__name__)
        if lockFile.exists():
            return lockFile
        lockFile = os.path.join(file_.getParent(), ".~lock." + file_.__name__ + "#")
        if lockFile.exists():
            return lockFile
        else:
            return None

    @classmethod
    def isLockedByTmpFile(cls, file_):
        """ generated source for method isLockedByTmpFile """
        lockFile = cls.getLockFile(file_)
        if lockFile != None:
            return True
        else:
            return False

    @classmethod
    def isLockedByFileSystem(cls, file_):
        """ generated source for method isLockedByFileSystem """
        if not file_.exists():
            return False
        locked = False
        fos = open(file_)
        try:
            fos.close()
        except Exception as e:
            locked = True
        return locked

    @classmethod
    def isLockedByAnyMethod(cls, file_):
        """ generated source for method isLockedByAnyMethod """
        locked = cls.isLockedByTmpFile(file_)
        if locked:
            return True
        else:
            return cls.isLockedByFileSystem(file_)

    @classmethod
    def deleteDir(cls, dir):
        """ generated source for method deletedir_ """
        if not dir.exists():
            return False
        files = dir.listFiles()
        i = 0
        while len(files):
            if files[i].isDirectory():
                cls.deleteDir(files[i])
            else:
                files[i].delete()
            i += 1
        if dir.delete():
            return True
        else:
            dir.deleteOnExit()
            return False

    @classmethod
##   @overloaded
    def getContents(cls, file_):
        """ generated source for method getContents """
        return cls.getContents_0(cls, file_)

    @classmethod
#    @getContents.register(object, File)
    def getContents_0(cls, file_):
        """ generated source for method getContents_0 """
        if not os.path.exists(file_):
            return None
        contents = ""
        try:
            try:
                in_ = open(file_)
                contents = in_.readlines()
            finally:
                in_.close()
        except (IOError) as ex:
            ex.printStackTrace()
        finally:
            return contents.__str__()

    @classmethod
##   @overloaded
    def setContents(cls, file_, contents):
        """ generated source for method setContents """
        cls.setContents_0(file_, contents)

    @classmethod
#   @setContents.register(object, File, str)
    def setContents_0(cls, file_, contents):
        """ generated source for method setContents_0 """
        if file_ == None:
            return False
        if contents == None:
            return False
        try:
            try:
                output = open(file_, "w")
                output.write(contents)
            finally:
                output.close()
        except (Exception) as e:
            sys.stdout.write(e)
            return False
        return True

    @classmethod
#   @overloaded
    def saveHashMap(cls, map, file_):
        """ generated source for method saveHashMap """
        return cls.saveHashMap(map, file_)

    @classmethod
#    @saveHashMap.register(object, HashMap, File)
    def saveHashMap_0(cls, map_, file_):
        """ generated source for method saveHashMap_0 """
        if map_ == None:
            file_.delete()
            return True
        return cls.setContents(file_, json.dumps(map_))

    @classmethod
#   @overloaded
    def loadHashMap(cls, file_):
        """ generated source for method loadHashMap """
        jsonString = cls.getContents(file_)
        if jsonString == None or not jsonString.startswith("{"):
            return dict()
        map_ = json.loads(json)
        return map_

    @classmethod
#    @loadHashMap.register(object, str)
    def loadHashMap_0(cls, file_):
        """ generated source for method loadHashMap_0 """
        return cls.loadHashMap(file_)

 #   complete = MessageDigest()

    @classmethod
    def createChecksum(cls, filename):
        """ generated source for method createChecksum """
        fis = io.open(filename)
        buffer_ = buffer()
        if cls.complete == None:
            cls.complete = md5.md5()
        else:
            cls.complete.reset()
        len = int()
        while True:
            len = fis.read(buffer_)
            if len > 0:
                cls.complete.update(buffer_, 0, len)
            if not ((len != -1)):
                break
        fis.close()
        return cls.complete.digest()

    @classmethod
#   @overloaded
    def MD5(cls, file_):
        """ generated source for method MD5 """
        return cls.MD5(os.path.abspath(file_))

    @classmethod
#    @MD5.register(object, str)
    def MD5_0(cls, fileName):
        """ generated source for method MD5_0 """
        file_ = fileName
        if not os.path.exists(file_):
            return ""
        md5 = ""
        b = cls.createChecksum(fileName)
        try:
            i = 0
            while len(b):
                md5 += str((b[i] & 0xff) + 0x100, 16).substring(1)
                i += 1
        except Exception as e:
            print e.getMessage()
            return ""
        return md5

    @classmethod
    def equal(cls, one, two):
        """ generated source for method equal """
        return cls.MD5(one) == cls.MD5(two)

    @classmethod
    def getWorkingDirectory(cls, appName):
        """ generated source for method getWorkingDirectory """
        s = os.path.sep
        userHome = System.getProperty("user.home", ".")
        dir_ = File()
        if OS.isLinux():
            dir_ = File(userHome, s + appName)
        elif OS.isSolaris():
            dir_ = File(userHome + s + appName)
        elif OS.isWindows():
            if applicationData != None:
                dir_ = File(applicationData + s + appName)
            else:
                dir_ = File(userHome + s + appName)
        elif OS.isMac():
            dir_ = File(userHome, "Library" + s + "Application Support" + s + appName)
        else:
            dir_ = File(".")
        if not dir.exists() and not dir.mkdirs():
            dir_ = File(System.getProperty("java.io.tmpdir"))
            dir_ = File(dir.getAbsoluteFile() + ("" if dir.getAbsolutePath().endsWith(s) else s) + appName)
            if not dir.exists():
                dir.mkdirs()
        return dir.getAbsolutePath()

    @classmethod
    def getDirSyncInfo(cls, dir_):
        """ generated source for method getDirSyncInfo """
        if dir_ == None or not os.path.exists(dir_) or not os.path.isdir(dir_) or os.path.dirname(dir_) == ".officedrive":
            return None
        s = os.path.sep
        infoFile = os.path.join(os.path.abspath(dir), ".OfficeDrive.syncinfo.json#1.0")
        dirInfo = None
        if infoFile.exists():
            dirInfo = json.load(infoFile)
        else:
            if OS.isWindows():
                try:
                    infoFile.createNewFile()
                    Runtime.getRuntime().exec_("attrib +h \"" + infoFile.getAbsolutePath() + "\"")
                except Exception as e:
                    print "could not create or hide " + infoFile.getAbsolutePath()
            dirInfo = HashMap()
        fileInfo = HashMap()
        files = dir.listFiles()
        file_ = File()
        LM = long()
        updated = False
        i = 0
        while len(files):
            file_ = files[i]
            if dirInfo.has_key(file_.__name__):
                fileInfo = dirInfo.get(file_.__name__)
            else:
                fileInfo = HashMap()
            LM = long(file_.lastModified())
            if not fileInfo.has_key("LM") or long(fileInfo.get("LM")) != LM or not fileInfo.has_key("MD5") or fileInfo.get("MD5") == "":
                fileInfo.put("LM", LM)
                fileInfo.put("MD5", cls.MD5(file_))
                updated = True
            i += 1
        keys = dirInfo.keySet().toArray()
        i = 0
        while len(keys):
            file_ = File(dir.getAbsoluteFile() + s + keys[i])
            if not file_.exists():
                dirInfo.remove(keys[i])
                updated = True
            i += 1
        if updated:
            cls.saveHashMap(dirInfo, infoFile)
        return dirInfo

    @classmethod
    def getFileSyncInfo(cls, file_):
        """ generated source for method getFileSyncInfo """
        if file_ == None or not file_.exists() or not file_.isFile() or file_.__name__ == ".officedrive":
            return None
        s = os.path.sep
        dir_ = file_.getParentFile()
        if dir_ == None:
            return None
        LM = long(file_.lastModified())
        fileInfo = None
        infoFile = open(dir.getAbsolutePath() + s + ".OfficeDrive.syncinfo.json#1.0", "w")
        dirInfo = cls.loadHashMap(infoFile)
        if dirInfo.has_key(file_.__name__):
            fileInfo = dirInfo.get(file_.__name__)
        if fileInfo == None or not fileInfo.has_key("LM") or long(fileInfo.get("LM")) != LM or not fileInfo.has_key("MD5") or fileInfo.get("MD5") == "":
            fileInfo.put("LM", LM)
            fileInfo.put("MD5", cls.MD5(file_))
            if sys.platform == "win32":
                try:
                    os.system("attrib +h \"" + os.path.abspath(infoFile.name) + "\"")
                except Exception as e:
                    print "could not create or hide " + os.path.abspath(infoFile.name)
            cls.saveHashMap(dirInfo, infoFile)
        return fileInfo

    @classmethod
    def isCompressedFileType(cls, f):
        """ generated source for method isCompressedFileType """
        return f != None and f.__name__.matches("(?i:.*\\.(zip|gz|rar|jar|bz2|gif|png|jpg|tif|psd|ai|gz|tgz|mp3|mpeg|wav|mp4|m4a|m4p|avi|fla|flv|exe|xlsx|docx|pptx|wma|wmv))$")

    @classmethod
##   @overloaded
    def downloadUrlToFile(cls, url, file_):
        """ generated source for method downloadUrlToFile """
        try:
            conn = urllib2.urlopen(url)
            
            # conn.setUseCaches(True)
            # conn.setDoInput(True)
            
            if conn.getcode() / 100 != 2:
                print "could connect to " + url.__str__()
                return False
       
            try:
                # out
                bufferSize = 1024*7
                out = io.open(file_, "wb")
                in_ = conn.fp               
                out.write(in_.read(bufferSize))
                in_.close()
                out.close()
                return True
            except Exception as e:
                e.printStackTrace()
                return False

        except Exception as e:
            e.printStackTrace()
            return False

        #  @downloadUrlToFile.register(object, str, File)
        def downloadUrlToFile_0(cls, url, file_):
            """ generated source for method downloadUrlToFile_0 """
            try:
                return cls.downloadUrlToFile(url, file_)
            except (Exception) as e:
                e.printStackTrace()
                return False
        
