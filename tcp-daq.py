#!/usr/bin/env python2.7
# -*- coding: utf8 -*-

import socket
import numpy as np
import argparse
import time
import datetime

class socket_instrument(object):
  def __init__(self,IPaddress,PortNumber=4000):
    self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    self.s.connect((IPaddress,PortNumber))
    self.s.setblocking(False)

  def write(self,cmd):
    self.s.send('{0}\n'.format(cmd))

  def ask(self,cmd,buffer=1024,timeout=5):
    self.s.send(cmd + '\n')
    response=''
    while True:
      char=''
      try:
        char=self.s.recv(1)
      except:
        time.sleep(0.1)
        if response.rstrip() !='':
          break
      if char:
        response+=char
    return response.rstrip()

  def read(self):
    response=''
    while True:
      char=''
      try:
        char=self.s.recv(1)
      except:
        time.sleep(0.1)
        if response.rstrip() !='':
          break
      if char:
        response+=char
    return response.rstrip()

  def close(self):
    self.s.close()

parser=argparse.ArgumentParser()
parser.add_argument('nwav', help='capture number',type=int)
args=parser.parse_args()
nwav=args.nwav

# ip address need to be configure on the scope side
scope=socket_instrument('192.168.10.14')

wavenum=0

scope.write(':head off')
scope.write(':verb off')
scope.write(':dat:sou ch1')
scope.write(':dat:enc fas')
scope.write(':wfmi:byt_n 1')
scope.write(':dis:wave off')
tdel=float(scope.ask(':hor:del:tim?'))
tpos=float(scope.ask(':hor:pos?'))
rlen=int(scope.ask(':hor:reco?'))
scope.write(':dat:star 1;stop {0}'.format(rlen))
Tsam=float(scope.ask(':wfmo:xin?'))
yfac=float(scope.ask(':wfmo:ymul?'))
yoff=float(scope.ask(':wfmo:yof?'))
scope.write(':acq:state seq')

t0=time.time()


while wavenum < nwav:
  #scope.write(':acq:state run')
  wait=int(scope.ask(':*opc?'))
  ttrg=time.strftime('%H:%M:%S',time.localtime(time.time()))
  scope.write(':curv?')   
  data=np.array(scope.read()[5:-1],np.int8)
  y=yfac*(data-yoff)
  wavenum+=1
  fdat.write('FC: {0}\n'.format(ttrg))
  np.savetxt(fdat,y,fmt='%1.4f',newline=' ')
  fdat.write('\n')

t1=time.time()
print u'Data acqusition completed in: {0} hours.'.format(str(datetime.timedelta(seconds=(t1-t0)))[0:7])
print nwav/(t1-t0)
scope.close()
