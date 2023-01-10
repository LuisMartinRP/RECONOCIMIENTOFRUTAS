from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import imutils
import cv2
from rasgos import Rasgos
from clasificador import Clasificador
from receta import Receta
imagen=None
filep=None
si=False

def openfile():
	global si
	si=True
	filepath=filedialog.askopenfilename(initialdir="/", title="Selecciona la imagen.",filetypes=(("image files","*.jpg"),("all files","*.*")))
	
	global imagen
	global filep
	filep=filepath
	imagen=cv2.imread(filepath)
	image=imutils.resize(imagen,height=360)

	imagetoshow=imutils.resize(image,height=120)
	imagetoshow=cv2.cvtColor(imagetoshow,cv2.COLOR_BGR2RGB)
	im=Image.fromarray(imagetoshow)
	imgmostrar=ImageTk.PhotoImage(image=im)
	labelimagen.configure(image=imgmostrar)
	labelimagen.Image=imgmostrar

def clasif():
	#print(si)
	if si:
		rasgos= Rasgos(filep)
		caracind=rasgos.extraccion()
		if len(caracind)!=0:
			clasificador=Clasificador(caracind)
			'''clases=["manzana roja","manzana verde","albaricoque","aguacate","platano","arandano","tuna","melon","cereza","mandarina","maiz","pepino",
					"uva azul","kiwi","limon","lima","mango","cebolla","naranja","papaya","maracuya","durazno","pera","pimiento verde","pimiento rojo","piña",
					"ciruela","granada","papa","frambuesa","fresa","tomate","sandia"]'''

			predic=clasificador.clasifica()
			textoclase.config(text=predic)
			#vent=Receta(predic)
			#vent.mostrarreceta()
		else:
			textoclase.config(text="No puedo identificar la clase de la imagen.")
	else:
		textoclase.config(text="No has seleccionado ninguna imagen.")

raiz=Tk()

raiz.title("Reconociendo frutas y verduras")
raiz.geometry("700x400")

mframe=Frame()
mframe.pack()
mframe.config(width="700", height="400",bg="black")

labelimagen=Label(mframe)
labelimagen.config(bg="black")
labelimagen.place(x=300,y=50)

label=Button(mframe,text="Selecciona la imagen.",command=openfile,bg="white",font=("verdana",12))
label.place(x=50,y=50)

botonclasif=Button(mframe, text="Clacificar",command=clasif,bg="white",font=("verdana",12))
botonclasif.place(x=50,y=200)

labelclase=Label(mframe,text="Clase encontrada:",fg="white",bg="black",font=("verdana",12))
labelclase.place(x=50,y=250)

textoclase=Label(mframe)
textoclase.config(fg="white",bg="black",font=("verdana",12))
textoclase.place(x=200,y=250)

'''labelp=Label(mframe,text="Puro trabajo honesto, ya pasenos profa :(",fg="white",bg="black",font=("verdana",18))
labelp.place(x=50,y=300)'''

labelimagenpat=Label(mframe,bg="yellow")
labelimagenpat.place(x=480,y=50)
patricio=cv2.imread("patricio.jpg")
imagetos=imutils.resize(patricio,height=120)
imagetos=cv2.cvtColor(imagetos,cv2.COLOR_BGR2RGB)
impat=Image.fromarray(imagetos)
imgmost=ImageTk.PhotoImage(image=impat)
labelimagenpat.configure(image=imgmost)
labelimagenpat.Image=imgmost

labelr=Label(mframe,text="Si no brandon se sacrifica",fg="gray",bg="black",font=("verdana",12))
labelr.place(x=200,y=350)

raiz.mainloop()