import os
import json
from pathlib import Path
from uc3m_money.exceptions import AccountManagmentException

class JsonManager:

    def __init__(self, path, data=None):
        self.path = os.path.join(Path(__file__).resolve().parents[2], "JsonFiles/") + path
        if data is not None:
            self.write_json(data)
        else:
            self.read_json()

    def read_json(self):
        try:
            with open(self.path, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}
        except json.JSONDecodeError as ex:
            raise AccountManagmentException ("ERROR: FORMATO JSON INCORRECTO.") from ex
        return data
    

    def write_json(self, data):
        try:
            with open(self.path, "w", encoding="utf-8", newline="") as file:
                json.dump(data, file, indent=2)
        except FileNotFoundError as exception:
            raise AccountManagmentException ("ERROR: ARCHIVO JSON DAÑADO O RUTA NO ENCONTRADA.") from exception
        except json.JSONDecodeError as exception:
            raise AccountManagmentException ("ERROR: FORMATO JSON INCORRECTO.") from exception
        except Exception as exception:
            raise AccountManagmentException ("ERROR: NO SE HA PODIDO ESCRIBIR EL JSON.") from exception
        return data
