import cv2
import os
import numpy as np
import csv
import pandas as pd
import imutils

inputpath="C:/Users/Luis Martin R.P/Documents/9 Semestre/reconocimiento de objetos/train/train"
filess=os.listdir(inputpath)
clase=0
allimages=[]
for carpeta in filess:
	print(carpeta)
	files=os.listdir(inputpath+"/"+carpeta)
	for image in files:
		caracind=[]
		if image.split(".")[-1]not in ["jpg","png"]:
			continue
		imagepath=inputpath+"/"+carpeta+"/"+image

		if image is None:
			continue
		img=cv2.imread(imagepath)

		#print(imagepath)
		#img = cv2.copyMakeBorder(img, 3, 3, 3, 3, cv2.BORDER_CONSTANT, value=[255,255,255])
		
		ancho = img.shape[1]
		alto = img.shape[0]

		b,g,r=cv2.split(img)
		
		gris=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		gaussiana = cv2.GaussianBlur(gris, (5,5), 0)
		
		'''brt = 20  
		gaussiana[gaussiana < 120-brt]+=brt'''
		'''brt = 100
		for pixel in gaussiana:
			if pixel.all()<100: 
				pixel += brt'''
		'''cv2.imshow('gris', gris)
		cv2.waitKey(0)   
		cv2.destroyAllWindows()'''
		#ret,th=cv2.threshold(gris,100,255,cv2.THRESH_BINARY_INV)
		ret, th1 = cv2.threshold(gaussiana,10,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
		
		th=cv2.morphologyEx(th1, cv2.MORPH_OPEN, (5,5));
		#th=cv2.morphologyEx(th1, cv2.MORPH_CLOSE, (5,5));
		#th=cv2.morphologyEx(th1, cv2.MORPH_OPEN, (5,5));
		#ret,th=cv2.threshold(gris,100,255,cv2.THRESH_BINARY_INV)
		'''cv2.imshow('umbral', th)
		cv2.waitKey(0)   
		cv2.destroyAllWindows()'''
		contornos,hierachy=cv2.findContours(th,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		
		#Contorno de mayor area
		#contornos=imutils.grab_contours(contornos)
		#contour=max(contornos,key=cv2.contourArea)
		#print(contour)
		cnt=contornos[0]
		#cont=cv2.drawContours(img, contornos, 0, (0,255,0), 1)
		'''cv2.imshow('contornos', cont)
		cv2.waitKey(0)   
		cv2.destroyAllWindows()'''
		#obtencion de los momentos de la imagen
		M=cv2.moments(cnt)
		#calculo de momentos de hu
		moments=cv2.HuMoments(M).flatten()
		if M["m00"] != 0:
			Cx=int(M["m10"]/M["m00"])
			Cy=int(M["m01"]/M["m00"])
			#calculo de largo en x
			largex=int(M["m20"]-(Cx*M["m10"]))
			#calculo de largo en y
			largey=int(M["m20"]-(Cy*M["m10"]))
			#calculo de area del objeto
			area=cv2.contourArea(cnt)
			#calculo de perimetro del objeto
			perimetro=cv2.arcLength(cnt,True)
			#print(perimetro)
			#cv2.circle(img,(Cx,Cy),5,(0,255,0),-1)
			#obtencion de suma de valor de pixeles para r,g,b individiualmente
			sumar=np.sum(r)
			sumag=np.sum(g)
			sumab=np.sum(b)
			#guardar las caracteristicas enontradas
			caracind.append(Cx)
			caracind.append(Cy)
			caracind.append(area)
			caracind.append(perimetro)
			caracind.append(largex)
			caracind.append(largey)
			#momentos de hu
			caracind.append(moments[0])
			caracind.append(moments[1])
			caracind.append(moments[2])
			caracind.append(moments[3])
			caracind.append(moments[4])
			caracind.append(moments[5])
			caracind.append(moments[6])
			caracind.append(sumar)
			caracind.append(sumag)
			caracind.append(sumab)
			#agregamos tambien el promedio de valor por pixel para r,g,b
			caracind.append(sumar//(ancho*alto))
			caracind.append(sumag//(ancho*alto))
			caracind.append(sumab//(ancho*alto))
			#for i in M:
				#caracind.append(i)
			caracind.append(carpeta)
			#print(len(M))
			allimages.append(caracind)
#print(len(caracind))
city = pd.DataFrame(allimages, columns=['x', 'y', 'area', 'perimetro', 'largox', 'largoy','m0', 'm1', 'm2', 'm3', 'm4', 'm5', 'm6', 'r', 'g', 'b', 'pr', 'pg', 'pb'
,'clase'])
city.to_csv(inputpath+"/datos.csv")
clase=clase+1