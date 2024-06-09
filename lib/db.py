import configparser

from pymongo import MongoClient
from pathlib import Path
from numpy import ndarray
from os import getenv
from configparser import RawConfigParser
from logging import getLogger

log = getLogger("__main__")

class Database:
    def __init__(self, host:str, port:int, certificate:Path, client_certificate:Path):
        _client = MongoClient(
            host=host,
            compressors="zstd",
            connect=True,
            port=port,
            #authMechanism="MONGODB-X509",
            #tls=True,
            #tlsCAFile=certificate,
            #tlsCertificateKeyFile=client_certificate
        )
        
        _db = _client['production']

        self.faces = _db["biometrics"]
        self.people = _db["people"]
        
    def get_person(self, record_id = None, face:ndarray = None):
        if record_id:
            return self.people.find_one({'_id':record_id})
        if face:
            biometrics = self.get_face(face=face)
            face_id = biometrics['_id']
            return self.people.find_one({'faces': face_id})
        
    def get_face(self, face:ndarray = None, record_id = None, delete_when_found = False):
        if delete_when_found:
            function = self.faces.find_one_and_delete
        else:
            function = self.faces.find_one
            
        if id:
            return function({'_id':record_id})
        if face:
            return function({'face':face.tobytes()})
        
    def insert_face(self, face_data:ndarray):
        if self.get_face(face=face_data):
            return None
        else:
            return self.faces.insert_one({'face':face_data.tobytes()})
        
    def get_knowns(self) -> [ndarray]:
        return self.faces.find({}, {'_id':True, 'face':True})
        
    def get_amount(self) -> int:
        return self.faces.estimated_document_count()
    
def quick_connect(config_path:Path = None):
    try:
        config = RawConfigParser()
        config.read(config_path)
        database = Database(
            config.get("db", "host"),
            config.get("db", "port"),
            config.get("db", "ssl_ca"),
            config.get("db", "client_ca")
        )
    except configparser.NoSectionError:
        database = Database(
            getenv('db_host', 'localhost'),
            getenv('db_port', 27017),
            Path(getenv('db_ssl_ca', 'ssl.crt')),
            Path(getenv('db_client_ca', 'client.crt'))
        )
    return database