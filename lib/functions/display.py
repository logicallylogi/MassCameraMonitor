from requests import get
from requests.exceptions import ConnectionError
from numpy import frombuffer, uint8
from cv2 import imdecode, imshow, waitKey, IMREAD_COLOR
from time import sleep
from logging import getLogger

log = getLogger("__main__")

def start(url = "localhost"):
    while True:
        try:
            if url == "ai":
                port = 5000
            else:
                port = 5555
            response = get(f"http://{url}:{port}")
            frame = imdecode(frombuffer(response.content,dtype=uint8), IMREAD_COLOR)
            imshow("Network Camera", frame)
            stopkey = waitKey(1)
            if stopkey == ord('q'):
                break
        except ConnectionError:
            log.warning("An error was made connecting to the camera. Waiting 5 seconds.")
            log.debug("Attempted and failed connection to " + url)
            sleep(5)
            log.info("Trying again... NOW")
            pass