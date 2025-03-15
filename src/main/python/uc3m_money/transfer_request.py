"""MODULE: transfer_request. Contains the transfer request class"""
import hashlib
import json
from datetime import datetime, timezone

class TransferRequest:
    """Class representing a transfer request"""
    def __init__(self,
                 from_iban: str,
                 transfer_type: str,
                 to_iban:str,
                 transfer_concept:str,
                 transfer_date:str,
                 transfer_amount:float):
        self.__from_iban = from_iban
        self.__to_iban = to_iban
        self.__transfer_type = transfer_type
        self.__concept = transfer_concept
        self.__transfer_date = transfer_date
        self.__transfer_amount = transfer_amount
        justnow = datetime.now(timezone.utc)
        self.__time_stamp = datetime.timestamp(justnow)

    def __str__(self):
        return "Transfer:" + json.dumps(self.__dict__)

    def to_json(self):
        """returns the object information in json format"""
        return {
            "from_iban": self.__from_iban,
            "to_iban": self.__to_iban,
            "transfer_type": self.__transfer_type,
            "transfer_amount": self.__transfer_amount,
            "transfer_concept": self.__concept,
            "transfer_date": self.__transfer_date,
            "time_stamp": self.__time_stamp,
            "transfer_code": self.transfer_code
        }

    def save_transfer(self):
        """Save the current transfer to a JSON file only if it's valid"""
        try:
            # Validate the transfer before saving
            if self.validate_transfer():
                # Use JsonManager to read the existing data
                json_manager = JsonManager("transfers.json")  # Specify the file path for transfers
                transfers = json_manager.read_json()  # Get the current data from the JSON file

                # Append the current transfer to the list of transfers
                if "transfers" not in transfers:
                    transfers["transfers"] = []

                transfers["transfers"].append(self.to_json())

                # Write the updated transfers data back to the file
                json_manager.write_json(transfers)
                print("Transfer saved successfully!")
            else:
                print("Transfer validation failed.")
        except ValueError as ve:
            print(f"Error: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    @property
    def from_iban(self):
        """Sender's iban"""
        return self.__from_iban

    @from_iban.setter
    def from_iban(self, value):
        self.__from_iban = value

    @property
    def to_iban(self):
        """receiver's iban"""
        return self.__to_iban

    @to_iban.setter
    def to_iban(self, value):
        self.__to_iban = value

    @property
    def transfer_type(self):
        """Property representing the type of transfer: REGULAR, INMEDIATE or URGENT """
        return self.__transfer_type
    @transfer_type.setter
    def transfer_type(self, value):
        self.__transfer_type = value

    @property
    def transfer_amount(self):
        """Property respresenting the transfer amount"""
        return self.__transfer_amount
    @transfer_amount.setter
    def transfer_amount(self, value):
        self.__transfer_amount = value

    @property
    def transfer_concept(self):
        """Property representing the transfer concept"""
        return self.__transfer_concept
    @transfer_concept.setter
    def transfer_concept(self, value):
        self.__transfer_concept = value

    @property
    def transfer_date( self ):
        """Property representing the transfer's date"""
        return self.__transfer_date
    @transfer_date.setter
    def transfer_date( self, value ):
        self.__transfer_date = value

    @property
    def time_stamp(self):
        """Read-only property that returns the timestamp of the request"""
        return self.__time_stamp

    @property
    def transfer_code(self):
        """Returns the md5 signature (transfer code)"""
        return hashlib.md5(str(self).encode()).hexdigest()
