#!/usr/bin/env python
""" generated source for module DesEncrypter """
import os
import cipher


class DesEncrypter(object):
    """ generated source for class DesEncrypter """
    ecipher = Cipher()
    dcipher = Cipher()
    buf = [None]*1024

    def __init__(self, passw):
        """ generated source for method __init__ """
        #  Create an 8-byte initialization vector
        salt = [None]*
        #  Iteration count
        iterationCount = 19
        try:
            #  Create key
            self.ecipher = Cipher.getInstance(key.getAlgorithm())
            self.dcipher = Cipher.getInstance(key.getAlgorithm())
            self.ecipher.init(Cipher.ENCRYPT_MODE, key, paramSpec)
            self.dcipher.init(Cipher.DECRYPT_MODE, key, paramSpec)
        except java.security.InvalidAlgorithmParameterException as e:
            pass
        except java.security.spec.InvalidKeySpecException as e:
            pass
        except javax.crypto.NoSuchPaddingException as e:
            pass
        except java.security.NoSuchAlgorithmException as e:
            pass
        except java.security.InvalidKeyException as e:
            pass

    @overloaded
    def encrypt(self, in_, out):
        """ generated source for method encrypt """
        try:
            #  Bytes written to out will be encrypted
            out = CipherOutputStream(out, self.ecipher)
            #  Read in the cleartext bytes and write to out to encrypt
            while (numRead = in_.read(self.buf)) >= 0:
                out.write(self.buf, 0, numRead)
            out.flush()
            out.close()
        except java.io.IOException as e:
            pass

    @encrypt.register(object, File, File)
    def encrypt_0(self, inFile, outFile):
        """ generated source for method encrypt_0 """
        in_ = FileInputStream(inFile)
        out = FileOutputStream(outFile)
        self.encrypt(in_, out)
        in_.close()
        out.close()

    @overloaded
    def decrypt(self, in_, out):
        """ generated source for method decrypt """
        try:
            #  Bytes read from in will be decrypted
            in_ = CipherInputStream(in_, self.dcipher)
            #  Read in the decrypted bytes and write the cleartext to out
            while (numRead = in_.read(self.buf)) >= 0:
                out.write(self.buf, 0, numRead)
            out.close()
        except java.io.IOException as e:
            pass

    @decrypt.register(object, File, File)
    def decrypt_0(self, inFile, outFile):
        """ generated source for method decrypt_0 """
        in_ = FileInputStream(inFile)
        out = FileOutputStream(outFile)
        self.decrypt(in_, out)
        in_.close()
        out.close()

