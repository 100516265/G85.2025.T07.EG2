"""Tests for the AccountDeposit class"""
import unittest
import hashlib
import sys
import os
from freezegun import freeze_time
from uc3m_money.account_deposit import AccountDeposit
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.json_manager import JsonManager

# Añadimos el path para poder importar los módulos necesarios
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../main/python")))

# Fecha de congelación para los tests
FREEZE_DATE = "2024-03-22 10:00:00"

# Datos de prueba para simular el JSON de entrada
INPUT_FILE = "RF2/deposit_requests.json"
STORAGE_FILE = "RF2/deposit_store.json"

class TestAccountDeposit(unittest.TestCase):
    """Class for testing the AccountDeposit class"""

    @freeze_time(FREEZE_DATE)
    def test_valid_tc1(self):
        """Test for the deposit_request method"""

        JsonManager(INPUT_FILE).delete()
        JsonManager(STORAGE_FILE).delete()
        json_entrada = JsonManager(INPUT_FILE)
        json_salida = JsonManager(STORAGE_FILE)
        lectura = json_entrada.read_json()
        lectura.append({"IBAN": "ES4500817294770123456789", "AMOUNT": "EUR1200.23"})
        json_entrada.write_json(lectura)

        expected_signature = hashlib.sha256(
            "{alg:SHA-256,typ:DEPOSIT,"
            "iban:ES4500817294770123456789,amount:1200.23,"
            "deposit_date:1711101600.0}".encode()
        ).hexdigest()

        result = AccountDeposit.deposit_into_account(INPUT_FILE)

        self.assertEqual(result, expected_signature)
        self.assertTrue(json_salida.bien_registrado_rf2(result),
                        "La transferencia no se guardó correctamente")

    @freeze_time(FREEZE_DATE)
    def test_invalid_tc1(self):
        """Test with empty JSON object"""

        json_entrada = JsonManager(INPUT_FILE)
        json_entrada.write_json([{}])

        with self.assertRaises(AccountManagementException) as cm:
            AccountDeposit.deposit_into_account(INPUT_FILE)
        self.assertEqual(str(cm.exception), "Excepción: El JSON no tiene la estructura esperada.")

    @freeze_time(FREEZE_DATE)
    def test_invalid_tc2(self):
        """Test with missing closing bracket"""

        json_entrada = JsonManager(INPUT_FILE)
        json_entrada.write_json(['{ "IBAN" : "ES4500817294770123456789" , "AMOUNT" : "EUR1200.23"'])

        with self.assertRaises(AccountManagementException) as cm:
            AccountDeposit.deposit_into_account(INPUT_FILE)
        self.assertEqual(str(cm.exception),
                             "Excepción: El JSON no tiene la estructura esperada.")

    @freeze_time(FREEZE_DATE)
    def test_invalid_tc3(self):
        """Test with missing curly braces"""

        json_entrada = JsonManager(INPUT_FILE)
        json_entrada.write_json(['"IBAN : "ES4500817294770123456789" , AMOUNT : "EUR1200.23" }'])

        with self.assertRaises(AccountManagementException) as cm:
            AccountDeposit.deposit_into_account(INPUT_FILE)
        self.assertEqual(str(cm.exception),
                             "Excepción: El JSON no tiene la estructura esperada.")

    @freeze_time(FREEZE_DATE)
    def test_invalid_tc4(self):
        """Test with double opening curly braces"""

        json_entrada = JsonManager(INPUT_FILE)
        json_entrada.write_json(
            ['{{ "IBAN" : "ES4500817294770123456789" , "AMOUNT" : "EUR1200.23" }'])

        with self.assertRaises(AccountManagementException) as cm:
            AccountDeposit.deposit_into_account(INPUT_FILE)
        self.assertEqual(str(cm.exception),
                             "Excepción: El JSON no tiene la estructura esperada.")

    @freeze_time(FREEZE_DATE)
    def test_invalid_tc5(self):
        """Test with missing IBAN key"""

        json_entrada = JsonManager(INPUT_FILE)
        json_entrada.write_json([{"AMOUNT": "EUR1200.23"}])

        with self.assertRaises(AccountManagementException) as cm:
            AccountDeposit.deposit_into_account(INPUT_FILE)
        self.assertEqual(str(cm.exception), "Excepción: El JSON no tiene la estructura esperada.")

    @freeze_time(FREEZE_DATE)
    def test_invalid_tc6(self):
        """Test with trailing comma"""

        json_entrada = JsonManager(INPUT_FILE)
        json_entrada.write_json(['{ "IBAN" : "ES4500817294770123456789", }'])

        with self.assertRaises(AccountManagementException) as cm:
            AccountDeposit.deposit_into_account(INPUT_FILE)
        self.assertEqual(str(cm.exception),
                         "Excepción: El JSON no tiene la estructura esperada.")



    @freeze_time(FREEZE_DATE)
    def test_invalid_tc7(self):
        """Test with trailing comma"""

        json_entrada = JsonManager(INPUT_FILE)
        json_entrada.write_json(['{  : "ES4500817294770123456789" , "AMOUNT" : "EUR1200.23" }'])

        with self.assertRaises(AccountManagementException) as cm:
            AccountDeposit.deposit_into_account(INPUT_FILE)
        self.assertEqual(str(cm.exception),
                             "Excepción: El JSON no tiene la estructura esperada.")


    @freeze_time(FREEZE_DATE)
    def test_invalid_tc8(self):
        """test within comillas"""

        json_entrada = JsonManager(INPUT_FILE)
        json_entrada.write_json(['{"IBAN": "ES4500817294770123456789" , "AMOUNT": EUR1200.23"}'])

        with self.assertRaises(AccountManagementException) as cm:
            AccountDeposit.deposit_into_account(INPUT_FILE)
        self.assertEqual(str(cm.exception),
                             "Excepción: El JSON no tiene la estructura esperada.")

    @freeze_time(FREEZE_DATE)
    def test_invalid_tc9(self):
        """test with an invalid IBAN"""

        json_entrada = JsonManager(INPUT_FILE)
        json_entrada.write_json([{ "IBAN" : "ESABCD" , "AMOUNT" : "EUR1200.23" }])

        with self.assertRaises(AccountManagementException) as cm:
            AccountDeposit.deposit_into_account(INPUT_FILE)
        self.assertEqual(str(cm.exception),
                         "Excepción: Los datos del JSON no tienen valores válidos.")

    @freeze_time(FREEZE_DATE)
    def test_invalid_tc10(self):
        """test with an invalid IBAN"""

        json_entrada = JsonManager(INPUT_FILE)
        json_entrada.write_json([{ "IBAN" : "ES45008172947701234567894500817294770123456789" ,
                                    "AMOUNT" : "EUR1200.23" }])

        with self.assertRaises(AccountManagementException) as cm:
            AccountDeposit.deposit_into_account(INPUT_FILE)
        self.assertEqual(str(cm.exception),
                         "Excepción: Los datos del JSON no tienen valores válidos.")

    @freeze_time(FREEZE_DATE)
    def test_invalid_tc11(self):
        """test with an invalid IBAN"""

        json_entrada = JsonManager(INPUT_FILE)
        json_entrada.write_json([{ "IBAN" : "ES" , "AMOUNT" : "EUR1200.23" }])

        with self.assertRaises(AccountManagementException) as cm:
            AccountDeposit.deposit_into_account(INPUT_FILE)
        self.assertEqual(str(cm.exception),
                         "Excepción: Los datos del JSON no tienen valores válidos.")

    @freeze_time(FREEZE_DATE)
    def test_invalid_tc12(self):
        """test with an invalid IBAN"""

        json_entrada = JsonManager(INPUT_FILE)
        json_entrada.write_json([{ "IBAN" : "4500817294770123456789" , "AMOUNT" : "EUR1200.23" }])

        with self.assertRaises(AccountManagementException) as cm:
            AccountDeposit.deposit_into_account(INPUT_FILE)
        self.assertEqual(str(cm.exception),
                         "Excepción: Los datos del JSON no tienen valores válidos.")

    @freeze_time(FREEZE_DATE)
    def test_invalid_tc13(self):
        """test with an invalid AMOUNT"""

        json_entrada = JsonManager(INPUT_FILE)
        json_entrada.write_json([{ "IBAN" : "ES4500817294770123456789" , "AMOUNT" : "EURA200.23" }])

        with self.assertRaises(AccountManagementException) as cm:
            AccountDeposit.deposit_into_account(INPUT_FILE)
        self.assertEqual(str(cm.exception),
                         "Excepción: Los datos del JSON no tienen valores válidos.")

    @freeze_time(FREEZE_DATE)
    def test_invalid_tc14(self):
        """test with an invalid AMOUNT"""

        json_entrada = JsonManager(INPUT_FILE)
        json_entrada.write_json([{ "IBAN" : "ES4500817294770123456789" ,
                                   "AMOUNT" : "EUR11200.23" }])

        with self.assertRaises(AccountManagementException) as cm:
            AccountDeposit.deposit_into_account(INPUT_FILE)
        self.assertEqual(str(cm.exception),
                         "Excepción: Los datos del JSON no tienen valores válidos.")


if __name__ == "__main__":
    unittest.main()
