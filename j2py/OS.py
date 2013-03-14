#!/usr/bin/env python
""" generated source for module OS """

import sys

class OS(object):
    """ generated source for class OS """
    @classmethod
    def getName(cls):
        """ generated source for method getName """
        if cls.name == None:
            cls.name = sys.platform.lower()
        return cls.name
    
    @classmethod
    def isWindows(cls):
        """ generated source for method isWindows """
        return OS.getName().indexOf("windows") != -1 or OS.name.indexOf("nt") != -1

    @classmethod
    def isWindows9X(cls):
        """ generated source for method isWindows9X """
        return getName() == "windows 95" or name == "windows 98"

    @classmethod
    def isWindows7(cls):
        """ generated source for method isWindows7 """
        return getName() == "windows 7" or name == "windows 98"

    @classmethod
    def isMac(cls):
        """ generated source for method isMac """
        return getName().startsWith("mac")

    @classmethod
    def isLinux(cls):
        """ generated source for method isLinux """
        return getName().indexOf("linux") != -1

    @classmethod
    def isSolaris(cls):
        """ generated source for method isSolaris """
        return getName().indexOf("solaris") != -1

    @classmethod
    def version(cls):
        """ generated source for method version """
        vv = getVersion().split("\\.")
        v = ""
        if vv[0].matches("^\\d+$") and len(vv):
            v = vv[0]
        if vv[1].matches("^\\d+$") and len(vv):
            v = v + "." + vv[1]
        if vv[2].matches("^\\d+$") and len(vv):
            v = v + vv[2]
        if not v == "":
            return Float.parseFloat(v)
        return 0

    @classmethod
    def is64bits(cls):
        """ generated source for method is64bits """
        return True if getArch().indexOf("64") > -1 else False

    @classmethod
    def description(cls):
        """ generated source for method description """
        return getName() + ", version: " + getVersion() + ", architecture: " + getArch()

    name = str()
    version = str()
    arch = str()



    @classmethod
    def getVersion(cls):
        """ generated source for method getVersion """
        if cls.version == None:
            cls.version = System.getProperty("os.version").lower()
        return cls.version

    @classmethod
    def getArch(cls):
        """ generated source for method getArch """
        if cls.arch == None:
            cls.arch = System.getProperty("os.arch").lower()
        return cls.arch

