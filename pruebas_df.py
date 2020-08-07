#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 11:13:48 2020

@author: jesica
"""
import numpy as np
import pandas as pd

ruta='/home/jesica/Documentos/Paleo/tp5_paleo/'

CCSM4_sheet_map = pd.read_excel(ruta+'CCSM4-MATRIZ.xlsx', sheet_name=None)

CCSM4_hojas=list(CCSM4_sheet_map.keys())

primer_hoja=CCSM4_sheet_map[CCSM4_hojas[0]]

matriz=primer_hoja.iloc[:,1::]

#quiero las columnas que solo esten entre -65,-55

lon=primer_hoja.columns.values[1::].astype('float32')
lat=primer_hoja.iloc[:,0]

lon_pampa =( (-66 <= lon) & (-55 >= lon))

recorte_lon=matriz.loc[:, lon_pampa]
region1=recorte_lon.loc[lat<=-60].values

lat_pampa=lat[(lat<=-30)&(lat>=-40)]
peso=np.cos(np.deg2rad(lat_pampa))

