"""Módulo de pruebas  para el módulo json_manager"""
import unittest
from uc3m_money.json_manager import JsonManager
from uc3m_money.account_management_exception import AccountManagementException

TEST_JSON_FILE = "test.json"


class TestJsonManager(unittest.TestCase):
    """Clase de pruebas para el módulo JsonManager"""
    def auto_eliminar(self):
        """Elimina el archivo de prueba si existe"""
        JsonManager(TEST_JSON_FILE).delete()

    def test_case_tc1(self):
        """Verifica que leer un JSON vacío devuelve una lista vacía"""
        json_manager = JsonManager(TEST_JSON_FILE)
        self.assertEqual(json_manager.read_json(), [])

    def test_case_tc2(self):
        """Verifica que leer un JSON mal formado lanza una excepción"""
        json_manager = JsonManager(TEST_JSON_FILE)

        with open(json_manager.json_path, "w", encoding="utf-8") as file:
            file.write("{abcf}")

        with self.assertRaises(AccountManagementException) as cm:
            json_manager.read_json()
        self.assertEqual(str(cm.exception), "ERROR: FORMATO JSON INCORRECTO.")
        self.auto_eliminar()

    def test_case_tc3(self):
        """Verifica que se pueden escribir y leer datos en el JSON"""
        json_manager = JsonManager(TEST_JSON_FILE)

        data = [{"transfer_code": "12345"}]
        json_manager.write_json(data)
        self.assertEqual(json_manager.read_json(), data)
        self.auto_eliminar()

    def test_case_tc4(self):
        """Verifica que bien_registrado encuentra una transferencia existente"""
        json_manager = JsonManager(TEST_JSON_FILE)

        data = [{"transfer_code": "abc123"}]
        json_manager.write_json(data)
        self.assertTrue(json_manager.bien_registrado("abc123"))
        self.auto_eliminar()

    def test_case_tc5(self):
        """Verifica que bien_registrado devuelve False si la transferencia no existe"""
        json_manager = JsonManager(TEST_JSON_FILE)

        data = [{"transfer_code": "abc123"}]
        json_manager.write_json(data)
        self.assertFalse(json_manager.bien_registrado("xyz789"))
        self.auto_eliminar()

    def test_case_tc6(self):
        """Verifica que el hash generado no cambia si el contenido del JSON es el mismo"""
        json_manager = JsonManager(TEST_JSON_FILE)

        data = [{"transfer_code": "123"}]
        json_manager.write_json(data)
        hash1 = json_manager.generate_hash()

        # Simula el mismo contenido para verificar que el hash es el mismo
        json_manager.write_json(data)
        hash2 = json_manager.generate_hash()
        self.assertEqual(hash1, hash2)
        self.auto_eliminar()

if __name__ == "__main__":
    unittest.main()
