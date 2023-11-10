# ChallngeMM_Temp_Color
# DESCRIPCION y FIABILIDAD
El objetivo de este challenge es asegurar que el usuario se encuentra en una sala concreta mediante el cálculo de la Temperatura de color de la sala reflejada en una imagen.
Presenta una fiabilidad baja, al realizar el experimento con imágenes tomadas desde un móvil el resultado es muy dependiente de las características del móvil y las sombras que pueden quedar en la imagen debido a la posición del usuario en el momento de tomar las fotos

# FUNCIONAMIENTO
Se pide al usuario que haga una foto a una superficie blanca dentro de la sala y la envíe al PC.  
La imagen se carga en plano RGB y se transforma al plano XYZ. Luego se extraen los valores de las matrices de cada componente X, Y y Z para calcular la CCT de la imagen. Este trabajo se ha basado en la investigación desarrollada en: https://ams.com/documents/20143/80162/TCS34xx_AN000517_1-00.pdf

Ficheros:

- Temp_Color.py: La implementación completa del challenge se encuentra en este único fichero python
- cap_temp.jpeg : fichero de prueba. La captura enviada por el server bluetooth debe tener este nombre para que no haya que hacer cambios en el código fuente.
- lock_Temp_Color: es un fichero generado durante la ejecución para impedir que dos challenges multimedia se ejecuten a la vez

El challenge da como resultado una clave de longitud 1 o 2 que estará entre los valores de 0 a 99, correspondientes a la CCT en grados Kelvin cuantizada en cuantos de 100.

# Requisitos
La variable de entorno **SECUREMIRROR_CAPTURES** debe existir y apuntar al path donde el server bluetooth deposita las capturas
El fichero de captura se debe llamar "cap_temp.jpeg".

Hay una variable en el challenge llamada **"DEBUG_MODE"** que la puedes cambiar a True o False. En caso DEBUG_MODE=false, la imagen se borra tras el procesamiento.
Las principales librerías utilizadas son las siguientes:
- Opencv : Usada para la carga de imagen y transformación de plano RGB a XYZ.

Para instalar la libreria openCV simplemente:
pip3 install opencv-python
IMPORTANTE: Tras instalar opencv, la dll python3.dll de instalacion de python cambia, debes darle acceso al programa que haga uso de este challenge ubicandola en un directorio al que pueda acceder

- Tkinter para las GUI utilizadas para interactuar con el usuario. https://www.pythontutorial.net/tkinter/

# Configuración json ejemplo
```json
{
	"FileName": "challenge_loader_python.dll",
 
	"Description": "This is a simple challenge.",
 
	"Props": {
 
		"module_python": "Temp_Color",
  
		"validity_time": 3600,
  
		"refresh_time": 10,
  
   
  },
  
  "Requirements": "camera" 
  
}
```




