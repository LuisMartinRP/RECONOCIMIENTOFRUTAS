import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier

class Clasificador:
	def __init__(self, dat=None):
		self.dat=dat
	def clasifica(self):	
		dgeneral = pd.read_csv("C:/Users/Luis Martin R.P/Documents/9 Semestre/reconocimiento de objetos/train/train/datos.csv")

		datos = dgeneral[['x', 'y', 'area', 'perimetro', 'largox', 'largoy','m0', 'm1', 'm2', 'm3', 'm4', 'm5', 'm6', 'r', 'g', 'b', 'pr', 
		'pg', 'pb']]
		clase = dgeneral["clase"]
		#print(datos)
		#print(clase)
		clasificador = KNeighborsClassifier(n_neighbors=30)
		clasificador.fit(datos, clase)

		'''dprueba = pd.read_csv("datostest2.csv")
		datosprueba=dprueba[["x", "y","area","perimetro","r","g","b","pr","pg","pb"]]'''
		
		prediccion=None
			
		prediccion=(clasificador.predict([self.dat]))
		return prediccion[0]
		#print(prediccion)