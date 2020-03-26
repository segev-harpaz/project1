# -*- coding: utf-8 -*-
import sqlite3
from flask import Flask, render_template, request
from scapy.all import *
import os.path
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "project.db")
global db
db = sqlite3.connect(db_path)
cursor = db.execute("SELECT * from PRO")
app = Flask(__name__)


def check(data):
    isit = False
    for row in cursor:
        if row[0] == data[0]:
            isit = True
            break
        if row[1] == data[1]:
            isit = True
            break
    return isit


def start(mac_address, ip):
    @app.route('/')
    def student():
        return render_template('projectHTML.html')

    @app.route('/result', methods=['POST', 'GET'])
    def result():
        if request.method == 'POST':
            result = request.form
            result = str(result)[:-2]
            num = result.split(',')
            data = []
            for i in range(1, 6, 2):
                data.append(num[i][2:-2])
            num = check(ip)
            if num:
                return render_template("projectHTML.html", result="change your name or password")
            else:
                db.execute("INSERT INTO PRO (name, password, mac_address, class) \ VALUES (?,?,?,?,?)", (data[0], data[1], mac_address, data[1]))
                return render_template('pass.html')


def set_db(mac, ip):
    db.execute("UPDATE PRO SET current_ip = ? WHERE mac_address = ?", (ip, mac))


def filter_dhcp(pac):
    return DHCP in pac


def main():
    while True:
        checker = False
        packets = sniff(count=1, lfilter=filter_dhcp)
        for row in cursor:
            if row[3] == packets[0][Ether].dst:
                checker = True
                set_db(packets[0][Ether].dst, packets[0][IP].dst)
                break
        if not checker:
            start(packets[0][Ether].dst, packets[0][IP].dst)


if __name__ == '__main__':
    main()
