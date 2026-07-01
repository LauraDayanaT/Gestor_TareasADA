import tkinter as tk
from tkinter import messagebox, ttk

class Tarea:
    def __init__(self, id_tarea, descripcion, prioridad_texto, fecha_vencimiento):
        self.id_tarea = id_tarea                  # Identificador único 
        self.descripcion = descripcion            # Descripción de la tarea 
        self.prioridad_texto = prioridad_texto    # Ej: "alta", "media", "baja" 
        self.fecha_vencimiento = fecha_vencimiento 
        
        # Asignamos un valor numérico para que el Heap pueda comparar fácilmente
        self.valor_prioridad = self._asignar_valor_prioridad(prioridad_texto)

    def _asignar_valor_prioridad(self, prioridad_texto):
        prioridad = prioridad_texto.lower()
        if prioridad == "alta":
            return 3
        elif prioridad == "media":
            return 2
        elif prioridad == "baja":
            return 1
        else:
            return 0

    def __str__(self):
        return f"ID: {self.id_tarea} | {self.descripcion} | Prioridad: {self.prioridad_texto.capitalize()} | Vence: {self.fecha_vencimiento}"
    
class MaxHeap:
    def __init__(self):
        self.heap = []

    def padre(self, i): return (i - 1) // 2
    def hijo_izquierdo(self, i): return 2 * i + 1
    def hijo_derecho(self, i): return 2 * i + 2

    def insertar(self, tarea):
        self.heap.append(tarea)
        self._flotar(len(self.heap) - 1)

    def _flotar(self, i):
        while i != 0 and self.heap[self.padre(i)].valor_prioridad < self.heap[i].valor_prioridad:
            self.heap[i], self.heap[self.padre(i)] = self.heap[self.padre(i)], self.heap[i]
            i = self.padre(i)

    def extraer_maxima_prioridad(self):
        if len(self.heap) == 0: return None 
        if len(self.heap) == 1: return self.heap.pop() 

        raiz = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._hundir(0)
        return raiz

    def _hundir(self, i):
        mayor = i
        izq = self.hijo_izquierdo(i)
        der = self.hijo_derecho(i)
        n = len(self.heap)

        if izq < n and self.heap[izq].valor_prioridad > self.heap[mayor].valor_prioridad:
            mayor = izq
        if der < n and self.heap[der].valor_prioridad > self.heap[mayor].valor_prioridad:
            mayor = der

        if mayor != i:
            self.heap[i], self.heap[mayor] = self.heap[mayor], self.heap[i]
            self._hundir(mayor)
            
    # NUEVO: Función para eliminar un ID específico del Heap
    def eliminar_por_id(self, id_tarea):
        idx = -1
        for i in range(len(self.heap)):
            if self.heap[i].id_tarea == id_tarea:
                idx = i
                break
                
        if idx == -1: return False # No se encontró
        
        ultimo = len(self.heap) - 1
        # Intercambiamos con el último
        self.heap[idx], self.heap[ultimo] = self.heap[ultimo], self.heap[idx]
        self.heap.pop() # Eliminamos el último (que era el que queríamos borrar)
        
        if idx < len(self.heap):
            # Reequilibramos el Heap (puede subir o bajar)
            padre_idx = self.padre(idx)
            if idx > 0 and self.heap[padre_idx].valor_prioridad < self.heap[idx].valor_prioridad:
                self._flotar(idx)
            else:
                self._hundir(idx)
        return True

class NodoAVL:
    def __init__(self, tarea):
        self.tarea = tarea
        self.izquierdo = None
        self.derecho = None
        self.altura = 1 

class ArbolAVL:
    def obtener_altura(self, nodo):
        if not nodo: return 0
        return nodo.altura

    def obtener_balance(self, nodo):
        if not nodo: return 0
        return self.obtener_altura(nodo.izquierdo) - self.obtener_altura(nodo.derecho)

    def rotacion_derecha(self, y):
        x = y.izquierdo
        T2 = x.derecho
        x.derecho = y
        y.izquierdo = T2
        y.altura = 1 + max(self.obtener_altura(y.izquierdo), self.obtener_altura(y.derecho))
        x.altura = 1 + max(self.obtener_altura(x.izquierdo), self.obtener_altura(x.derecho))
        return x

    def rotacion_izquierda(self, x):
        y = x.derecho
        T2 = y.izquierdo
        y.izquierdo = x
        x.derecho = T2
        x.altura = 1 + max(self.obtener_altura(x.izquierdo), self.obtener_altura(x.derecho))
        y.altura = 1 + max(self.obtener_altura(y.izquierdo), self.obtener_altura(y.derecho))
        return y

    def insertar(self, nodo, tarea):
        if not nodo:
            return NodoAVL(tarea)
        elif tarea.id_tarea < nodo.tarea.id_tarea:
            nodo.izquierdo = self.insertar(nodo.izquierdo, tarea)
        else:
            nodo.derecho = self.insertar(nodo.derecho, tarea)

        nodo.altura = 1 + max(self.obtener_altura(nodo.izquierdo), self.obtener_altura(nodo.derecho))
        balance = self.obtener_balance(nodo)

        if balance > 1 and tarea.id_tarea < nodo.izquierdo.tarea.id_tarea: return self.rotacion_derecha(nodo)
        if balance < -1 and tarea.id_tarea > nodo.derecho.tarea.id_tarea: return self.rotacion_izquierda(nodo)
        if balance > 1 and tarea.id_tarea > nodo.izquierdo.tarea.id_tarea:
            nodo.izquierdo = self.rotacion_izquierda(nodo.izquierdo)
            return self.rotacion_derecha(nodo)
        if balance < -1 and tarea.id_tarea < nodo.derecho.tarea.id_tarea:
            nodo.derecho = self.rotacion_derecha(nodo.derecho)
            return self.rotacion_izquierda(nodo)

        return nodo

    def buscar(self, nodo, id_tarea):
        if nodo is None or nodo.tarea.id_tarea == id_tarea:
            return nodo.tarea if nodo else None
        if nodo.tarea.id_tarea < id_tarea:
            return self.buscar(nodo.derecho, id_tarea)
        return self.buscar(nodo.izquierdo, id_tarea)
    
    def nodo_minimo(self, nodo):
        if nodo is None or nodo.izquierdo is None: return nodo
        return self.nodo_minimo(nodo.izquierdo)

    def eliminar(self, nodo, id_tarea):
        if not nodo: return nodo
        
        if id_tarea < nodo.tarea.id_tarea:
            nodo.izquierdo = self.eliminar(nodo.izquierdo, id_tarea)
        elif id_tarea > nodo.tarea.id_tarea:
            nodo.derecho = self.eliminar(nodo.derecho, id_tarea)
        else:
            if nodo.izquierdo is None: return nodo.derecho
            elif nodo.derecho is None: return nodo.izquierdo
            
            temp = self.nodo_minimo(nodo.derecho)
            nodo.tarea = temp.tarea
            nodo.derecho = self.eliminar(nodo.derecho, temp.tarea.id_tarea)
        
        if nodo is None: return nodo
            
        nodo.altura = 1 + max(self.obtener_altura(nodo.izquierdo), self.obtener_altura(nodo.derecho))
        balance = self.obtener_balance(nodo)
        
        if balance > 1 and self.obtener_balance(nodo.izquierdo) >= 0: return self.rotacion_derecha(nodo)
        if balance < -1 and self.obtener_balance(nodo.derecho) <= 0: return self.rotacion_izquierda(nodo)
        if balance > 1 and self.obtener_balance(nodo.izquierdo) < 0:
            nodo.izquierdo = self.rotacion_izquierda(nodo.izquierdo)
            return self.rotacion_derecha(nodo)
        if balance < -1 and self.obtener_balance(nodo.derecho) > 0:
            nodo.derecho = self.rotacion_derecha(nodo.derecho)
            return self.rotacion_izquierda(nodo)
            
        return nodo

class GestorTareas:
    def __init__(self):
        self.heap = MaxHeap()
        self.avl = ArbolAVL()
        self.raiz_avl = None 

    def agregar_tarea(self, id_tarea, descripcion, prioridad, fecha):
        nueva_tarea = Tarea(id_tarea, descripcion, prioridad, fecha)
        self.heap.insertar(nueva_tarea)
        self.raiz_avl = self.avl.insertar(self.raiz_avl, nueva_tarea)
        return nueva_tarea

    def buscar_tarea(self, id_tarea):
        return self.avl.buscar(self.raiz_avl, id_tarea)

    def completar_tarea_mas_urgente(self):
        tarea_completada = self.heap.extraer_maxima_prioridad()
        if tarea_completada:
            self.raiz_avl = self.avl.eliminar(self.raiz_avl, tarea_completada.id_tarea)
        return tarea_completada

    # NUEVO: Función general para borrar de ambas estructuras
    def eliminar_tarea(self, id_tarea):
        tarea = self.buscar_tarea(id_tarea)
        if tarea:
            self.raiz_avl = self.avl.eliminar(self.raiz_avl, id_tarea)
            self.heap.eliminar_por_id(id_tarea)
            return True
        return False

class InterfazGrafica:
    def __init__(self, root, gestor):
        self.gestor = gestor
        self.root = root
        self.root.title("Gestor de Tareas de Productividad (AVL y Max-Heap)")
        self.root.geometry("650x600") 
        
        # --- Formulario ---
        frame_entradas = tk.LabelFrame(root, text="Gestión de Tarea", padx=10, pady=10)
        frame_entradas.pack(pady=10, padx=10, fill="x")

        tk.Label(frame_entradas, text="ID de Tarea (Número):").grid(row=0, column=0, pady=5, sticky="w")
        self.entry_id = tk.Entry(frame_entradas)
        self.entry_id.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(frame_entradas, text="Descripción:").grid(row=1, column=0, pady=5, sticky="w")
        self.entry_desc = tk.Entry(frame_entradas, width=30)
        self.entry_desc.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(frame_entradas, text="Prioridad:").grid(row=2, column=0, pady=5, sticky="w")
        self.combo_prioridad = ttk.Combobox(frame_entradas, values=["Alta", "Media", "Baja"], state="readonly")
        self.combo_prioridad.grid(row=2, column=1, pady=5, padx=5)
        self.combo_prioridad.set("Media") 

        tk.Label(frame_entradas, text="Fecha de Vencimiento:").grid(row=3, column=0, pady=5, sticky="w")
        self.entry_fecha = tk.Entry(frame_entradas)
        self.entry_fecha.grid(row=3, column=1, pady=5, padx=5)

        # Botones de Agregar y Guardar Cambios (Editar)
        frame_botones_form = tk.Frame(frame_entradas)
        frame_botones_form.grid(row=4, column=0, columnspan=2, pady=10)
        
        tk.Button(frame_botones_form, text="Agregar Nueva Tarea", command=self.agregar, bg="lightblue").pack(side="left", padx=5)
        tk.Button(frame_botones_form, text="Guardar Edición", command=self.guardar_edicion, bg="lightyellow").pack(side="left", padx=5)

        # --- Controles ---
        frame_controles = tk.Frame(root)
        frame_controles.pack(pady=5)

        tk.Label(frame_controles, text="Buscar ID:").grid(row=0, column=0, padx=5)
        self.entry_buscar = tk.Entry(frame_controles, width=10)
        self.entry_buscar.grid(row=0, column=1, padx=5)
        tk.Button(frame_controles, text="Buscar (AVL)", command=self.buscar).grid(row=0, column=2, padx=5)
        
        tk.Button(frame_controles, text="Completar Más Urgente (Heap)", command=self.completar_urgente, bg="#ffcccb").grid(row=0, column=3, padx=15)

        # --- Tabla ---
        frame_tabla = tk.Frame(root)
        frame_tabla.pack(pady=10, padx=10, fill="both", expand=True)

        self.tree = ttk.Treeview(frame_tabla, columns=("ID", "Descripción", "Prioridad", "Fecha"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.heading("Prioridad", text="Prioridad")
        self.tree.heading("Fecha", text="Fecha de Venc.")
        
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Descripción", width=200)
        self.tree.column("Prioridad", width=80, anchor="center")
        self.tree.column("Fecha", width=120, anchor="center")
        self.tree.pack(fill="both", expand=True)

        # --- Botones de la tabla ---
        frame_acciones_tabla = tk.Frame(root)
        frame_acciones_tabla.pack(pady=5)
        tk.Button(frame_acciones_tabla, text="Cargar para Editar", command=self.cargar_para_editar).pack(side="left", padx=10)
        # AQUÍ CAMBIAMOS EL NOMBRE DEL BOTÓN Y EL COLOR
        tk.Button(frame_acciones_tabla, text="Marcar como Completada", command=self.marcar_completada_seleccionada, bg="lightgreen").pack(side="left", padx=10)

    # --- Lógica de la interfaz ---
    def agregar(self):
        try:
            id_tarea = int(self.entry_id.get())
            desc = self.entry_desc.get()
            prioridad = self.combo_prioridad.get()
            fecha = self.entry_fecha.get()

            if not desc or not fecha:
                messagebox.showwarning("Faltan datos", "Por favor llena todos los campos.")
                return

            if self.gestor.buscar_tarea(id_tarea):
                messagebox.showerror("Error", f"La tarea con ID {id_tarea} ya existe.")
                return

            self.gestor.agregar_tarea(id_tarea, desc, prioridad, fecha)
            self.limpiar_campos()
            self.actualizar_tabla()
            
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número entero (ej: 101).")

    def completar_urgente(self):
        tarea = self.gestor.completar_tarea_mas_urgente()
        if tarea:
            messagebox.showinfo("Completada", f"Has completado automáticamente la tarea más urgente:\n{tarea.descripcion}\n(Prioridad: {tarea.prioridad_texto})")
            self.actualizar_tabla()
        else:
            messagebox.showinfo("Lista Vacía", "No hay tareas pendientes en el sistema.")

    def buscar(self):
        try:
            id_buscar = int(self.entry_buscar.get())
            tarea = self.gestor.buscar_tarea(id_buscar)
            if tarea:
                messagebox.showinfo("Tarea Encontrada", f"Resultados:\n\n{tarea}")
            else:
                messagebox.showwarning("No Encontrada", f"No se encontró la tarea con ID {id_buscar}.")
        except ValueError:
            messagebox.showerror("Error", "Ingresa un ID válido.")

    # AHORA ESTA FUNCIÓN SE LLAMA MARCAR COMO COMPLETADA
    def marcar_completada_seleccionada(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Por favor selecciona una tarea de la tabla primero.")
            return
        
        item = self.tree.item(seleccion[0])
        id_tarea = int(item['values'][0])
        desc_tarea = item['values'][1]
        
        # Llama a gestor.eliminar_tarea que la borra del Heap y del AVL como pide el profesor
        if self.gestor.eliminar_tarea(id_tarea):
            messagebox.showinfo("Tarea Completada", f"¡Excelente! Marcaste como completada la tarea:\n'{desc_tarea}'\n\nSe ha eliminado del sistema (AVL y Heap).")
            self.actualizar_tabla()

    def cargar_para_editar(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona una tarea de la tabla para editar.")
            return
        
        item = self.tree.item(seleccion[0])
        valores = item['values']
        
        self.limpiar_campos()
        self.entry_id.insert(0, valores[0])
        self.entry_id.config(state="disabled")
        self.entry_desc.insert(0, valores[1])
        self.combo_prioridad.set(valores[2])
        self.entry_fecha.insert(0, valores[3])
        messagebox.showinfo("Modo Edición", "Datos cargados. Modifica lo que necesites y presiona 'Guardar Edición'.")

    def guardar_edicion(self):
        if self.entry_id.cget("state") == "normal":
            messagebox.showwarning("Aviso", "Primero usa el botón 'Cargar para Editar' en la tabla.")
            return
            
        self.entry_id.config(state="normal") 
        id_tarea = int(self.entry_id.get())
        desc = self.entry_desc.get()
        prioridad = self.combo_prioridad.get()
        fecha = self.entry_fecha.get()
        
        self.gestor.eliminar_tarea(id_tarea)
        self.gestor.agregar_tarea(id_tarea, desc, prioridad, fecha)
        
        self.limpiar_campos()
        messagebox.showinfo("Éxito", "Tarea actualizada correctamente.")
        self.actualizar_tabla()

    def limpiar_campos(self):
        self.entry_id.config(state="normal")
        self.entry_id.delete(0, tk.END)
        self.entry_desc.delete(0, tk.END)
        self.entry_fecha.delete(0, tk.END)

    def actualizar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        tareas_visuales = sorted(self.gestor.heap.heap, key=lambda t: t.valor_prioridad, reverse=True)
        for t in tareas_visuales:
            self.tree.insert("", tk.END, values=(t.id_tarea, t.descripcion, t.prioridad_texto.capitalize(), t.fecha_vencimiento))

if __name__ == "__main__":
    ventana_principal = tk.Tk()
    gestor_principal = GestorTareas()
    app = InterfazGrafica(ventana_principal, gestor_principal)
    ventana_principal.mainloop()

    # --- Lógica de la interfaz ---
    def agregar(self):
        try:
            id_tarea = int(self.entry_id.get())
            desc = self.entry_desc.get()
            prioridad = self.combo_prioridad.get()
            fecha = self.entry_fecha.get()

            if not desc or not fecha:
                messagebox.showwarning("Faltan datos", "Por favor llena todos los campos.")
                return

            if self.gestor.buscar_tarea(id_tarea):
                messagebox.showerror("Error", f"La tarea con ID {id_tarea} ya existe.")
                return

            self.gestor.agregar_tarea(id_tarea, desc, prioridad, fecha)
            self.limpiar_campos()
            self.actualizar_tabla()
            
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número entero (ej: 101).")

    def completar_urgente(self):
        tarea = self.gestor.completar_tarea_mas_urgente()
        if tarea:
            messagebox.showinfo("Completada", f"Has completado la tarea:\n{tarea.descripcion}\n(Prioridad: {tarea.prioridad_texto})")
            self.actualizar_tabla()
        else:
            messagebox.showinfo("Lista Vacía", "No hay tareas pendientes en el sistema.")

    def buscar(self):
        try:
            id_buscar = int(self.entry_buscar.get())
            tarea = self.gestor.buscar_tarea(id_buscar)
            if tarea:
                messagebox.showinfo("Tarea Encontrada", f"Resultados:\n\n{tarea}")
            else:
                messagebox.showwarning("No Encontrada", f"No se encontró la tarea con ID {id_buscar}.")
        except ValueError:
            messagebox.showerror("Error", "Ingresa un ID válido.")

    # NUEVO: Lógica para eliminar de la tabla
    def eliminar_seleccionada(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Por favor selecciona una tarea de la tabla primero.")
            return
        
        item = self.tree.item(seleccion[0])
        id_tarea = int(item['values'][0])
        
        if self.gestor.eliminar_tarea(id_tarea):
            messagebox.showinfo("Éxito", f"Tarea {id_tarea} eliminada correctamente.")
            self.actualizar_tabla()

    # NUEVO: Pone los datos de la tabla en los recuadros de arriba
    def cargar_para_editar(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona una tarea de la tabla para editar.")
            return
        
        item = self.tree.item(seleccion[0])
        valores = item['values']
        
        self.limpiar_campos()
        self.entry_id.insert(0, valores[0])
        self.entry_id.config(state="disabled") # Bloqueamos el ID para que no lo cambien en la edición
        self.entry_desc.insert(0, valores[1])
        self.combo_prioridad.set(valores[2])
        self.entry_fecha.insert(0, valores[3])
        messagebox.showinfo("Modo Edición", "Datos cargados. Modifica lo que necesites y presiona 'Guardar Edición'.")

    # NUEVO: Guarda la tarea editada
    def guardar_edicion(self):
        if self.entry_id.cget("state") == "normal":
            messagebox.showwarning("Aviso", "Primero usa el botón 'Cargar para Editar' en la tabla.")
            return
            
        self.entry_id.config(state="normal") # Desbloqueamos para leer el ID
        id_tarea = int(self.entry_id.get())
        desc = self.entry_desc.get()
        prioridad = self.combo_prioridad.get()
        fecha = self.entry_fecha.get()
        
        # Eliminamos la versión vieja y metemos la nueva actualizada
        self.gestor.eliminar_tarea(id_tarea)
        self.gestor.agregar_tarea(id_tarea, desc, prioridad, fecha)
        
        self.limpiar_campos()
        messagebox.showinfo("Éxito", "Tarea actualizada correctamente.")
        self.actualizar_tabla()

    def limpiar_campos(self):
        self.entry_id.config(state="normal")
        self.entry_id.delete(0, tk.END)
        self.entry_desc.delete(0, tk.END)
        self.entry_fecha.delete(0, tk.END)

    def actualizar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        tareas_visuales = sorted(self.gestor.heap.heap, key=lambda t: t.valor_prioridad, reverse=True)
        for t in tareas_visuales:
            self.tree.insert("", tk.END, values=(t.id_tarea, t.descripcion, t.prioridad_texto.capitalize(), t.fecha_vencimiento))

if __name__ == "__main__":
    ventana_principal = tk.Tk()
    gestor_principal = GestorTareas()
    app = InterfazGrafica(ventana_principal, gestor_principal)
    ventana_principal.mainloop()