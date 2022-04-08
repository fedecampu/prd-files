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
#INFILEx="/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/NET4n001tRsMG11rR1c07-20349123932-003.prd"  #Banda X
#INFILEx="/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/NET4n001tRsMG11rR1c03-20349123932-007.prd"  #Banda X
#INFILEx="/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/NET4n001tRsMG11rR1c04-20349123932-009.prd"  #Banda X
#INFILEx="/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/NET4n001tRsMG11rR1c01-20349123932-012.prd"  #Banda X
INFILEx="/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/NET4n001tRsMG11rR1c02-20349123932-014.prd"  #Banda X
#INFILEx="/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/NET4n001tRsMG11rR1c05-20349123932-015.prd"  #Banda X
#INFILEx="/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/NET4n001tRsMG11rR1c06-20349123932-016.prd"  #Banda X
#INFILEx="/home/federico/work/DS3/observacion/Marcelo/j349/TTCCP/NET4n001tRsMG11rR1c08-20349123932-017.prd"  #Banda X
#Lectura de los archivos de la banda X
# Banda X = 8510000000.0 Hz = 8.5 GHz


sz = os.path.getsize(INFILEx)
#print(sz)
rcfile = int(sz/4000176.0)
print("sec obs_C02 files:", rcfile)
#
#fileout = "header_C2-x.txt"
labels = "sec" + "record_label" + "  " + "record_length" + "  " + "record_version"+ "  " + \
            "station" + "  " + "spacecraft_id" + "  " + "sample_size"+ "  " + \
          "sample_rate" + "  " + "validity_flag" + "  " + \
           "agency_flag" + "  " + "rf_to_if" + "             " + "if_to_ch" + "          " + \
          "timetag_year" + "  " + "timetag_doi" + "  " + "timetag_sec_of_day"+"  " + \
          "timetag_picosec_of_sec" + "  " + "ch_accum_phase" + "  " + "ch_phase_pol_coef0" + "  " + \
           "ch_phase_pol_coef1" + "  " + "ch_phase_pol_coef2" + "  " + "ch_phase_pol_coef3" + "  " + \
          "empty_field" + "  " + "iau_flags_FVer" + "  " + "iau_flags_FSrc" +  "  " + \
           "iau_flags_subchSrc" +  "  " + "iau_flags_G" +  "  " + "iau_flags_D" +  "  " + \
          "iau_flags_GD_rest" + "  " + "IAU_CHANNEL_GAIN" + "   " + "IAU_INPUT_DELAY" + "  " + \
           "empty_field" +  "    " + "end_label" + "    " +   "hora_sec" + "\n"
#f = open(fileout,'w')
#f.write(labels) 
##
with open(INFILEx, 'rb') as fd:
    b = ConstBitStream(fd)  
    for rc in range(0,rcfile):
        record_label = bytes.join(b'', b.readlist('bytes:4')).decode('ascii')
        record_length = b.readlist('uintle:32')
        record_version = b.readlist('uintle:16')
        station = b.readlist('uintle:16')
        spacecraft_id = b.readlist('uintle:16')
        sample_size = b.readlist('uintle:16')
        sample_rate = b.readlist('uintle:32')
        validity_flag = b.readlist('uintle:16')
        agency_flag = b.readlist('uintle:16')
        rf_to_if = b.readlist('floatle:64')
        if_to_ch = b.readlist('floatle:64')
        timetag_year = b.readlist('uintle:16')
        timetag_doi = b.readlist('uintle:16')
        timetag_sec_of_day = b.read('uintle:32')
        timetag_picosec_of_sec = b.read('floatle:64')
        ch_accum_phase = b.readlist('floatle:64')
        ch_phase_pol_coef0 = b.readlist('floatle:64')
        ch_phase_pol_coef1 = b.readlist('floatle:64')
        ch_phase_pol_coef2 = b.readlist('floatle:64')
        ch_phase_pol_coef3 = b.readlist('floatle:64')
        empty_field = b.readlist('bytes:36')
        aux = b.read('bits:8')
        iau_flags_FVer = aux.int
        aux = b.read('bits:4')
        iau_flags_FSrc =  aux.int # (11...8)# (15...12)
        aux = b.read('bits:4') 
        iau_flags_subchSrc = aux.int  # G y D
        aux = b.read('bits:1')
        iau_flags_G =  aux.int  # G y D
        aux = b.read('bits:1')
        iau_flags_D =  aux.int  # G y D
        aux = b.read('bits:14')
        iau_flags_GD_rest =  ''  # G y D
        IAU_CHANNEL_GAIN =  b.readlist('floatle:32') #
        IAU_INPUT_DELAY =  b.readlist('floatle:64') #
        empty_field = b.readlist('bytes:24')
        del aux
        end_label = b.readlist('intle:32')
        hora_sec = float(timetag_sec_of_day) + float(timetag_picosec_of_sec)*1e-12
    #   print(hora_sec)
        salida = str(rc+1) + "    " + str(record_label) + "         " + str(record_length) + "           " + str(record_version) + "          " + \
        str(station) + "          " + str(spacecraft_id) + "          " + str(sample_size)+ "     " + \
        str(sample_rate) + "     " + str(validity_flag) + "               " + \
        str(agency_flag) + "   " + str(rf_to_if) + "      " + str(if_to_ch) + "        " + \
        str(timetag_year) + "           " + str(timetag_doi) + "        " + str(timetag_sec_of_day) +"             " + \
        str(timetag_picosec_of_sec) + "       " + str(ch_accum_phase) + "       " + str(ch_phase_pol_coef0) + "          " + \
        str(ch_phase_pol_coef1) + "              " + str(ch_phase_pol_coef2) + "                     " + str(ch_phase_pol_coef3) + "          " + \
        str("empty_field") + "       " + str(iau_flags_FVer) + "                " + str(iau_flags_FSrc) +  "                  " + \
        str(iau_flags_subchSrc) +  "                " + str(iau_flags_G) +  "            " + str(iau_flags_D) +  "         " + \
        str("empty_field") + "   "+ str(IAU_CHANNEL_GAIN) + "   " + str(IAU_INPUT_DELAY) + "  " + \
        "empty_field" +  "  " + str(end_label) + "  " + str(hora_sec) +  "\n"
#        f.write(salida) 
        print(salida)
#        print(yaml.dump(header, default_flow_style=False, sort_keys=False))
#                #print('iau_flags_G', iau_flags_G)
        b.readlist('bytes:4000000') #skip data
##
fin = time.time()
print("tiempo de corrida:", fin-inicio)
