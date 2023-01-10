import cv2
import numpy as np
import imutils
class Rasgos:
	def __init__(self, img=None):
		self.imagen=img

	def extraccion(self):
		caracind=[]
		img=cv2.imread(self.imagen)
		#redimenconar 
		img=cv2.resize(img,(100, 100))
		#agregar borde
		img = cv2.copyMakeBorder(img, 3, 3, 3, 3, cv2.BORDER_CONSTANT, value=[255,255,255])
		#calculo de ancho y alto
		ancho = img.shape[1]
		alto = img.shape[0]
		#separacion de imagen en sus planos
		b,g,r=cv2.split(img)
		#cambio de imagen a grises	
		gris=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		#eliminacion de ruido
		gaussiana = cv2.GaussianBlur(gris, (5,5), 0)
		#umbralado a imagen
		ret, th1 = cv2.threshold(gaussiana,10,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
		#operacion de apertura a imagen para eliminar puntos no deseados
		th=cv2.morphologyEx(th1, cv2.MORPH_OPEN, (5,5));
		#identificacion de contornos
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
		'''print(M)
		print("")
		print(moments)'''
		if M["m00"] != 0:
			#calculo del cenroide del objeto
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
			return caracind
		else:
			caracind=[]
			#print(caracind)