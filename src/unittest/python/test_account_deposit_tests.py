import unittest
import hashlib
import sys
import os
from freezegun import freeze_time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../main/python")))
from uc3m_money.account_manager import AccountManager
from uc3m_money.account_deposit import AccountDeposit
from uc3m_money.json_manager import JsonManager
from uc3m_money.account_management_exception import AccountManagementException

freeze_date = "2024-03-22 10:00:00"

# Datos de prueba para simular el JSON de entrada
input_file = "RF2/deposit_requests.json"
storage_file = "RF2/deposit_store.json"

class TestAccountDeposit(unittest.TestCase):
    """Class for testing the AccountDeposit class"""

    @freeze_time(freeze_date)
    def test_valid_deposit_1(self):
        """Test for the deposit_request method"""
        json_entrada = JsonManager(input_file)
        json_salida = JsonManager(storage_file)

        lectura=json_entrada.read_json()
        lectura.append({ "IBAN" : "ES4500817294770123456789" , "AMOUNT": "EUR1200.23" })
        json_entrada.write_json((lectura))

        expected_signature = hashlib.sha256(
            "{alg:SHA-256,typ:DEPOSIT,iban:ES4500817294770123456789,amount:1200.23,deposit_date:1711101600.0}".encode()
        ).hexdigest()

        result = AccountDeposit.deposit_into_account(input_file)


        self.assertEqual(result, expected_signature)
        self.assertTrue(json_salida.bien_registrado_RF2(result), "La transferencia no se guardo correctamente")


    @freeze_time(freeze_date)
    def test_valid_deposit_2(self):

        json_entrada = JsonManager(input_file)

        lectura = json_entrada.read_json()
        lectura.append({})
        json_entrada.write_json((lectura))

        with self.assertRaises(AccountManagementException) as cm:
            AccountDeposit.deposit_into_account(input_file)

        self.assertEqual(cm.exception.message, "Excepción: El JSON no tiene la estructura esperada.")




if __name__ == "__main__":
    unittest.main()
