"""class for testing the register_order method"""
import unittest
import sys
import os
from freezegun import freeze_time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../main/python")))
from uc3m_money.transfer_request import TransferRequest
from uc3m_money.account_manager import AccountManager
from uc3m_money.account_management_exception import AccountManagementException

freeze_date = "2024-03-22 10:00:00"

class MyTestCase(unittest.TestCase):
    """class for testing the register_order method"""
    """Tests for the AccountManager's transfer request"""

    @freeze_time(freeze_date)
    def test_valid_tc1(self):
        """Valid transfer request"""
        my_manager = AccountManager()
        from_iban_to_test = "ES4500817294770123456789"
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
            self.assertEqual(result, "2bbb9b4a9d23dcbe14c97b7fdb7f43f7")


    @freeze_time(freeze_date)
    def test_valid_TC2(self):
       
        my_manager = AccountManager()
        from_iban_to_test = "ES4500817294770123456789"
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
            self.assertEqual(result, "1d80b7003a9cc4ecf98ceffbf989498e")

    """
    def test_valid_TC3(self):
     
        my_manager = AccountManager()
        from_iban_to_test = "ES4500817294770123456789"
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
            self.assertEqual(result, "7e72a7829fdc0242dc7e03bb23b2eef9")
    
    def test_valid_TC4(self):
       
        my_manager = AccountManager()
        from_iban_to_test = "ES4500817294770123456789"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "transfere compra semana pasada"
        amount_to_test = 400.3
        date_to_test = "31/12/2050"
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
            self.assertEqual(result, "7e72a7829fdc0242dc7e03bb23b2eef9")

    def test_valid_TC5(self):
       
        my_manager = AccountManager()
        from_iban_to_test = "123"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "transfer for rent"
        amount_to_test = 200.45
        date_to_test = "22/03/2025"
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
            self.assertEqual(result, "7e72a7829fdc0242dc7e03bb23b2eef9")

    def test_valid_TC6(self):
        
        my_manager = AccountManager()
        from_iban_to_test = "ES3400491500950012345679"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "transfer for rent"
        amount_to_test = 200.45
        date_to_test = "22/03/2025"
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
            self.assertEqual(result, "7e72a7829fdc0242dc7e03bb23b2eef9")

    def test_valid_TC7(self):
        
        my_manager = AccountManager()
        from_iban_to_test = "S34004915009500123456780"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "transfer for rent"
        amount_to_test = 200.45
        date_to_test = "22/03/2025"
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
            self.assertEqual(result, "7e72a7829fdc0242dc7e03bb23b2eef9")

    def test_valid_TC8(self):
       
        my_manager = AccountManager()
        from_iban_to_test = "ES23456789UYTR3456789654"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "transfer for rent"
        amount_to_test = 200.45
        date_to_test = "22/03/2025"
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
            self.assertEqual(result, "7e72a7829fdc0242dc7e03bb23b2eef9")

    def test_valid_TC9(self):
        
        my_manager = AccountManager()
        from_iban_to_test = "ES123456789123456789112"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "transfer for rent"
        amount_to_test = 200.45
        date_to_test = "22/03/2025"
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
            self.assertEqual(result, "7e72a7829fdc0242dc7e03bb23b2eef9")

    def test_valid_TC10(self):
        
        my_manager = AccountManager()
        from_iban_to_test = "ES34004915009500123456791"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "transfer for rent"
        amount_to_test = 200.45
        date_to_test = "22/03/2025"
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
            self.assertEqual(result, "7e72a7829fdc0242dc7e03bb23b2eef9")

    def test_valid_TC11(self):
        
        my_manager = AccountManager()
        from_iban_to_test = "ES4500817294770123456789"
        to_iban_to_test = "123"
        concept_to_test = "transfer for rent"
        amount_to_test = 200.45
        date_to_test = "22/03/2025"
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
            self.assertEqual(result, "7e72a7829fdc0242dc7e03bb23b2eef9")

    def test_valid_TC12(self):
      
        my_manager = AccountManager()
        from_iban_to_test = "ES4500817294770123456789"
        to_iban_to_test = "ES3400491500950012345679"
        concept_to_test = "transfer for rent"
        amount_to_test = 200.45
        date_to_test = "22/03/2025"
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
            self.assertEqual(result, "7e72a7829fdc0242dc7e03bb23b2eef9")

    def test_valid_TC13(self):
        
        my_manager = AccountManager()
        from_iban_to_test = "ES4500817294770123456789"
        to_iban_to_test = "S34004915009500123456780"
        concept_to_test = "transfer for rent"
        amount_to_test = 200.45
        date_to_test = "22/03/2025"
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
            self.assertEqual(result, "7e72a7829fdc0242dc7e03bb23b2eef9")

    def test_valid_TC14(self):
      
        my_manager = AccountManager()
        from_iban_to_test = "ES4500817294770123456789"
        to_iban_to_test = "ES23456789UYTR3456789654"
        concept_to_test = "transfer for rent"
        amount_to_test = 200.45
        date_to_test = "22/03/2025"
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
            self.assertEqual(result, "7e72a7829fdc0242dc7e03bb23b2eef9")

    def test_valid_TC15(self):
        
        my_manager = AccountManager()
        from_iban_to_test = "ES4500817294770123456789"
        to_iban_to_test = "ES123456789123456789112"
        concept_to_test = "transfer for rent"
        amount_to_test = 200.45
        date_to_test = "22/03/2025"
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
            self.assertEqual(result, "7e72a7829fdc0242dc7e03bb23b2eef9")

    def test_valid_TC16(self):
       
        my_manager = AccountManager()
        from_iban_to_test = "ES4500817294770123456789"
        to_iban_to_test = "ES34004915009500123456791"
        concept_to_test = "transfer for rent"
        amount_to_test = 200.45
        date_to_test = "22/03/2025"
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
            self.assertEqual(result, "7e72a7829fdc0242dc7e03bb23b2eef9")

    def test_valid_TC17(self):
        
        my_manager = AccountManager()
        from_iban_to_test = "ES4500817294770123456789"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "1111111111"
        amount_to_test = 200.45
        date_to_test = "22/03/2025"
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
            self.assertEqual(result, "7e72a7829fdc0242dc7e03bb23b2eef9")

    def test_valid_TC18(self):
      
        my_manager = AccountManager()
        from_iban_to_test = "ES4500817294770123456789"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "Pay Final"
        amount_to_test = 200.45
        date_to_test = "22/03/2025"
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
            self.assertEqual(result, "7e72a7829fdc0242dc7e03bb23b2eef9")

    def test_valid_TC19(self):
       
        my_manager = AccountManager()
        from_iban_to_test = "ES4500817294770123456789"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "transferencia para javier perez"
        amount_to_test = 200.45
        date_to_test = "22/03/2025"
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
            self.assertEqual(result, "7e72a7829fdc0242dc7e03bb23b2eef9")

    def test_valid_TC20(self):
       
        my_manager = AccountManager()
        from_iban_to_test = "ES4500817294770123456789"
        to_iban_to_test = "ES4500817294770123456789"
        concept_to_test = "pagoparapablo"
        amount_to_test = 200.45
        date_to_test = "22/03/2025"
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
            self.assertEqual(result, "7e72a7829fdc0242dc7e03bb23b2eef9")
"""

if __name__ == '__main__':
    unittest.main()


