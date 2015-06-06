#!/usr/bin/env python

def asciiToByes(x):
    try:
        return(bytes)
    except:
        return bytes(x, 'ascii')