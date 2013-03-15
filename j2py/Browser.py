#!/usr/bin/env python
""" generated source for module Browser """

class Browser(object):
    """ generated source for class Browser """
    browser = {}

    def __init__(self, info=None):
        """ generated source for method __init__ """
        self.browser = info

    def getBrowserType(self):
        """ generated source for method getBrowserType """
        if self.browser != None and self.browser.containsKey("type"):
            return str(self.browser.get("type"))
        else:
            return "unknown"

    def isIE(self):
        """ generated source for method isIE """
        return (self.getBrowserType() == "Internet Explorer")

    def isSafari(self):
        """ generated source for method isSafari """
        return (self.getBrowserType() == "Safari")

