#!/usr/bin/env python3

# Knowledge:
# AES: Advanced Encryption Standard
# Symmetric Cipher
# 16 byte block size: each part of the encrypted data is
# encrypted 16 bytes, it must be full, so padding is required.
# The keys can be 128, 192 or 256 bits long
# IV: stands for initialization vector

import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import main

def encrypt(key, filename):
    chunksize = 64*1024
    outputFile ="enc_"+ filename +".hacklab"
    filesize = str(os.path.getsize(filename)).zfill(16)
    IV = Random.new().read(16)

    encryptor = AES.new(key, AES.MODE_CBC, IV)

    with open(filename, 'rb') as infile:
        with open(outputFile, 'wb') as outfile:
            outfile.write(filesize.encode('utf-8'))
            outfile.write(IV)

            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - (len(chunk) % 16))

                outfile.write(encryptor.encrypt(chunk))

def decrypt(key, filename):
    chunksize = 64*1024
    outputFile ="dec_" + filename.split('.hacklab')[0] 

    with open(filename, 'rb') as infile:
        filesize = int(infile.read(16))
        IV = infile.read(16)

        decryptor = AES.new(key, AES.MODE_CBC, IV)

        with open(outputFile, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break

                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(filesize)

def getKey(password):
    hasher = SHA256.new(password)
    return hasher.digest()


# if __name__ == "__main__":
#     main.Main()