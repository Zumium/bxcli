import os


def port():
    """port reads port settings from environment"""
    server_port = None
    try:
        server_port = int(os.environ['BXCLI_PORT'])
    except:
        server_port = 6077
    return server_port
