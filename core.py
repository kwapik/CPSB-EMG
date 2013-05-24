#!/usr/bin/python
# -*- coding: utf-8 -*-

from bluetooth import *
import io
import time
from struct import *

from PyQt4 import QtCore

#from main import FFTCanvas, SignalCanvas

class Acquire(QtCore.QObject):
    """Class which acquires automaticaly with 1kHz"""
    timer = None
    sock = None

    def start(self):
        self.timer = QtCore.QTimer(self)
        #QtCore.QObject.connect(timer, QtCore.SIGNAL("timeout()"), self.acquire)
        self.timer.timeout.connect(self.acquire)
        self.timer.start(1000)
	self.init_BT()
        print "Acquire class initialized"
    
    def init_BT(self):
	server_address = "00:12:10:25:02:43"
	port = 1
	self.sock = BluetoothSocket(RFCOMM)
	self.sock.connect((server_address, port))

    def acquire(self):
        print "acquire function called"
        #acquireSource = '/dev/rfcomm0'
        #print 'Acquire started from ' + acquireSource
        #f = io.open(acquireSource, 'rb')
    
        samples = 1000
        output = []
	source = []
	a = time.localtime()
	#for i in xrange(samples):
	    #source.append(f.readline())
	for i in xrange(3):
	    tmp = self.sock.recv(900)
	    time.sleep(0.3)
	    source.extend(tmp.split('\n'))
	    print "Read", str(len(source)), "numbers"
	b = time.localtime()
	print str(b.tm_sec - a.tm_sec)
        for value in source:
            #value = value[:-1]
            """Deleting \n"""
            try:
                number = unpack('H', value)
                output.append(number[0])
                #print number[0]
            except error:
		#print 'Wrong number', number[0]
                pass
        print "Sending signal with", len(output), "probes."
        self.emit(QtCore.SIGNAL('update_plots(PyQt_PyObject)'), output)
