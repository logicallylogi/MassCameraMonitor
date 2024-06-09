from lib.db import quick_connect
from pathlib import Path

def start(req_id:str, config:Path = "config.ini"):
    db = quick_connect(config)
    result = db.get_person(record_id=req_id)
    print(req_id)
    print("=========================")
    for key, value in result.items():
        print(f'{key}: {value}')