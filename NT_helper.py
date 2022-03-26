import socket
from networktables import NetworkTables

def is_networktable(ip, SEARCH_TIMEOUT=1, NT_PORT=1735):
    """
        Checks if a networktable server is running on the given ip.
        :param str ip: The ip to check.
        :return True if a networktable server is running on the given ip, false otherwise.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(SEARCH_TIMEOUT)
    try:
        sock.connect((ip, NT_PORT))
        sock.shutdown(socket.SHUT_RDWR)
        return True
    except:
        return False
    finally:
        sock.close()


def nt_init(*args):
    """
        Blocking function that searches given IP addresses until a networktable server has been found.
    """
    while True:
        for ip in args:
            if isinstance(ip, str) and is_networktable(ip):
                NetworkTables.initialize(ip)
                print("connected!")
                return ip