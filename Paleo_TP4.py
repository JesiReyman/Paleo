#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 20:20:43 2020

@author: jesica
"""


from pandas_ods_reader import read_ods
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

archivo='/home/jesica/Descargas/Bintaja.ods'

sheet_name = "Sheet1"
datos = read_ods(archivo, sheet_name)


plt.plot(datos['Time'],datos['Iso_tot'])
plt.xlabel('Time (ky BP)')
plt.ylabel('18O ‰')
plt.show()


plt.plot(datos['Time'],datos['Tsurf'],'orange')
plt.xlabel('Time (ky BP)')
plt.ylabel('°C')
plt.show()

plt.plot(datos['Time'],datos['Ice_eas'],label='Eurasia')
plt.plot(datos['Time'],datos['Ice_nam'],label='North America')
plt.xlabel('Time (ky BP)')
plt.ylabel('Ice volume (m.s.l.e)')
plt.legend()
plt.show()

plt.plot(datos['Time'],datos['RSL'],'grey')
plt.xlabel('Time (ky BP)')
plt.ylabel('Global sea level (m)')
plt.legend()
plt.show()
