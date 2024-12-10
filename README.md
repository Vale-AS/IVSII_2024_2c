# Proyecto final: Ray Tracing in One Weekend

Este repositorio contiene el proyecto final de la materia Introducción a la Visualización y Simulación Interactivas e Inmersivas, dictada en el 2c2024 en FCEN-UBA.
El proyecto consiste en una implementación de [Ray Tracing in One Weekend](https://raytracing.github.io/books/RayTracingInOneWeekend.html) en Python.

### Información de las implementaciones

En el proyecto se encuentran dos implementaciones de la clase camera (`camara_class.py` y `camara_class_optimized.py`) y dos versiones de la función main (`main.py` y `main_optimized.py`). Las versiones optimizadas se valen del multiprocesamiento para mejorar el runtime considerablemente.

### Ejecución del programa
La ejecución de las dos implementaciones es ligeramente distinta: 
- La versión sin optimizar se ejecuta simplemente con el comando:
```bash
python3 main.py
```
- La versión optimizada se ejecuta con el siguiente comando:
```bash
python3 main_optimized.py [archivo de salida] [cantidad de cores]
```
- 
   - El argumento `archivo de salida` indica el archivo en el que se escribirá la imagen. De no ser especificado, se le da un nombre genérico.
   - El argumento `cantidad de cores` indica con cuántos núcleos se hará el multiprocesamiento. De no ser especificado, se asume 8 núcleos.