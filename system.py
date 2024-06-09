from argparse import ArgumentParser
from os import makedirs
from threading import Thread
import logging

parser = ArgumentParser(
    prog='system',
    description='More than just 14 eyes.',
    epilog="You're always being watched.")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logfile = logging.FileHandler("system.log")
console = logging.StreamHandler()

logfile.setLevel("DEBUG")
console.setLevel("WARN")

logfileFormat = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
consoleFormat = logging.Formatter("[%(levelname)s] %(message)s")

logfile.setFormatter(logfileFormat)
console.setFormatter(consoleFormat)

logger.addHandler(logfile)
logger.addHandler(console)

parser.add_argument("-v", "--verbose",
                    action="store_true",
                    help="dump all debug information to console")
parser.add_argument("-t", "--train",
                    action="store_true",
                    help="load the database with a folder of IDs")
parser.add_argument("-c", "--camera",
                    action="store_true",
                    help="turn this device into a wireless camera")
parser.add_argument("-p", "--process",
                    action="store_true",
                    help="start processing information")
parser.add_argument("-d", "--display",
                    nargs='?',
                    const="localhost",
                    help="display what a wireless camera can see")
parser.add_argument("-q", "--query",
                    help="query user based on id code")
parser.add_argument("-o", "--options",
                    default="config.ini",
                    help="specify a config file in ini format")

args = parser.parse_args()
tasks = []

if args.verbose:
    console.setLevel("DEBUG")
    logger.debug("The console will now display all debug information.")
    
if args.train:
    logger.debug("Training mode has been selected.")
    makedirs("training", exist_ok=True)
    import lib.functions.train as tra
    tasks.append(Thread(target=tra.start, args=(args.options,)))
    
if args.camera:
    logger.debug("Camera mode has been selected.")
    logger.info("The camera server should start shortly.")
    import lib.functions.camera as cam
    tasks.append(Thread(target=cam.start))
    
if args.process:
    logger.debug("Processing mode has been selected.")
    import lib.functions.processor as pro
    tasks.append(Thread(target=pro.start, args=(args.options,)))
    
if args.query:
    logger.debug("User has requested informatin on " + args.query)
    import lib.functions.query as que
    tasks.append(Thread(target=que.start, args=(args.options,)))
    
for task in tasks:
    task.start()
    
if args.display:
    logger.debug("Display mode has been selected.")
    logger.info("You should see what " + args.display + " can see.")
    logger.info("Press 'Q' to quit.")
    import lib.functions.display as dis
    dis.start(args.display)

for task in tasks:
    task.join()