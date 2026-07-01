# Gestor de Tareas de Productividad (Arboles AVL y Max-Heap)

Este proyecto es una aplicacion de gestion de tareas con Interfaz Grafica (GUI) desarrollada en Python. Integra dos estructuras de datos avanzadas para garantizar un rendimiento optimo:
- Max-Heap: Para gestionar la cola de prioridad de las tareas.
- Arbol AVL: Para indexar y buscar tareas rapidamente mediante su identificador unico.

---

## Requisitos Previos

Para ejecutar este programa, necesitas tener instalado lo siguiente en tu computadora:
1. Python 3.x (Recomendado Python 3.6 o superior).
2. Tkinter: Es la libreria estandar de Python para interfaces graficas. En la mayoria de las instalaciones de Windows y macOS, viene incluida por defecto. En Linux, puede requerir instalacion manual (ej. sudo apt-get install python3-tk).

---

## Como poner a funcionar el programa

1. Clona este repositorio o descarga los archivos en tu computadora.
2. Abre una terminal (o consola de comandos).
3. Navega hasta la carpeta donde se encuentra el archivo principal del proyecto.
4. Ejecuta el siguiente comando:

   ```bash
   python main.py

  ---

## Pruebas Unitarias Automatizadas (Unit Tests)

Además de la comprobación visual a través de la Interfaz Gráfica, este proyecto incluye un conjunto de **Pruebas Unitarias** que validan la robustez de las estructuras de datos (Heap y AVL) de forma independiente, cubriendo estrictamente los 4 casos de prueba requeridos en el documento del proyecto.
Para ejecutar las pruebas automatizadas de inserción, eliminación, indexación y equilibrio, abre la terminal en la raíz del proyecto y ejecuta:

```bash
python test_gestor.py
