import tkinter as tk
import json
from datetime import datetime
from tkinter import messagebox, ttk
from estructuras import Tarea, MaxHeap, ArbolAVL


class GestorTareas:
    ARCHIVO = "tareas.json"

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

    def eliminar_tarea(self, id_tarea):
        tarea = self.buscar_tarea(id_tarea)
        if tarea:
            self.raiz_avl = self.avl.eliminar(self.raiz_avl, id_tarea)
            self.heap.eliminar_por_id(id_tarea)
            return True
        return False

    def guardar_en_archivo(self):
        tareas = self.avl.recorrido_inorden(self.raiz_avl)
        datos = [
            {"id": t.id_tarea, "descripcion": t.descripcion,
             "prioridad": t.prioridad_texto, "fecha": t.fecha_vencimiento}
            for t in tareas
        ]
        with open(self.ARCHIVO, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)

    def cargar_desde_archivo(self):
        try:
            with open(self.ARCHIVO, "r", encoding="utf-8") as f:
                datos = json.load(f)
            for d in datos:
                self.agregar_tarea(d["id"], d["descripcion"], d["prioridad"], d["fecha"])
        except FileNotFoundError:
            pass



class InterfazGrafica:
    def __init__(self, root, gestor):
        self.gestor = gestor
        self.gestor.cargar_desde_archivo()
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
        tk.Button(frame_acciones_tabla, text="Marcar como Completada", command=self.marcar_completada_seleccionada, bg="lightgreen").pack(side="left", padx=10)

        self.actualizar_tabla()
        self.root.protocol("WM_DELETE_WINDOW", self.al_cerrar)

        # Valida que la fecha ingresada tenga el formato correcto DD/MM/AAAA
    def validar_fecha(self, fecha):
        try:
            datetime.strptime(fecha, "%d/%m/%Y")
            return True
        except ValueError:
            return False

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
            
            if not self.validar_fecha(fecha):
                messagebox.showerror(
                    "Fecha inválida",
                    "La fecha debe tener el formato DD/MM/AAAA.\nEjemplo: 15/07/2026")
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

    def marcar_completada_seleccionada(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Por favor selecciona una tarea de la tabla primero.")
            return

        item = self.tree.item(seleccion[0])
        id_tarea = int(item['values'][0])
        desc_tarea = item['values'][1]

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
        if not desc or not fecha:
            messagebox.showwarning(
                "Faltan datos",
                "Por favor llena todos los campos.")
            self.entry_id.config(state="disabled")
            return

        if not self.validar_fecha(fecha):
            messagebox.showerror(
                "Fecha inválida",
                "La fecha debe tener el formato DD/MM/AAAA.\nEjemplo: 15/07/2026")
            self.entry_id.config(state="disabled")
            return

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

        # Ordena las tareas por prioridad y, en caso de empate,
        # por la fecha de vencimiento más cercana
        tareas_visuales = sorted(
            self.gestor.heap.heap,
            key=lambda t: (-t.valor_prioridad, t.fecha_objeto))
        for t in tareas_visuales:
            self.tree.insert("", tk.END, values=(t.id_tarea, t.descripcion, t.prioridad_texto.capitalize(), t.fecha_vencimiento))

    def al_cerrar(self):
        self.gestor.guardar_en_archivo()
        self.root.destroy()

if __name__ == "__main__":
    ventana_principal = tk.Tk()
    gestor_principal = GestorTareas()
    app = InterfazGrafica(ventana_principal, gestor_principal)
    ventana_principal.mainloop()