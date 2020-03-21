# -*- coding: utf-8 -*-
import sys
import sqlite3
i, o, e = sys.stdin, sys.stdout, sys.stderr
from scapy.all import *
sys.stdin, sys.stdout, sys.stderr = i, o, e
conn = sqlite3.connect('project.db')
global cursor
cursor = conn.execute("SELECT * from users")


def main():
    check = False
    packets = sniff(count=1, filter='dhcp and host 127.0.0.1')
    for row in cursor:
        if row[0] == packets[0][Ethernet].dst:
            check = True
    if not check:
        conn.execute("INSERT INTO project         (mac_address,current_ip,name) \
              VALUES (?, ?, 'Segev' )", (packets[0][Ethernet].dst, packets[0][IP].dst));


if __name__ == '__main__':
    main()
