#!/usr/bin/env python3

import sys
import socket
import selectors
import types
import yaml
import logging
from dns import message, query
from pyfiglet import Figlet
import binascii
import time

# General config
f = Figlet(font='slant')

# Load Config
with open("dnproxy.yml", "r") as configfile:
    cfg = yaml.load(configfile, Loader=yaml.FullLoader)

# create logger
logger = logging.getLogger('dnproxy')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - [%(levelname)s] - %(message)s ") # I am printing thread id here
ch.setFormatter(formatter)
logger.addHandler(ch)

# Init
logger.info(f.renderText('dnproxy'))

HOST = cfg['dnproxy']['host']
PORT = cfg['dnproxy']['port']
UPSTREAM_IP = cfg['upstream']['ip']
TLS_HOSTNAME = cfg['upstream']['hostname']

sel = selectors.DefaultSelector()

def receive_message(sock):
    (wire, host) = sock.recvfrom(1024)
    q = message.from_wire(wire)
    logger.info(f'UDP Socket - Query ID: {q.id}, Question:{q.question}')
    r = query.tls(q, UPSTREAM_IP, server_hostname=TLS_HOSTNAME)
    logger.info(f'UDP Socket - Query ID: {q.id}, Answer: {r.answer}')
    wire = r.to_wire()
    sock.sendto(wire, host)

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    logger.debug(f"TCP Socket - Accepted connection from {addr[0]}:{addr[1]}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.outb += recv_data
        else:
            logger.debug(f"TCP Socket - Closing connection to {data.addr[0]}:{data.addr[1]}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            q = message.from_wire(data.outb[2:])
            logger.info(f'TCP Socket - Question from {data.addr[0]}:{data.addr[1]}, Query ID: {q.id}, Question:{q.question}')
            r = query.tls(q, UPSTREAM_IP, server_hostname=TLS_HOSTNAME)
            logger.info(f'TCP Socket - Response to {data.addr[0]}:{data.addr[1]}, Query ID: {q.id}, Answer: {r.answer}')
            wire = r.to_wire()
            length = binascii.unhexlify("%04x" % len(wire))
            if r:
                sent = sock.send(length+wire)
                data.outb = data.outb[sent:]


if __name__=="__main__":

    # Sockets Creations
    
    tsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tsock.bind((HOST, PORT))
    tsock.listen()
    logger.info(f"TCP Socket - Listening on {HOST}:{PORT}")
    tsock.setblocking(False)
    sel.register(tsock, selectors.EVENT_READ, data=None)

    usock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    usock.bind((HOST, PORT))
    logger.info(f"UDP Socket - Listening on {HOST}:{PORT}")
    sel.register(usock, selectors.EVENT_READ, data=None)

    try:
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    if key.fileobj.type == socket.SOCK_STREAM:
                        accept_wrapper(key.fileobj)
                    elif key.fileobj.type == socket.SOCK_DGRAM:
                        receive_message(key.fileobj)
                else:
                    service_connection(key, mask)
    except KeyboardInterrupt:
        logger.info("Caught keyboard interrupt, exiting")
    finally:
        sel.close()
