# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 21:29:56 2021

@author: suare
"""

import matplotlib.pyplot as plt
import cv2
import numpy as np
import math

def promilu(image,n,m):
    lensum=0
    sumpix=0
    for i in range(0,n-1):
        for j in range(0,m-1):
            pix=image[i,j]
            if pix>=1:
                sumpix=pix+sumpix
                lensum=lensum+1
    
    sprom=sumpix/lensum
    return sprom

sigma=0.33
def auto_canny(image, sigma):                                                   # compute the median of the single channel pixel intensities
	v = np.median(image)	                                                        # apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)
	return edged

def changeformat(img_cf):                                                       #pasar de float64 a unit8
    info = np.info(img_cf.dtype)                                                # Get the information of the incoming image type
    data = img_cf.astype(np.float64) / np.max(img_cf)                           # normalize the data to 0 - 1
    data = 255 * data                                                           # Now scale by 255
    imgNuev = data.astype(np.uint8)                                             #máscara Disco Optico
    return imgNuev

def funumbral(image,vmin,vmax,valueminhist):
    h=plt.hist(image.ravel(),256,[valueminhist,256])
    inten=[]
    valor=0
    
    for i in range(0,len(h[0])):
        inten.append(h[0][i])    
    
    for j in range(0,len(inten)):
        valor=valor+inten[j]
        if round(valor)>=round(vmin*sum(inten)) and round(valor)<=round(vmax*sum(inten)):
            umbral=j
            break 
    plt.clf()
    return umbral

#nombre="V0382"
#nombre="g0020"
#ruta="D:\\Disco_Duro_JP\\Archivos\\Universidad\\Pocesamiento digital de imagenes\\Proyecto\\Archivos\\Database\\G\\",nombre,".jpg"
#ruta="E:\\Users\\Escritorio\\Nueva carpeta\\REFUGE2\DATOS_TRAIN\\Refuge2-Validation\\Refuge2-Validation","\\",nombre,".jpg"
#ruta=''.join(ruta)
#image=plt.imread(ruta)
    
def funseg(image):
    img=image
    imagemix=(img[:,:,0]*0.70)+(img[:,:,1]*0.1)+(img[:,:,2]*0.20)                   #mix de canales
    imgsquare=255.0*(imagemix/255.0)**2                                             #ecualizacion cuadrada.... más oscura de poco contraste
    n,m=np.shape(imgsquare)                                                         #dimensión de la imagen
    mediapix=promilu(imgsquare,n,m)                                                 #promedio de la imagen sin pixeles negros
    print("Promedio de la intensidad: ",mediapix)
    nuevaimg=imgsquare.copy()
    filtrado = cv2.blur(nuevaimg,(9,9))                                             #filtro difuminado con kernel 9x9
    umbral1=funumbral(filtrado,0.98,1,0)                                            #imagen, vmin, vmax,valueminhist  
    print("Umbral:",umbral1)       
    ret,thresh1 = cv2.threshold(filtrado,umbral1,255,cv2.THRESH_BINARY_INV)
    dilatada = cv2.dilate(thresh1, None, iterations=3)                              #limpia la imagen
    erosion = cv2.erode(dilatada, None, iterations=20)                              #Expande a su forma
    imagen_ero=erosion.copy()
    imgN=changeformat(imagen_ero)                                                   #PASAR DE FLOAT A UINT8
    disco_opt=auto_canny(imgN,sigma)
    (imagencontrno,cont) = cv2.findContours(disco_opt, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cont2=cv2.drawContours(img.copy(),imagencontrno,-1,(0,255,0), 21)
    plt.imshow(cont2,cmap="gray")
    #-------------------------------------------------------
    
    #---------------Seleccion del contorno--------------------
    cont=imagencontrno
    
    if len(cont)>=1:
        cx=0
        cy=0
        areas=[]
        pcx=[]
        pcy=[]
        peri=[]
        for i in range(0,len(cont)):
            ca = cont[i] #contornosarea
            M = cv2.moments(ca) 
            if M['m00']==0:
                M['m00'] =  100
            else:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
            
            area = cv2.contourArea(ca)
            perimetro=cv2.arcLength(ca,False)
            areas.append(area)
            pcx.append(cx)
            pcy.append(cy)
            peri.append(perimetro)
        
        #condicion1-Compacta
        condi1=[]
        for f in range(0,len(areas)):
            if peri[f]==0:
                peri[f]=1
                com=(4*math.pi*areas[f])/(peri[f]**2)
                condi1.append(com)
            else:
                com=(4*math.pi*areas[f])/(peri[f]**2)
                condi1.append(com)
        pun=0
        condi2=[]
        for ff in range(0,len(condi1)):        
            if condi1[ff]>=pun and pun<=1 and condi1[ff]<=1:
                if len(condi1)>=7:
                    flag=peri.index(max(peri))               
                else:
                    pun=condi1[ff]
                    flag=ff  
    else:
        flag=0
        cont2=cv2.drawContours(img.copy(),cont,-1,(0,255,0), 21)  
        
        
    #------------------------------------------------------
    tam=520                                                                         #pixeles de entrada de la red
    img_i_r=np.zeros((tam,tam,3))                                                   #creación de la máscara de recorte
    #print(flag)
    x,y,w,h = cv2.boundingRect(cont[flag])
    img_rec = cv2.rectangle(img.copy(), (x,y), (x+w,y+h), (0,255,0), 20)
    
    #print(x,y,w,h)
    
    centro_x=x+(w/2)
    centro_y=y+(h/2)
    #print(centro_x)
    #print(centro_y)
    
    x_n=round(centro_x-(tam/2))
    y_n=round(centro_y-(tam/2))
    h_n=round(centro_x+(tam/2))
    w_n=round(centro_y+(tam/2))
    #print(x_n,y_n,h_n,w_n)
    
    img_rec2 = cv2.rectangle(img.copy(), (x_n,y_n), (h_n,w_n), (0,255,0), 20)
    
    
    
    for k in range(3):
      for i in range(tam):
        for j in range(tam):
          img_i_r[i,j,k]=int(img[y_n+j,x_n+i,k])
          
    
    #plt.imshow(img_i_r)
    #plt.imshow((img_i_r*255).astype(np.uint8))
    img_i_r= img_i_r/255
    return img_i_r

