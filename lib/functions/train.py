from pathlib import Path
from lib.faces import get_all
from lib.db import quick_connect
import cv2

def start(config:Path = "config.ini"):
    images = Path("training").glob("*.jpg")
    for image in images:
        img = cv2.imread(image, 0)
        db = quick_connect(config)
        get_all(img, db)
        