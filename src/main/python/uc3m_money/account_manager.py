import re
from datetime import datetime
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


        if(not isinstance(concept, str)
            or not (10<= len(concept) <= 30)):
            return False
        #dividimos el concepto en palabras
        palabras = concept.split()

        #comprueba que sean dos o mas cadenas
        if len(palabras) < 2:
            return False

        #comprobamos que cada palabra solo tenga caracteres [a-zA-Z]
        for palabra in palabras:
            for char in palabra:
                if not( 'a' <=char <= 'z' or 'A' <= char <= 'Z' ):
                    return False
        return True


    @staticmethod
    def validate_type(type: str) ->bool:

        if not isinstance(type, str):
            return False
        if type in ["ORDINARY", "URGENT", "INMEDIATE"]:
            return True
        return False

    @staticmethod
    def validate_date(date: str) -> bool:

        if not isinstance(date, str):
            return False

        try:
            fecha_valida = datetime.strptime(date, "%d/%m/%Y")
        except ValueError:
            return False

        hoy = datetime.today()
        if fecha_valida < hoy:
            return False
        if not (1 <= fecha_valida.day <=31) or not (1<= fecha_valida.month <=12) or not (2025 <= fecha_valida.year <= 2050):
            return False
        return True



    @staticmethod
    def validate_amount(amount: float) -> bool:

        if (not isinstance(amount, float)) or not (10.00 <= amount <= 10000.00):
            return False

        return len(str(amount).split(".")[1] ) <= 2

    def transfer_request(self, from_iban: str, to_iban: str, concept: str, amount: float, date: str, type: str) -> str:
        # Create a TransferRequest instance
        #VALIDACIONES
        if not self.validate_iban(from_iban):
            raise AccountManagementException("Excepción: Los números de cuenta (from) recibidos no son válidos.")

        if not self.validate_iban(to_iban):
            raise AccountManagementException("Excepcion: Los números de cuenta (to) recibidos no son válidos.")

        if not self.validate_concept(concept):
            raise AccountManagementException("Excepción: El concepto no tiene un valor válido.")

        if not self.validate_type(type):
            raise AccountManagementException("Excepción: El tipo de transferencia no es válido.")

        if not self.validate_date(date):
            raise AccountManagementException("Excepción: La fecha de la transferencia no es válida.")

        if not self.validate_amount(amount):
            raise AccountManagementException("Excepción: La cantidad no es válida.")

        # Crea una instancia de TransferRequest
        transfer = TransferRequest(
            from_iban=from_iban,
            transfer_type=type,
            to_iban=to_iban,
            transfer_concept=concept,
            transfer_date=date,
            transfer_amount=amount
        )

        # Leemos el json para ver si existe la transferencia
        json_manager = JsonManager("RF1/transfer_requests.json")
        datos_json = json_manager.read_json()
        for datos in datos_json:
            if (datos['transfer_code'] == transfer.transfer_code):
                raise AccountManagementException("Error, la transferencia ya existe")

        # Creando los datos a escribir en el archivo JSON
        dict_json = {
            'from_iban': transfer.from_iban,
            'to_iban': transfer.to_iban,
            'transfer_type': transfer.transfer_type,
            'transfer_concept': transfer.transfer_concept,
            'transfer_date': transfer.transfer_date,
            'transfer_amount': transfer.transfer_amount,
            'time_stamp': transfer.time_stamp,
            'transfer_code': transfer.transfer_code
        }

        # Adjuntamos a los datos leidos del archivo JSON
        datos_json.append(dict_json)
        json_manager.write_json(datos_json)

        # Devolvemos el hash MD5
        return transfer.transfer_code
