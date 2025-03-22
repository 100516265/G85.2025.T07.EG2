"""Contains the class OrderShipping"""
from datetime import datetime, timezone
import hashlib
from .json_manager import JsonManager
from .account_management_exception import AccountManagementException


class AccountDeposit:
    """Class representing the information required for shipping of an order"""

    def __init__(self,
                 to_iban: str,
                 deposit_amount):
        self.__alg = "SHA-256"
        self.__type = "DEPOSIT"
        self.__to_iban = to_iban
        self.__deposit_amount = deposit_amount
        justnow = datetime.now(timezone.utc)
        self.__deposit_date = datetime.timestamp(justnow)

    def to_json(self):
        """returns the object data in json format"""
        return {"alg": self.__alg,
                "type": self.__type,
                "to_iban": self.__to_iban,
                "deposit_amount": self.__deposit_amount,
                "deposit_date": self.__deposit_date,
                "deposit_signature": self.deposit_signature}

    def __signature_string(self):
        """Composes the string to be used for generating the key for the date"""
        return "{alg:" + str(self.__alg) +",typ:" + str(self.__type) +",iban:" + \
               str(self.__to_iban) + ",amount:" + str(self.__deposit_amount) + \
               ",deposit_date:" + str(self.__deposit_date) + "}"

    @property
    def to_iban(self):
        """Property that represents the product_id of the patient"""
        return self.__to_iban

    @to_iban.setter
    def to_iban(self, value):
        self.__to_iban = value

    @property
    def deposit_amount(self):
        """Property that represents the order_id"""
        return self.__deposit_amount
    @deposit_amount.setter
    def deposit_amount(self, value):
        self.__deposit_amount = value

    @property
    def deposit_date(self):
        """Property that represents the phone number of the client"""
        return self.__deposit_date
    @deposit_date.setter
    def deposit_date( self, value ):
        self.__deposit_date = value


    @property
    def deposit_signature( self ):
        """Returns the sha256 signature of the date"""
        return hashlib.sha256(self.__signature_string().encode()).hexdigest()

    @staticmethod
    def deposit_request(input_file: str, storage_file: str) -> str:
        """Processes a deposit request, reading from input and saving to storage"""
        # Leyendo los archivos de entrada y salida
        data = JsonManager(input_file).read_json()
        json_salida = JsonManager(storage_file)

        # Validar la estructura del JSON de entrada
        if 'IBAN' not in data or 'AMOUNT' not in data:
            raise AccountManagementException("Excepción: El JSON no tiene la estructura esperada.")

        to_iban = data["IBAN"]
        deposit_amount = data["AMOUNT"]

        # Crear una instancia de AccountDeposit
        try:
            deposit = AccountDeposit(to_iban=to_iban, deposit_amount=deposit_amount)
            deposit_signature = deposit.deposit_signature
        except Exception as e:
            raise AccountManagementException(f"Exception: Error al obtener el deposit_signature: {str(e)}")

        # Convertir la transacción a formato JSON
        transaction_data = deposit.to_json()

        # Guardar la transacción
        transactions = json_salida.read_json()
        transactions.append(transaction_data)
        json_salida.write_json(transactions)

        return deposit_signature