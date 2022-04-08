# prd-files
How to read binary files from DSA3-Malargue 

Los scripts son las herramientas para poder leer los archivo binarios-prd de la antena DS3.

Se pueden leer los headers, la data, y hacer las correcciones por Ganancia para obtener la P[dBm] que necesitamos para estudiar a la señal y a la polarización de la señal.

Liberías necesarias para que los programas puedan ejecutarse:

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






