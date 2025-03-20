import os
from pathlib import Path
import json

from .account_management_exception import AccountManagementException


class JsonManager:
    def __init__(self, path, data=None):
        self.path = path
        self.JSON_FILES_PATH = os.path.join(Path(__file__).resolve().parents[2], "JsonFiles/")
        if data is not None:
            self.write_json(data)
        else:
            self.read_json()

    def read_json(self):
        try:
            with open(self.JSON_FILES_PATH+self.path, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        except json.JSONDecodeError as exception:
            raise AccountManagementException ("ERROR: FORMATO JSON INCORRECTO.") from exception
        return data


    def write_json(self, data):
        try:
            with open(self.JSON_FILES_PATH + self.path, "w", encoding="utf-8", newline="") as file:
                json.dump(data, file, indent=2)
        except FileNotFoundError as exception:
            raise AccountManagementException ("ERROR: ARCHIVO JSON DAÑADO O RUTA NO ENCONTRADA.") from exception
        except json.JSONDecodeError as exception:
            raise AccountManagementException ("ERROR: FORMATO JSON INCORRECTO.") from exception
        except Exception as exception:
            raise AccountManagementException ("ERROR: NO SE HA PODIDO ESCRIBIR EL JSON.") from exception
        return data
