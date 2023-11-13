import cv2
# para instalar la libreria openCV simplemente:
# pip3 install opencv-python
# o bien py -m pip install opencv-python
# para aprender opencv https://www.geeksforgeeks.org/opencv-python-tutorial
import numpy as np
import os
from pathlib import Path
import time
#para instalar el modulo easygui simplemente:
#pip3 install easygui
# o bien py -m pip install easygui
#import easygui
from tkinter import messagebox
import lock

# variables globales
# ------------------
props_dict={}
DEBUG_MODE=True

def init(props):
    global props_dict
    print("Python: Enter in init")
    
    #props es un diccionario
    props_dict= props
    
    # retornamos un cero como si fuese ok, porque
    # no vamos a ejecutar ahora el challenge
    return 0 # si init va mal retorna -1 else retorna 0
    

def executeChallenge():
    print("Starting execute")
    #for key in os.environ: print(key,':',os.environ[key]) # es para ver variables entorno
    folder=os.environ['SECUREMIRROR_CAPTURES']
    print ("storage folder is :",folder)
    
    # mecanismo de lock BEGIN
    # -----------------------
    lock.lockIN("Temp_Color")

    # pregunta si el usuario tiene movil con capacidad foto
    # -----------------------------------------------------
    #textos en español, aunque podrian ser parametros adicionales del challenge
    #conexion=easygui.ynbox('¿Tienes un movil con bluetooth activo y cámara emparejado con tu PC?',"challenge MM: Temp_Color", choices=("Yes","Not"))
    conexion=messagebox.askyesno('challenge MM: Temp_Color','¿Tienes un móvil con bluetooth activo emparejado a tu PC y con cámara?')
    print(conexion)
    #Si el usuario responde que no ha emparejado móvil y PC, devolvemos clave y longitud 0
    if (conexion==False):
        lock.lockOUT("Temp_Color")
        print ("return key zero and long zero")
        key=0
        key_size=0
        result =(key,key_size)
        print ("result:",result)
        return result # clave cero, longitud cero
    
    #popup msgbox pidiendo interaccion
    #---------------------------------
    #sent=easygui.ynbox(props_dict["interactionText"], "challenge MM: RGB", choices=("Yes","Not"))
    sent=conexion=messagebox.askyesno('challenge MM: Temp_Color',"Por favor, haga una foto de una superficie blanca solo con la luz ambiental de la sala, sin incidencia de luz natural. Envíe la imagen desde el móvil a tu PC?")
    print(sent)

    #Si el usuario responde que no ha enviado la imagen, devolvemos clave y longitud 0
    if (sent== False):
        lock.lockOUT("Temp_Color")
        print ("return key zero and long zero")
        key=0
        key_size=0
        result =(key,key_size)
        print ("result:",result)
        return result # clave cero, longitud cero
    
    
    filename="cap_temp.jpeg"
    
        
    if os.path.exists(folder+"/"+filename):    
        img = cv2.imread(folder+"/"+filename,cv2.IMREAD_COLOR)
    else:
        print ("ERROR: el fichero de captura",filename," no existe")
        key=0
        key_size=0
        result =(key,key_size)
        print ("result:",result)
        lock.lockOUT("Temp_Color")
        return result # clave cero, longitud cero
    
    # una vez consumida, podemos borrar la captura (fichero "capture.jpg")
    if (DEBUG_MODE==False):
        if os.path.exists(folder+"/"+filename):    
            os.remove(folder+"/"+filename)
        
    if (DEBUG_MODE==True): #mostramos imagenes en modo debug
        cv2.imshow("challenge MM Temp_Color", img)
    
    imgXYZ = cv2.cvtColor(img, cv2.COLOR_BGR2XYZ) # La imagen se pasa al plano XYZ
    cv2.imshow("imgXYZ", imgXYZ)

    #b,g,r=cv2.split(img)
    X,Y,Z=cv2.split(imgXYZ)
    #print ("b,g,r:", b,g,r)
    #print ("Y:", Y)
    
    suma=X+Y+Z
        
    x = X/(suma) 
    y = Y/(suma)

    #print ("x:", x)
    #print ("y:", y)

    n = (x - 0.3320) / (0.1858 - y)
    
    CCT = 449*(n**3) + 3525*(n**2) + 6823.3*n + 5520.33
    
    CCTRes=[]
    for i in range(len(CCT)):
        CCTRes.append(np.mean(CCT[i])) 

    CCTR=int(np.mean(CCTRes))

    #print (" n:",  n)

    print (" CCTR:",  CCTR, "º Kelvin")


    #mecanismo de lock END
    #-----------------------
    lock.lockOUT("Temp_Color")
    
    
    #cierre 
    #cv2.waitKey(0)        
    cv2.destroyAllWindows()

    #construccion de la respuesta
    cad="%d"%(CCTR/100)
    key = bytes(cad,'utf-8')
    key_size = len(key)
    result =(key, key_size)
    print ("result:",result)
    return result


if __name__ == "__main__":
    midict={""}
    init(midict)
    executeChallenge()

