#!/usr/bin/env python3

import logging as l
import socket

from pyfiglet import Figlet

import dns.flags
import dns.message
import dns.rdataclass
import dns.rdatatype
import dns.name
import dns.query

from typing import cast

# General config
l.basicConfig(level=l.INFO)
f = Figlet(font='slant')

l.info(f.renderText('dnproxy'))

# General Parameters
HOST = '127.0.0.1'
PORT = 53
UPSTREAM_IP = '1.1.1.1'
TLS_HOSTNAME = 'cloudflare-dns.com'


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    l.info(f"Listening on {HOST}:{PORT}")

    while True:
        (wire, host) = s.recvfrom(1024)
        q = dns.message.from_wire(wire)
        l.info(f'Question {q.id}:{q.question}')
        
        try:
            r = dns.query.tls(q, UPSTREAM_IP, server_hostname=TLS_HOSTNAME)
            l.info(f'Response {r.id}:{r.answer}')

        except KeyError:
            l.error("error")

        wire = r.to_wire()
        s.sendto(wire, host)