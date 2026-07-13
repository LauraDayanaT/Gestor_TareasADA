from datetime import datetime

class Tarea:
    def __init__(self, id_tarea, descripcion, prioridad_texto, fecha_vencimiento):
        self.id_tarea = id_tarea
        self.descripcion = descripcion
        self.prioridad_texto = prioridad_texto
        self.fecha_vencimiento = fecha_vencimiento

        self.valor_prioridad = self._asignar_valor_prioridad(prioridad_texto)

        self.fecha_objeto = datetime.strptime(
            fecha_vencimiento,
            "%d/%m/%Y")

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
        
    def es_mas_prioritaria_que(self, otra_tarea):
        if self.valor_prioridad != otra_tarea.valor_prioridad:
            return self.valor_prioridad > otra_tarea.valor_prioridad

        return self.fecha_objeto < otra_tarea.fecha_objeto

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
        while i != 0 and self.heap[i].es_mas_prioritaria_que(self.heap[self.padre(i)]):
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

        if izq < n and self.heap[izq].es_mas_prioritaria_que(self.heap[mayor]):
            mayor = izq

        if der < n and self.heap[der].es_mas_prioritaria_que(self.heap[mayor]):
            mayor = der

        if mayor != i:
            self.heap[i], self.heap[mayor] = self.heap[mayor], self.heap[i]
            self._hundir(mayor)

    def eliminar_por_id(self, id_tarea):
        idx = -1
        for i in range(len(self.heap)):
            if self.heap[i].id_tarea == id_tarea:
                idx = i
                break

        if idx == -1: return False

        ultimo = len(self.heap) - 1
        self.heap[idx], self.heap[ultimo] = self.heap[ultimo], self.heap[idx]
        self.heap.pop()

        if idx < len(self.heap):
            padre_idx = self.padre(idx)
            if idx > 0 and self.heap[idx].es_mas_prioritaria_que(self.heap[padre_idx]):
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