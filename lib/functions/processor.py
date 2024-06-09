import requests
import numpy as np
import cv2 as cv
from logging import getLogger
from pathlib import Path
from lib.db import quick_connect
from lib.faces import get_all
from asyncio import sleep, create_task, gather, run
from configparser import RawConfigParser, NoSectionError

db = []
knowns = []
log = getLogger("__main__")

async def get_all_knowns():
    global knowns
    while True:
        log.debug(db)
        knowns = db[0].get_knowns()
        await sleep(10)

async def run_inference(url:str):
    global knowns
    while True:
        response = requests.get("http://" + url + ":5555")
        frame = cv.imdecode(np.frombuffer(response.content), -1)
        faces = get_all(frame, db[0])
        i = 0
        
        for face in faces:
            matches = face.compare(knowns)
            if len(matches) > 0:
                faces[i].id = max(matches)
                frame = faces[i].identify(frame)
            else:
                log.debug(f"Insufficent matches found.")
            i =+ 1

async def process_from_feed(urls:list):
    tasks = [create_task(get_all_knowns())]
    for url in urls:
        tasks.extend(create_task(run_inference(url)))
        
    await gather(*tasks)
    
def start(config_path: Path = "config.ini"):
    db.append(quick_connect(config_path))
    urls = []
    
    config = RawConfigParser()
    config.read(config_path)
    ips = {"localhost":"yes"}
    try:
        ips = config.items("feeds")
    except NoSectionError:
        pass
    
    log.debug(ips)
    for key, enabled in ips.items():
        if enabled == "yes":
            urls.append(key)
            
    run(process_from_feed(urls))