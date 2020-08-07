#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 08:05:53 2020

@author: jesica
"""


import pandas as pd
import numpy as np


import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


ruta='/home/jesica/Documentos/Paleo/tp5_paleo/'

#cargo los archivos
# for pandas version >= 0.21.0
CCSM4_sheet_map = pd.read_excel(ruta+'CCSM4-MATRIZ.xlsx', sheet_name=None)
CNRM_sheet_map=pd.read_excel(ruta+'CNRM-CM5-MATRIZ.xlsx', sheet_name=None)
IPSL_sheet_map=pd.read_excel(ruta+'IPSL-CM5A-LR-MATRIZ.xlsx', sheet_name=None)
MIROC_sheet_map=pd.read_excel(ruta+'MIROC-ESM-MATRIZ.xlsx', sheet_name=None)
MRI_sheet_map=pd.read_excel(ruta+'MRI-CGCM3-MATRIZ.xlsx', sheet_name=None)

#quiero en listas los nombres de las hojas de cada archivo
CCSM4_hojas=list(CCSM4_sheet_map.keys())
CNRM_hojas=list(CNRM_sheet_map.keys())
IPSL_hojas=list(IPSL_sheet_map.keys())
MIROC_hojas=list(MIROC_sheet_map.keys())
MRI_hojas=list(MRI_sheet_map.keys())

#voy a definir una funcion que haga las cuentas, ingresando el set de datos
#del modelo y ademas la lista de nombres de las hojas que contiene el archivo
def cuentas(modelo,lista_hojas):
 #lee la primer hoja
 primer_hoja=modelo[lista_hojas[0]]
 
#extraigo las latitudes y longitudes (estas ultimas estan como el nombre de cada columna)
 lats=primer_hoja.iloc[:,0]
 
 #para las longitudes me quedo a partir de la columna 1, la primera esta vacia
 lons=primer_hoja.columns.values[1::].astype('float32')

 #recorte en la region Pampa
 #primero pongo las condiciones sobre las latitudes y longitudes,me devuelve arreglos con True o False
 cond_lat=((lats<=-30)&(lats>=-40)) #esto cambio segun las latitudes que quiero
 lats_region=lats[cond_lat]
 
 cond_lons=((lons<=-56)&(lons>=-66))  #solo se habilita para una region en particular

 #calculo los pesos por latitud
 pesos=np.cos(np.deg2rad(lats_region))

#defino un arreglo donde voy a guardar cada promedio areal que haga
 medias_areales=np.zeros((35,1),dtype='float32')

#para cada hoja del excel,quiero calcular las medias areales
 for i in range(0,35):
  #lee la hoja
  hoja=modelo[lista_hojas[i]]
  #extraigo los valores de la matriz a partir de la segunda columna (indice=1)
  matriz=hoja.iloc[:,1::]
  
  #pongo las condiciones de longitud y latitud a la matriz
  matriz=matriz.loc[:, cond_lons] #si no puse condicion a las longitudes,la comento
  matriz=matriz.loc[cond_lat].values
 
  #calculo el promedio zonal de la matriz
  media_zonal=np.mean(matriz,axis=1)
  #ahora calculo el promedio de las medias zonales pero poniendoles el peso por latitud
  medias_areales[i]=np.average(media_zonal,weights=pesos)

 #separa en periodos 
 hom=medias_areales[0:5]
 ppi=medias_areales[5:10]
 pre=medias_areales[10:15]
 r26=medias_areales[15:20]
 r45=medias_areales[20:25]
 r85=medias_areales[25:30]
 umg=medias_areales[30:35]

 #junto por columnas el resultado de cada periodo,las filas representaran:anual,def,mam,jja,son
 periodos=np.column_stack((hom,ppi,pre,r26,r45,r85,umg))

 #calcula diferencias/relaciones entre periodos
 umg_hom=umg-hom
 umg_ppi=umg-ppi
 umg_pre=umg-pre
 hom_ppi=hom-ppi
 hom_pre=hom-pre
 ppi_pre=ppi-pre
 r26_pre=r26-pre
 r45_pre=r45-pre
 r85_pre=r85-pre
 umgr26=umg/r26
 umgr45=umg/r45
 umgr85=umg/r85
 
 #ahora junto por columnas las diferencias y las relaciones entre periodos
 diferencias=np.column_stack((umg_hom,umg_ppi,umg_pre,hom_ppi,hom_pre,ppi_pre,r26_pre,r45_pre,r85_pre,umgr26,umgr45,umgr85))

 return periodos,diferencias

#llamo a la funcion cuentas para cada uno de los modelos

periodos_CCSM4,diferencias_CCSM4=cuentas(CCSM4_sheet_map, CCSM4_hojas)
periodos_CNRM,diferencias_CNRM=cuentas(CNRM_sheet_map, CNRM_hojas)
periodos_IPSL,diferencias_IPSL=cuentas(IPSL_sheet_map, IPSL_hojas)
periodos_MIROC,diferencias_MIROC=cuentas(MIROC_sheet_map, MIROC_hojas)
periodos_MRI,diferencias_MRI=cuentas(MRI_sheet_map, MRI_hojas)

####################### GRAFICOS ######################################

titulos_periodos=['HOM','PPI','PRE','RCP26','RCP45','RCP85','UMG']
titulos_diferencias=['UMG-HOM','UMG-PPI','UMG-PRE','HOM-PPI','HOM-PRE','PPI-PRE','RCP26-PRE','RCP45-PRE','RCP85-PRE','UMG/RCP26','UMG/RCP45','UMG/RCP85']

for i in range(0,7):
 fig = plt.figure(figsize=(15,13))   
 plotdata = pd.DataFrame({
    "CCSM4":periodos_CCSM4[:,i],
    "CNRM":periodos_CNRM[:,i],
    "IPSL":periodos_IPSL[:,i],
    "MIROC":periodos_MIROC[:,i],
    "MRI":periodos_MRI[:,i],
    }, 
    index=["Anual", "DEF", "MAM", "JJA", "SON"]
 )
 plotdata.plot(kind="bar",alpha=0.8)
 plt.xticks(rotation=0,horizontalalignment="center")
 plt.ylim(0,30)
 plt.title("Pampa "+titulos_periodos[i])
 plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
 plt.ylabel("T (°C)")
 plt.savefig(ruta+'figuras/periodo_pampa'+str(i)+'.png',bbox_inches='tight')


for i in range(0,12):
 fig = plt.figure(figsize=(15,13))   
 plotdata = pd.DataFrame({
    "CCSM4":diferencias_CCSM4[:,i],
    "CNRM":diferencias_CNRM[:,i],
    "IPSL":diferencias_IPSL[:,i],
    "MIROC":diferencias_MIROC[:,i],
    "MRI":diferencias_MRI[:,i],
    }, 
    index=["Anual", "DEF", "MAM", "JJA", "SON"]
 )
 plotdata.plot(kind="bar",alpha=0.8)
 plt.xticks(rotation=0,horizontalalignment="center")
 
 plt.title("Pampa "+titulos_diferencias[i])
 plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
 plt.ylabel("T (°C)")
 plt.savefig(ruta+'figuras/diferencia_pampa'+str(i)+'.png',bbox_inches='tight')

 
