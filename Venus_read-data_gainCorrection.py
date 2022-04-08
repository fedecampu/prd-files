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
###
###
inicio = time.time()



#INFILEka="/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/NET4n001tRsMG11rR2c07-20349123932-002.prd" #Banda Ka
#INFILEka="/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/NET4n001tRsMG11rR2c03-20349123932-004.prd" #Banda Ka
#INFILEka="/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/NET4n001tRsMG11rR2c02-20349123932-005.prd" #Banda Ka
#INFILEka="/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/NET4n001tRsMG11rR2c01-20349123932-006.prd" #Banda Ka
INFILEka="/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/NET4n001tRsMG11rR2c04-20349123932-008.prd" #Banda Ka
#INFILEka="/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/NET4n001tRsMG11rR2c05-20349123932-010.prd" #Banda Ka
#INFILEka="/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/NET4n001tRsMG11rR2c06-20349123932-011.prd" #Banda Ka
#INFILEka="/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/NET4n001tRsMG11rR2c08-20349123932-013.prd" #Banda Ka
#print(os.stat(INFILEka).st_size)

#INFILEx="/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/NET4n001tRsMG11rR1c07-20349123932-003.prd"  #Banda X
#INFILEx="/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/NET4n001tRsMG11rR1c03-20349123932-007.prd"  #Banda X
#INFILEx="/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/NET4n001tRsMG11rR1c04-20349123932-009.prd"  #Banda X
#INFILEx="/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/NET4n001tRsMG11rR1c01-20349123932-012.prd"  #Banda X
#INFILEx="/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/NET4n001tRsMG11rR1c02-20349123932-014.prd"  #Banda X
#INFILEx="/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/NET4n001tRsMG11rR1c05-20349123932-015.prd"  #Banda X
#INFILEx="/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/NET4n001tRsMG11rR1c06-20349123932-016.prd"  #Banda X
#INFILEx="/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/NET4n001tRsMG11rR1c08-20349123932-017.prd"  #Banda X
#Lectura de los archivos de la banda X
# Banda X = 8510000000.0 Hz = 8.5 GHz

#sz = os.path.getsize(INFILEx)
sz = os.path.getsize(INFILEka)
rcfile = int(sz/4000176.0)
print("sec obs_C04 files:", rcfile)
#
#file_s1 = "Poten_total_C6-x_gain.txt"
file_s1 = "Poten_total_C4-ka_gain.txt"
files1 = open('/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/outputs/Venus/' + file_s1,'w')
labels_pote = "hora_sec" + "           " + "Potencia_uncorrect"    +   "           " +"P[dBm] "  +   "\n"
files1.write(labels_pote)
#with open(INFILEx, 'rb') as fd:
with open(INFILEka, 'rb') as fd:
    b = ConstBitStream(fd)  
    for rc in range(0,rcfile):
        P1 = []
        P2 = []
        b.read('bytes:42')
        timetag_doi = b.readlist('uintle:16')
        timetag_sec_of_day = b.read('uintle:32')
        timetag_picosec_of_sec = b.read('floatle:64')
        b.read('bytes:78')
        aux = b.read('bits:1')
        iau_flags_G =  aux.int  # G y D
        aux = b.read('bits:1')
        iau_flags_D =  aux.int  # G y D
        aux = b.read('bits:14')
        iau_flags_GD_rest =  ''  # G y D
        IAU_CHANNEL_GAIN =  b.read('floatle:32') #
        IAU_INPUT_DELAY =  b.readlist('floatle:64') #
        empty_field = b.readlist('bytes:24')
        del aux
        end_label = b.readlist('intle:32')
        #b.read('bytes:120')
        t = float(timetag_sec_of_day) + float(timetag_picosec_of_sec)*1e-12
        sum_Pot=0
        sum_Pot1=0
        sum_Pot2=0
        SUM_AUX1=0
        SUM_AUX2=0
        for j in range(0,1000000):
            I1=b.read('uintle:8')
            X0=I1
            I1=2*I1+1
            Q1=b.read('uintle:8')
            X1=Q1
            Q1=2*Q1+1
            I2=b.read('uintle:8')
            X2=I2
            I2=2*I2+1
            Q2=b.read('uintle:8')
            X3=Q2
            Q2=2*Q2+1
            #Marcelo
            SUM_AUX1+=X0**2+X1**2+X2**2+X3**2
            SUM_AUX2+=X0+X1+X2+X3
            #print('I1:',I1,', Q1:',Q1)
            #calculamos P²
            Pot1=(I1**2+Q1**2)
            #print('Pot1:',math.sqrt(Pot1))
            Pot2=(I2**2+Q2**2)
            #calc
            sum_Pot += Pot1
            sum_Pot += Pot2
        P_final=sum_Pot/2000000
        P_marcelo=4*((SUM_AUX1+SUM_AUX2)/2000000+0.5)
        P_final_dbm=20*math.log10(np.sqrt(P_final))-IAU_CHANNEL_GAIN
        P_marcelo_dbm=20*math.log10(np.sqrt(P_marcelo))-IAU_CHANNEL_GAIN
#        print(t,', P_final:',P_final,', P_final_dbm:',P_final_dbm)
#        print(t,', P_marcelo:',np.sqrt(P_marcelo),', P_marcelo_dbm:',P_marcelo_dbm)
        print(t, P_final, P_final_dbm,file = files1)
files1.close()
fin = time.time()
print("tiempo de corrida:", fin-inicio)
