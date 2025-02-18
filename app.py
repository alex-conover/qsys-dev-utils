import threading
import time

from cfg import CORE_IP_ADDRESS, QRC_PASSWORD, QRC_USERNAME, control_scripts
from lib.log import logger
from lib.qrc import Qrc
from live_reload import start_watching
from src.api import authenticate, connect, send


def read_file(path: str) -> str | None:
    with open(path, "r") as file:
        return file.read()


def process_file(filepath: str):
    logger.info(f"Processing file: {filepath}")
    qrc = Qrc()
    targets = control_scripts()

    if QRC_USERNAME == "" or QRC_USERNAME is None:
        logger.error("QRC_USERNAME is not set")
        return
    if QRC_PASSWORD == "" or QRC_PASSWORD is None:
        logger.error("QRC_PASSWORD is not set")
        return
    if CORE_IP_ADDRESS == "" or CORE_IP_ADDRESS is None:
        logger.error("QRC_IP_ADDRESS is not set")
        return

    s = connect(qrc, CORE_IP_ADDRESS)
    r = authenticate(s, qrc, QRC_USERNAME, QRC_PASSWORD)
    if not r:
        logger.warning("QRC Authentication failed")
        return
    id = 0
    for target in targets:
        id += 1
        if target["filepath"] == filepath:
            value = read_file(target["filepath"])
            if value is None:
                logger.warning(f"Failed to read file {target['filepath']}")
                continue
            controls = [{"Name": target["control"], "Value": value}]
            query = qrc.set_component(id, target["component"], controls)
            r = send(s, qrc, query)
            logger.info(
                f"Component: {target['component']}, Control: {target['control']}, Success: {r}"
            )
    s.close()


def live_reload(filepath: str):
    logger.debug(f"Calling main function for file: {filepath}")
    process_file(filepath)


if __name__ == "__main__":
    reload_directory = "./lua"
    logger.info(f"Starting watcher for directory: {reload_directory}")
    watcher_thread = threading.Thread(
        target=start_watching, args=(reload_directory, live_reload)
    )
    watcher_thread.daemon = True
    watcher_thread.start()
    # Initial run for all files
    for target in control_scripts():
        process_file(target["filepath"])

    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping watcher...")
