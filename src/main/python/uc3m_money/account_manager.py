"""Module"""

from .account_management_exception import AccountManagementException
from .transfer_request import TransferRequest
from .json_manager import JsonManager
import hashlib
import _md5


class AccountManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    @staticmethod
    def validate_iban(iban: str) ->bool:
        """
        Validates whether a given IBAN is correctly formatted
        and has valid control digits
        :param iban: The IBAN to validate
        :return: True if the IBAN is valid
        """

        if(not isinstance(iban, str)
            or not iban.startswith("ES")
            or len(iban)!=24
            or not iban[2:].isdigit()):
            return False

        control_digits = int(iban[2:4])
        iban_number = int(iban[4:] + "142800") % 97
        calculated_control_digits = 98 - iban_number

        return control_digits == calculated_control_digits


    @staticmethod
    def validate_concept(concept: str) ->bool:
        return isinstance(concept, str) and (10<= len(concept) <= 30)



    @staticmethod
    def validate_type(type: str) ->bool:

        if not isinstance(type, str):
            return False
        if type == "ORDINARY" or "URGENT" or "INMEDIATE":
            return True

    @staticmethod
    def validate_date(date: str) -> bool:

        if not isinstance(date, str):
            return False

    @staticmethod
    def validate_amount(amount: str) -> bool:

        if (not isinstance(amount, float))\
            or not (10.00 <= amount <= 10000.00):
            return False


    def transfer_request(self, from_iban: str, to_iban: str,transfer_concept: str,
                        transfer_type: str, transfer_date: str, transfer_amount: float):

        if not self.validate_iban(from_iban):
            raise AccountManagementException("Excepción: Número de IBAN inválido. ")

        if not self.validate_iban(to_iban):
            raise AccountManagementException("Excepción: Número de IBAN inválido. ")

        if not self.validate_concept(transfer_concept):
            raise AccountManagementException("Excepción: concept inválido ")

        if not self.validate_type(transfer_type):
            raise AccountManagementException("Excepción: type inválido ")

        if not self.validate_date(transfer_date):
            raise AccountManagementException("Excepción: date inválido ")

        if not self.validate_amount(transfer_amount):
            raise AccountManagementException("Excepción: amount inválido ")


        tr = TransferRequest(from_iban, transfer_type, to_iban, transfer_concept, transfer_date, transfer_amount)

        JSON_FILE_NAME = "transfer_requests.json"

        json_manager = JsonManager(JSON_FILE_NAME)
        data_list = json_manager.read_json()

        for data in data_list:
            if (data['from_iban'] == tr.from_iban and
                data['to_iban'] == tr.to_iban and
                data['transfer_concept'] == tr.transfer_concept and
                data['transfer_type'] == tr.transfer_type and
                data['transfer_date'] == tr.transfer_date and
                data['transfer_amount'] == tr.transfer_amount):
                raise AccountManagementException("Error, la transferencia ya existe")

        data_list.append(tr.to_json())
        json_manager.write_json(data_list)

        return tr.transfer_code



