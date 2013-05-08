#!/usr/bin/python
# -*- coding: utf-8 -*-

from struct import *


def acquire(samples, delete):
    acquireSource = 'exampleInput'
    print 'Acquire started from ' + acquireSource
    file = open(acquireSource, 'r')
    
    samples = 1000
    output = []
    for i in range(samples):
        value = file.readline()
        while not value:
            value = file.readline()
        """Reading data"""
        value = value[:-1]
        #print '----------'
        #print value
        #print '----------'
        """Deleting \n"""
        try:
            number = unpack('H', value)
            output.append(number[0])
            #print number[0]
        except error:
            print 'Wrong number'
        samples -= 1
    
    return output
