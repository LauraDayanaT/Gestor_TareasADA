import unittest
from main import GestorTareas

class TestGestorTareas(unittest.TestCase):

    def setUp(self):
        # Esto se ejecuta antes de cada prueba para tener un gestor limpio
        self.gestor = GestorTareas()

    def test_prueba_insercion(self):
        """Prueba de inserción: Verificar orden de extracción (Heap)"""
        self.gestor.agregar_tarea(101, "Baja urgencia", "Baja", "Mañana")
        self.gestor.agregar_tarea(102, "Alta urgencia", "Alta", "Hoy")
        self.gestor.agregar_tarea(103, "Media urgencia", "Media", "Tarde")

        # Al extraer, DEBE salir primero la de prioridad Alta (ID 102)
        tarea_urgente = self.gestor.completar_tarea_mas_urgente()
        self.assertEqual(tarea_urgente.id_tarea, 102)
        
        # Luego la Media (ID 103)
        tarea_medio = self.gestor.completar_tarea_mas_urgente()
        self.assertEqual(tarea_medio.id_tarea, 103)

    def test_prueba_eliminacion(self):
        """Prueba de eliminación: Asegurar que se elimina del Heap y AVL"""
        self.gestor.agregar_tarea(1, "Tarea de prueba", "Alta", "Hoy")
        self.gestor.agregar_tarea(2, "Otra tarea", "Media", "Hoy")
        
        # Eliminamos la tarea 1 manualmente
        eliminado = self.gestor.eliminar_tarea(1)
        self.assertTrue(eliminado)
        
        # Verificamos que ya no existe en el AVL
        tarea_buscada = self.gestor.buscar_tarea(1)
        self.assertIsNone(tarea_buscada)
        
        # Verificamos que la que queda en el Heap es la tarea 2
        tarea_restante = self.gestor.completar_tarea_mas_urgente()
        self.assertEqual(tarea_restante.id_tarea, 2)

    def test_prueba_indexacion(self):
        """Prueba de indexación: Buscar elementos en el AVL"""
        self.gestor.agregar_tarea(500, "Encontrar la aguja", "Baja", "Nunca")
        
        # Buscamos la tarea por su ID
        tarea = self.gestor.buscar_tarea(500)
        self.assertIsNotNone(tarea)
        self.assertEqual(tarea.descripcion, "Encontrar la aguja")
        
        # Buscamos un ID que no existe
        tarea_falsa = self.gestor.buscar_tarea(999)
        self.assertIsNone(tarea_falsa)

    def test_prueba_equilibrio(self):
        """Prueba de equilibrio: Inserción desbalanceada y rotación AVL"""
        # Insertamos IDs en orden secuencial (el peor caso para un árbol binario normal)
        self.gestor.agregar_tarea(1, "Uno", "Baja", "-")
        self.gestor.agregar_tarea(2, "Dos", "Baja", "-")
        self.gestor.agregar_tarea(3, "Tres", "Baja", "-")
        
        # Si el árbol AVL no rotara, la raíz seguiría siendo el ID 1, y el 2 y 3 serían hijos derechos.
        # Gracias a la rotación izquierda automática del AVL, la nueva raíz DEBE ser el ID 2.
        raiz_actual = self.gestor.raiz_avl.tarea.id_tarea
        self.assertEqual(raiz_actual, 2)

if __name__ == "__main__":
    unittest.main()