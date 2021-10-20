# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 11:52:53 2020

@author: JP
"""

import matplotlib.pyplot as plt
import pygame
import seg
import time

start = time.time()
for i in range(235,361): #401
    if i<10:
        nombre="n000",str(i)    
        nombre=''.join(nombre)
    elif i>=10 and i<=99:
        nombre="n00",str(i)
        nombre=''.join(nombre) 
    elif i>=100 and i<=401:
        nombre="n0",str(i)
        nombre=''.join(nombre)
    ruta="D:\\Disco_Duro_JP\\Archivos\\Universidad\\Pocesamiento digital de imagenes\\Proyecto\\Archivos\\Database\\N_G\\",nombre,".jpg"
    #ruta="E:\\Users\\Escritorio\\Nueva carpeta\\REFUGE2\DATOS_TRAIN\\Refuge2-Validation\\Refuge2-Validation","\\",nombre,".jpg"
    ruta=''.join(ruta)
    image=plt.imread(ruta)
    print(nombre)
    #---
    do=seg.funseg(image)
    #---
    
    plt.imshow(do,cmap="gray")
    plt.axis('off')
    plt.tight_layout() 
    nom=str(nombre),".png"
    nom=''.join(nom)
    my_dpi=5200/37
    #my_dpi=497.5 
    rutasave="D:\\Disco_Duro_JP\\Archivos\\Universidad\\Pocesamiento digital de imagenes\\Proyecto\\Archivos\\Seg\\N_G\\",nom
    #rutasave="E:\\Users\\Escritorio\\Nueva carpeta\\REFUGE2\PRUEBAS\\26. FINALPRIMERA\\NSeg\\",nom
    rutasave=''.join(rutasave)
    #plt.savefig(rutasave,bbox_inches="tight",figsize=(5.416, 5.416), pad_inches = 0,dpi=my_dpi)
    plt.savefig(rutasave,bbox_inches="tight", pad_inches = 0,dpi=my_dpi)
    plt.clf()

end = time.time()
print(end - start)

pygame.mixer.init()
pygame.mixer.music.load("so.mp3")
pygame.mixer.music.play()