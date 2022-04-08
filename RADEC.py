import os,sys
import struct
import numpy as np
import yaml
import bitstring as bs
from bitstring import ConstBitStream
import time
import glob
import math
from statistics import mean
import matplotlib.pyplot as plt

f = open('/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/programas/files_Marcelo/cat_201214_1.txt','r')
#g = open('schvenus4_icrs_201028.txt','r')
g = open('/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/programas/files_Marcelo/schsol0_icrs_201214.txt','r')
#h = open('./datos/ttcp1/j181ttcp1c05.txt','r')
h = open('/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/programas/files_Marcelo/fase02ttcp2c03.txt','r')

#f = open('/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/outputs/Venus/cat_201214_1v.txt', 'r')
#g = open('/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/outputs/Venus/sch_201214_1v.txt', 'r')
h1 = open('/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/outputs/Venus/Poten_total_C1-x_gain.txt', 'r')
h2 = open('/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/outputs/Venus/Poten_total_C2-x_gain.txt', 'r')
h3 = open('/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/outputs/Venus/Poten_total_C3-x_gain.txt', 'r')
h4 = open('/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/outputs/Venus/Poten_total_C4-x_gain.txt', 'r')
h5 = open('/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/outputs/Venus/Poten_total_C5-x_gain.txt', 'r')
h6 = open('/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/outputs/Venus/Poten_total_C6-x_gain.txt', 'r')
h7 = open('/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/outputs/Venus/Poten_total_C7-x_gain.txt', 'r')
h8 = open('/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/outputs/Venus/Poten_total_C8-x_gain.txt', 'r')


x = []
y = []
z = []
cat1 = f.readlines()
sch1 = g.readlines()
dat1 = h.readlines()

data = {}
for d in dat1:
    dl = d.split()
    datid = int(round(float(dl[0])))
    flujo = float(dl[1])
    data[datid] = flujo
#    z.append(data[datid])
dcat = {}
for l in cat1:
    lc = l.split()
    catid = lc[0]
    #print(lc)
    rahms = lc[1].split(':')
    dedms = lc[2].split(':')
#    print(rahms)
    if float(rahms[0]) < 0.0:
        rag = (float(rahms[0]) - float(rahms[1])/60.0 -\
            float(rahms[2])/3600.0)*15.0
    else:    
        rag = (float(rahms[0]) + float(rahms[1])/60.0 +\
            float(rahms[2])/3600.0)*15.0
    if float(dedms[0]) < 0.0:
        decg = float(dedms[0]) - float(dedms[1])/60.0 -\
            float(dedms[2])/3600.0
    else:
        decg = float(dedms[0]) + float(dedms[1])/60.0 +\
            float(dedms[2])/3600.0
    
    
    rag1 = "{0:.2f}".format(rag)
    decg1 ="{0:.4f}".format(decg)
#    print(rag1)
    dcat[catid] = rag1, decg1
    print(dcat[catid])
    
for ll in sch1:
    lls = ll.split()
    #print(lls)
    #print(lls[0],lls[1],lls[2])
    schid = lls[2]
#    print(schid)
    ns = int(lls[1]) #
#    print(ns)
    fyh = lls[0].split('/')
#    print(fyh)
    hora = fyh[3].split(':')
#    print(hora)
    yyyy = int(fyh[0])
    mm = int(fyh[1])
    dd = int(fyh[2])
    hh = int(hora[0])
    ms = int(hora[1])
    ss = int(hora[2])
#    print(yyyy, mm, dd, hh, ms, hh, ms, ss)
    sod = ss + ms*60 + hh*3600 #sec of day
#    print(dcat[schid])
    #print(sod)
    count = 0
    suma = 0.0
    for sec in range(0,ns):
        seg = sod + sec
#        print(sod, seg)
#        print(ll, data[seg])
        if seg not in data.keys() or data[seg]==0.0:
            count += 1
            data[seg] = 0.0 
            #print('not in dic')
        suma = suma + data[seg]
    if count == 0:
        prom = suma / float(ns)
    elif (ns - count) != 0:
        prom = suma / (float(ns) - float(count))
#        print(prom)
    else:
        prom = 0
#    raiz = np.sqrt(prom)
#    print(raiz)
    if prom != 0:
        x.append(dcat[schid][0])
        y.append(dcat[schid][1])
        z.append(prom)
#-----------------------------------------------
#           Plots
#-----------------------------------------------
plt.tricontourf(x, y, z, 20, cmap='rainbow')
#plt.title('Venus banda X - C01')
plt.title('Sol banda X - C01')
plt.colorbar()
plt.ylabel('DEC [deg]')
plt.xlabel('RA [deg]')
#plt.savefig('VXC1.png')
plt.show()

