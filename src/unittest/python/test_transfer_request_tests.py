"""class for testing the register_order method"""
import unittest
import sys
import os
from freezegun import freeze_time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../main/python")))
from uc3m_money.transfer_request import TransferRequest
from uc3m_money.account_manager import AccountManager
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.json_manager import JsonManager

freeze_date = "2024-03-22 10:00:00"

class MyTestCase(unittest.TestCase):
    """class for testing the register_order method"""
    """Tests for the AccountManager's transfer request"""

    @freeze_time(freeze_date)
    def test_valid_TC1(self):
        """Valid transfer request"""
        my_manager = AccountManager()
        json_manager = JsonManager("RF1/transfer_requests.json")
        from_iban_to_test = "ES9121000418450200051332"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "text valid"
        amount_to_test = 10.00
        date_to_test = "01/01/2025"
        type_to_test = "ORDINARY"
        with freeze_time(freeze_date):
            result = my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(result, "264e833dbab20a7840492a753af7301a")
            self.assertTrue(json_manager.bien_registrado(result), "La transferencia no se guardo correctamente")


    @freeze_time(freeze_date)
    def test_valid_TC2(self):

        my_manager = AccountManager()
        json_manager = JsonManager("RF1/transfer_requests.json")
        from_iban_to_test = "ES9121000418450200051332"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "concept val"
        amount_to_test = 10.01
        date_to_test = "02/02/2026"
        type_to_test = "URGENT"
        with freeze_time(freeze_date):
            result = my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(result, "edec2f7f43bb746f6819efff114d13b7")
            self.assertTrue(json_manager.bien_registrado(result), "La transferencia no se guardo correctamente")


    @freeze_time(freeze_date)
    def test_valid_TC3(self):

        my_manager = AccountManager()
        json_manager = JsonManager("RF1/transfer_requests.json")
        from_iban_to_test = "ES9121000418450200051332"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "transferencia inmediata viaje"
        amount_to_test = 9999.99
        date_to_test = "30/11/2049"
        type_to_test = "INMEDIATE"
        with freeze_time(freeze_date):
            result = my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(result, "f03535650dc76d640625f2f3414671bf")
            self.assertTrue(json_manager.bien_registrado(result), "La transferencia no se guardo correctamente")


    @freeze_time(freeze_date)
    def test_valid_TC4(self):

        my_manager = AccountManager()
        json_manager = JsonManager("RF1/transfer_requests.json")
        from_iban_to_test = "ES9121000418450200051332"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "transfere compra semana pasada"
        amount_to_test = 400.3
        date_to_test = "31/12/2050"
        type_to_test = "ORDINARY"
        with freeze_time(freeze_date):
            result = my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(result, "bdeb29173a5c8aaea92b8a9be0dbb03b")
            self.assertTrue(json_manager.bien_registrado(result), "La transferencia no se guardo correctamente")

    @freeze_time(freeze_date)
    def test_invalid_TC5(self):

        my_manager = AccountManager()
        json_manager = JsonManager("RF1/transfer_requests.json")
        from_iban_to_test = "123"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "text valid"
        amount_to_test = 10.00
        date_to_test = "01/01/2025"
        type_to_test = "ORDINARY"
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(cm.exception.message, "Excepción: Los números de cuenta (from) recibidos no son válidos.")
            self.assertTrue(json_manager.comprobar_json(len(json_manager)), "La transferencia no válida ha modificado el JSON")



    @freeze_time(freeze_date)
    def test_invalid_TC6(self):
        my_manager = AccountManager()
        json_manager = JsonManager("RF1/transfer_requests.json")
        from_iban_to_test = "ES3400491500950012345679"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "text valid"
        amount_to_test = 10.00
        date_to_test = "01/01/2025"
        type_to_test = "ORDINARY"
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(cm.exception.message, "Excepción: Los números de cuenta (from) recibidos no son válidos.")
            self.assertTrue(json_manager.comprobar_json(len(json_manager)),"La transferencia no válida ha modificado el JSON")



    @freeze_time(freeze_date)
    def test_invalid_TC7(self):

        my_manager = AccountManager()
        json_manager = JsonManager("RF1/transfer_requests.json")
        from_iban_to_test = "S34004915009500123456780"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "text valid"
        amount_to_test = 10.00
        date_to_test = "01/01/2025"
        type_to_test = "ORDINARY"
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(cm.exception.message, "Excepción: Los números de cuenta (from) recibidos no son válidos.")
            self.assertTrue(json_manager.comprobar_json(len(json_manager)),"La transferencia no válida ha modificado el JSON")



    @freeze_time(freeze_date)
    def test_invalid_TC8(self):

        my_manager = AccountManager()
        json_manager = JsonManager("RF1/transfer_requests.json")
        from_iban_to_test = "ES23456789UYTR3456789654"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "text valid"
        amount_to_test = 10.00
        date_to_test = "01/01/2025"
        type_to_test = "ORDINARY"
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(cm.exception.message, "Excepción: Los números de cuenta (from) recibidos no son válidos.")
            self.assertTrue(json_manager.comprobar_json(len(json_manager)),"La transferencia no válida ha modificado el JSON")




    @freeze_time(freeze_date)
    def test_invalid_TC9(self):

        my_manager = AccountManager()
        json_manager = JsonManager("RF1/transfer_requests.json")
        from_iban_to_test = "ES123456789123456789112"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "text valid"
        amount_to_test = 10.00
        date_to_test = "01/01/2025"
        type_to_test = "ORDINARY"
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(cm.exception.message, "Excepción: Los números de cuenta (from) recibidos no son válidos.")
            self.assertTrue(json_manager.comprobar_json(len(json_manager)),"La transferencia no válida ha modificado el JSON")



    @freeze_time(freeze_date)
    def test_invalid_TC10(self):

        my_manager = AccountManager()
        json_manager = JsonManager("RF1/transfer_requests.json")
        from_iban_to_test = "ES34004915009500123456791"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "text valid"
        amount_to_test = 10.00
        date_to_test = "01/01/2025"
        type_to_test = "ORDINARY"
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(cm.exception.message, "Excepción: Los números de cuenta (from) recibidos no son válidos.")
            self.assertTrue(json_manager.comprobar_json(len(json_manager)),"La transferencia no válida ha modificado el JSON")





    @freeze_time(freeze_date)
    def test_invalid_TC11(self):

        my_manager = AccountManager()
        json_manager = JsonManager("RF1/transfer_requests.json")
        from_iban_to_test = "ES9121000418450200051332"
        to_iban_to_test = "123"
        concept_to_test = "text valid"
        amount_to_test = 10.00
        date_to_test = "01/01/2025"
        type_to_test = "ORDINARY"
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(cm.exception.message, "Excepcion: Los números de cuenta (to) recibidos no son válidos.")
            self.assertTrue(json_manager.comprobar_json(len(json_manager)),"La transferencia no válida ha modificado el JSON")





    @freeze_time(freeze_date)
    def test_invalid_TC12(self):

        my_manager = AccountManager()
        json_manager = JsonManager("RF1/transfer_requests.json")
        from_iban_to_test = "ES9121000418450200051332"
        to_iban_to_test = "ES3400491500950012345679"
        concept_to_test = "text valid"
        amount_to_test = 10.00
        date_to_test = "01/01/2025"
        type_to_test = "ORDINARY"
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(cm.exception.message, "Excepcion: Los números de cuenta (to) recibidos no son válidos.")
            self.assertTrue(json_manager.comprobar_json(len(json_manager)),"La transferencia no válida ha modificado el JSON")




    @freeze_time(freeze_date)
    def test_invalid_TC13(self):

        my_manager = AccountManager()
        json_manager = JsonManager("RF1/transfer_requests.json")
        from_iban_to_test = "ES9121000418450200051332"
        to_iban_to_test = "S34004915009500123456780"
        concept_to_test = "text validt"
        amount_to_test = 10.00
        date_to_test = "01/01/2025"
        type_to_test = "ORDINARY"
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(cm.exception.message, "Excepcion: Los números de cuenta (to) recibidos no son válidos.")
            self.assertTrue(json_manager.comprobar_json(len(json_manager)),"La transferencia no válida ha modificado el JSON")






    @freeze_time(freeze_date)
    def test_invalid_TC14(self):

        my_manager = AccountManager()
        json_manager = JsonManager("RF1/transfer_requests.json")
        from_iban_to_test = "ES9121000418450200051332"
        to_iban_to_test = "ES23456789UYTR3456789654"
        concept_to_test = "text valid"
        amount_to_test = 10.00
        date_to_test = "01/01/2025"
        type_to_test = "ORDINARY"
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(cm.exception.message, "Excepcion: Los números de cuenta (to) recibidos no son válidos.")
            self.assertTrue(json_manager.comprobar_json(len(json_manager)),"La transferencia no válida ha modificado el JSON")






    @freeze_time(freeze_date)
    def test_invalid_TC15(self):

        my_manager = AccountManager()
        json_manager = JsonManager("RF1/transfer_requests.json")
        from_iban_to_test = "ES9121000418450200051332"
        to_iban_to_test = "ES123456789123456789112"
        concept_to_test = "text valid"
        amount_to_test = 10.00
        date_to_test = "01/01/2025"
        type_to_test = "ORDINARY"
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(cm.exception.message, "Excepcion: Los números de cuenta (to) recibidos no son válidos.")
            self.assertTrue(json_manager.comprobar_json(len(json_manager)),"La transferencia no válida ha modificado el JSON")





    @freeze_time(freeze_date)
    def test_invalid_TC16(self):

        my_manager = AccountManager()
        json_manager = JsonManager("RF1/transfer_requests.json")
        from_iban_to_test = "ES9121000418450200051332"
        to_iban_to_test = "ES34004915009500123456791"
        concept_to_test = "text valid"
        amount_to_test = 10.00
        date_to_test = "01/01/2025"
        type_to_test = "ORDINARY"
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(cm.exception.message, "Excepcion: Los números de cuenta (to) recibidos no son válidos.")
            self.assertTrue(json_manager.comprobar_json(len(json_manager)),"La transferencia no válida ha modificado el JSON")






    @freeze_time(freeze_date)
    def test_invalid_TC17(self):

        my_manager = AccountManager()
        json_manager = JsonManager("RF1/transfer_requests.json")
        from_iban_to_test = "ES9121000418450200051332"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "1111111111"
        amount_to_test = 10.00
        date_to_test = "01/01/2025"
        type_to_test = "ORDINARY"
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(cm.exception.message, "Excepción: El concepto no tiene un valor válido.")
            self.assertTrue(json_manager.comprobar_json(len(json_manager)),"La transferencia no válida ha modificado el JSON")





    @freeze_time(freeze_date)
    def test_invalid_TC18(self):

        my_manager = AccountManager()
        json_manager = JsonManager("RF1/transfer_requests.json")
        from_iban_to_test = "ES9121000418450200051332"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "Pay Final"
        amount_to_test = 10.00
        date_to_test = "01/01/2025"
        type_to_test = "ORDINARY"
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(cm.exception.message, "Excepción: El concepto no tiene un valor válido.")
            self.assertTrue(json_manager.comprobar_json(len(json_manager)),"La transferencia no válida ha modificado el JSON")






    @freeze_time(freeze_date)
    def test_invalid_TC19(self):

        my_manager = AccountManager()
        json_manager = JsonManager("RF1/transfer_requests.json")
        from_iban_to_test = "ES9121000418450200051332"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "transferencia para javier perez"
        amount_to_test = 10.00
        date_to_test = "01/01/2025"
        type_to_test = "ORDINARY"
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(cm.exception.message, "Excepción: El concepto no tiene un valor válido.")
            self.assertTrue(json_manager.comprobar_json(len(json_manager)),"La transferencia no válida ha modificado el JSON")





    @freeze_time(freeze_date)
    def test_invalid_TC20(self):

        my_manager = AccountManager()
        json_manager = JsonManager("RF1/transfer_requests.json")
        from_iban_to_test = "ES9121000418450200051332"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "pagoparapablo"
        amount_to_test = 10.00
        date_to_test = "01/01/2025"
        type_to_test = "ORDINARY"
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(cm.exception.message, "Excepción: El concepto no tiene un valor válido.")
            self.assertTrue(json_manager.comprobar_json(len(json_manager)),"La transferencia no válida ha modificado el JSON")



    @freeze_time(freeze_date)
    def test_invalid_TC21(self):

        my_manager = AccountManager()
        json_manager = JsonManager("RF1/transfer_requests.json")
        from_iban_to_test = "ES9121000418450200051332"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "Pago para &%pablo"
        amount_to_test = 10.00
        date_to_test = "01/01/2025"
        type_to_test = "ORDINARY"
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(cm.exception.message, "Excepción: El concepto no tiene un valor válido.")
            self.assertTrue(json_manager.comprobar_json(len(json_manager)),"La transferencia no válida ha modificado el JSON")



    @freeze_time(freeze_date)
    def test_invalid_TC22(self):

        my_manager = AccountManager()
        json_manager = JsonManager("RF1/transfer_requests.json")
        from_iban_to_test = "ES9121000418450200051332"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "text valid"
        amount_to_test = 10.00
        date_to_test = "01/01/2025"
        type_to_test = "123"
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(cm.exception.message, "Excepción: El tipo de transferencia no es válido.")
            self.assertTrue(json_manager.comprobar_json(len(json_manager)),"La transferencia no válida ha modificado el JSON")



    @freeze_time(freeze_date)
    def test_invalid_TC23(self):

        my_manager = AccountManager()
        json_manager = JsonManager("RF1/transfer_requests.json")
        from_iban_to_test = "ES9121000418450200051332"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "text valid"
        amount_to_test = 10.00
        date_to_test = "01/01/2025"
        type_to_test = "OTHER"
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(cm.exception.message, "Excepción: El tipo de transferencia no es válido.")
            self.assertTrue(json_manager.comprobar_json(len(json_manager)),"La transferencia no válida ha modificado el JSON")



    @freeze_time(freeze_date)
    def test_invalid_TC24(self):

        my_manager = AccountManager()
        json_manager = JsonManager("RF1/transfer_requests.json")
        from_iban_to_test = "ES9121000418450200051332"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "text valid"
        amount_to_test = 10.00
        date_to_test = "123"
        type_to_test = "ORDINARY"
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(cm.exception.message, "Excepción: La fecha de la transferencia no es válida.")
            self.assertTrue(json_manager.comprobar_json(len(json_manager)),"La transferencia no válida ha modificado el JSON")




    @freeze_time(freeze_date)
    def test_invalid_TC25(self):

        my_manager = AccountManager()
        json_manager = JsonManager("RF1/transfer_requests.json")
        from_iban_to_test = "ES9121000418450200051332"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "text valid"
        amount_to_test = 10.00
        date_to_test = "11-12-2027"
        type_to_test = "ORDINARY"
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(cm.exception.message, "Excepción: La fecha de la transferencia no es válida.")
            self.assertTrue(json_manager.comprobar_json(len(json_manager)),"La transferencia no válida ha modificado el JSON")




    @freeze_time(freeze_date)
    def test_invalid_TC26(self):

        my_manager = AccountManager()
        json_manager = JsonManager("RF1/transfer_requests.json")
        from_iban_to_test = "ES9121000418450200051332"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "text valid"
        amount_to_test = 10.00
        date_to_test = "00/02/2026"
        type_to_test = "ORDINARY"
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(cm.exception.message, "Excepción: La fecha de la transferencia no es válida.")
            self.assertTrue(json_manager.comprobar_json(len(json_manager)),"La transferencia no válida ha modificado el JSON")




    @freeze_time(freeze_date)
    def test_invalid_TC27(self):

        my_manager = AccountManager()
        json_manager = JsonManager("RF1/transfer_requests.json")
        from_iban_to_test = "ES9121000418450200051332"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "text valid"
        amount_to_test = 10.00
        date_to_test = "32/02/2026"
        type_to_test = "ORDINARY"
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(cm.exception.message, "Excepción: La fecha de la transferencia no es válida.")
            self.assertTrue(json_manager.comprobar_json(len(json_manager)),"La transferencia no válida ha modificado el JSON")




    @freeze_time(freeze_date)
    def test_invalid_TC28(self):

        my_manager = AccountManager()
        json_manager = JsonManager("RF1/transfer_requests.json")
        from_iban_to_test = "ES9121000418450200051332"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "text valid"
        amount_to_test = 10.00
        date_to_test = "02/00/2026"
        type_to_test = "ORDINARY"
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(cm.exception.message, "Excepción: La fecha de la transferencia no es válida.")
            self.assertTrue(json_manager.comprobar_json(len(json_manager)),"La transferencia no válida ha modificado el JSON")



    @freeze_time(freeze_date)
    def test_invalid_TC29(self):

        my_manager = AccountManager()
        json_manager = JsonManager("RF1/transfer_requests.json")
        from_iban_to_test = "ES9121000418450200051332"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "text valid"
        amount_to_test = 10.00
        date_to_test = "02/13/2026"
        type_to_test = "ORDINARY"
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(cm.exception.message, "Excepción: La fecha de la transferencia no es válida.")
            self.assertTrue(json_manager.comprobar_json(len(json_manager)),"La transferencia no válida ha modificado el JSON")



    @freeze_time(freeze_date)
    def test_invalid_TC30(self):

        my_manager = AccountManager()
        json_manager = JsonManager("RF1/transfer_requests.json")
        from_iban_to_test = "ES9121000418450200051332"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "text valid"
        amount_to_test = 10.00
        date_to_test = "02/02/2024"
        type_to_test = "ORDINARY"
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(cm.exception.message, "Excepción: La fecha de la transferencia no es válida.")
            self.assertTrue(json_manager.comprobar_json(len(json_manager)),"La transferencia no válida ha modificado el JSON")




    @freeze_time(freeze_date)
    def test_invalid_TC31(self):

        my_manager = AccountManager()
        json_manager = JsonManager("RF1/transfer_requests.json")
        from_iban_to_test = "ES9121000418450200051332"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "text valid"
        amount_to_test = 10.00
        date_to_test = "02/02/2051"
        type_to_test = "ORDINARY"
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(cm.exception.message, "Excepción: La fecha de la transferencia no es válida.")
            self.assertTrue(json_manager.comprobar_json(len(json_manager)),"La transferencia no válida ha modificado el JSON")



    @freeze_time(freeze_date)
    def test_invalid_TC32(self):

        my_manager = AccountManager()
        json_manager = JsonManager("RF1/transfer_requests.json")
        from_iban_to_test = "ES9121000418450200051332"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "text valid"
        amount_to_test = "num"
        date_to_test = "01/01/2025"
        type_to_test = "ORDINARY"
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(cm.exception.message, "Excepción: La cantidad no es válida.")
            self.assertTrue(json_manager.comprobar_json(len(json_manager)),"La transferencia no válida ha modificado el JSON")



    @freeze_time(freeze_date)
    def test_invalid_TC33(self):

        my_manager = AccountManager()
        json_manager = JsonManager("RF1/transfer_requests.json")
        from_iban_to_test = "ES9121000418450200051332"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "text valid"
        amount_to_test = 9,99
        date_to_test = "01/01/2025"
        type_to_test = "ORDINARY"
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(cm.exception.message, "Excepción: La cantidad no es válida.")
            self.assertTrue(json_manager.comprobar_json(len(json_manager)),"La transferencia no válida ha modificado el JSON")



    @freeze_time(freeze_date)
    def test_invalid_TC34(self):

        my_manager = AccountManager()
        json_manager = JsonManager("RF1/transfer_requests.json")
        from_iban_to_test = "ES9121000418450200051332"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "text valid"
        amount_to_test = 10000.01
        date_to_test = "01/01/2025"
        type_to_test = "ORDINARY"
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(cm.exception.message, "Excepción: La cantidad no es válida.")
            self.assertTrue(json_manager.comprobar_json(len(json_manager)),"La transferencia no válida ha modificado el JSON")




    @freeze_time(freeze_date)
    def test_invalid_TC35(self):

        my_manager = AccountManager()
        json_manager = JsonManager("RF1/transfer_requests.json")
        from_iban_to_test = "ES9121000418450200051332"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "text valid"
        amount_to_test = 123.123
        date_to_test = "01/01/2025"
        type_to_test = "ORDINARY"
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(cm.exception.message, "Excepción: La cantidad no es válida.")
            self.assertTrue(json_manager.comprobar_json(len(json_manager)),"La transferencia no válida ha modificado el JSON")



    @freeze_time(freeze_date)
    def test_valid_TC36(self):
        my_manager = AccountManager()
        json_manager = JsonManager("RF1/transfer_requests.json")
        from_iban_to_test = "ES9121000418450200051332"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "text valid"
        amount_to_test = 10.00
        date_to_test = "01/01/2025"
        type_to_test = "ORDINARY"
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban=from_iban_to_test,
                to_iban=to_iban_to_test,
                concept=concept_to_test,
                amount=amount_to_test,
                date=date_to_test,
                type=type_to_test
            )
            self.assertEqual(cm.exception.message, "Error, la transferencia ya existe")
            self.assertTrue(json_manager.comprobar_json(len(json_manager)),"La transferencia no válida ha modificado el JSON")






if __name__ == '__main__':
    unittest.main()


