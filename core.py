#!/usr/bin/python
# -*- coding: utf-8 -*-

from struct import *

from PyQt4 import QtCore

#from main import FFTCanvas, SignalCanvas

class Acquire(QtCore.QObject):
    """Class which acquires automaticaly with 1kHz"""

    def start(self):
        self.timer = QtCore.QTimer(self)
        #QtCore.QObject.connect(timer, QtCore.SIGNAL("timeout()"), self.acquire)
        self.timer.timeout.connect(self.acquire)
        self.timer.start(1000)
        print timer.isActive()
        print "Acquire class initialized"


    def acquire(self):
        print "acquire function called"
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
        print "Sending signal with", len(output), "probes."
        self.emit(QtCore.SIGNAL('update_plots(PyQt_PyObject)'), output)
