#!/usr/bin/env python

""" Des Encrypter """


import pyDes


class DesEncrypter(object):
    """ generated source for class DesEncrypter """
   
    def __init__(self):
        """ generated source for method __init__ """
        #  Create an 8-byte initialization vector
      
    def encrypt(self, in_, out):
        """ generated source for method encrypt """
        try:
            #  Bytes written to out will be encrypted
            out.write(pyDes.des.encrypt(self, in_.read()))
            
        except Exception as e:
            print e
            pass


    def encrypt_0(self, inFile, outFile):
        """ generated source for method encrypt_0 """
        in_ = open(inFile, "r")
        out = open(outFile, "w")
        self.encrypt(in_, out)
        in_.close()
        out.close()

    def decrypt(self, in_, out):
        """ generated source for method decrypt """
        try:
            #  Bytes read from in will be decrypted
            
            out.write(pyDes.des.decrypt(in_.read()))
            #  Read in the decrypted bytes and write the cleartext to out
            out.close()
        except Exception as e:
            print e
            pass

    
    def decrypt_0(self, inFile, outFile):
        """ generated source for method decrypt_0 """
        in_ = open(inFile, "r")
        out = open(outFile, "w")
        self.decrypt(in_, out)
        in_.close()
        out.close()

