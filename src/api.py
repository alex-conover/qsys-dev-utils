import json
import socket

from lib.log import logger
from lib.qrc import Qrc


def _decode_response(response: str) -> dict | None:
    # Remove the null character if present
    response = response.replace("\0", "")
    try:
        # Parse the JSON string into a Python dictionary
        data = json.loads(response)
        return data
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {e}")


def connect(qrc: Qrc, core: str) -> socket.socket:
    """
    Opens a QRC Connection to the Q-SYS Core.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect((core, 1710))
    s.settimeout(None)
    response = s.recv(1024).decode()
    # Decode the response
    data = _decode_response(response)
    if data:
        logger.debug(f"Connection response: {data}")
    return s


def authenticate(
    socket: socket.socket, qrc: Qrc, username: str, password: str, id: int = 123456789
) -> bool:
    """
    Authenticates a user on a Q-SYS Core via the QRC API.
    """
    logon = qrc.logon(id, username, password)
    socket.send(str.encode(logon + "\0"))
    response = socket.recv(1024).decode()
    data = _decode_response(response)
    if data:
        if "result" in dict.keys(data):
            if data["result"]:
                logger.debug(f"Authentication Response: {data}")
                return True
        if "error" in dict.keys(data):
            logger.warning(f"Error authenticating: {data['error']}")
            return False
    return False


def send(socket: socket.socket, qrc: Qrc, query: str) -> bool:
    """
    Sends a query to a Q-SYS Core via the QRC API.
    """
    socket.send(str.encode(query + "\0"))
    response = socket.recv(1024).decode()
    data = _decode_response(response)
    if data:
        if "result" in dict.keys(data):
            if data["result"]:
                logger.debug(f"Query Response: {data}")
                return True
        if "error" in dict.keys(data):
            logger.warning(f"Error sending query: {data['error']}")
            return False
    return False
