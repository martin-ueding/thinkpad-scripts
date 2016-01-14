# -*- coding: utf-8 -*-

# Copyright © 2016 Lukasz Czuja <pub@czuja.pl>
# Licensed under The GNU Public License Version 2 (or later)

import os

def fileExists(file):
    return os.path.exists(file)

def fileReadBoolean(file, errMsg):
    return fileReadInt(file, errMsg) == 1
    
def fileReadHex(file, errMsg):
    return int(fileRead(file, errMsg), 16)
    
def fileReadInt(file, errMsg):
    return int(fileRead(file, errMsg))

def fileRead(file, errMsg):
    try:
        with open(file, 'r') as f:
            return f.read().strip()
    except IOError:
        logger.error(errMsg)
        raise

def fileWriteBoolean(file, errMsg, data):
    return fileWriteInt(file, errMsg, 1 if data else 0)
    
def fileWriteHex(file, errMsg, data):
    return fileWrite(file, errMsg, hex(data))
    
def fileWriteInt(file, errMsg, data):
    return fileWrite(file, errMsg, str(data))

def fileWrite(file, errMsg, data):        
    try:
        with open(file, 'w') as f:
            f.write(str(data))
        return True
    except IOError:
        logger.error(errMsg)
        return False
